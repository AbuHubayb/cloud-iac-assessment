import json


"""
Cloud IaC Analyzer

Compares cloud resources with Infrastructure-as-Code (IaC) definitions.

States:
- Match: Cloud and IaC resources are identical
- Missing: Resource exists in Cloud but not IaC
- Modified: Resource exists but properties differ
- Orphaned: Resource exists in IaC but not Cloud
"""


# -----------------------------------
# Recursive comparison
# -----------------------------------

def compare_nested(cloud_val, iac_val, parent_key=""):

    changes = []

    if isinstance(cloud_val, dict) and isinstance(iac_val, dict):

        all_keys = set(cloud_val.keys()) | set(iac_val.keys())

        for key in all_keys:

            if parent_key == "":
                full_key = key
            else:
                full_key = parent_key + "." + key

            cloud_child = cloud_val.get(key)
            iac_child = iac_val.get(key)

            deeper_changes = compare_nested(cloud_child, iac_child, full_key)

            changes.extend(deeper_changes)

    else:

        if cloud_val != iac_val:

            changes.append({
                "KeyName": parent_key,
                "CloudValue": cloud_val,
                "IacValue": iac_val
            })

    return changes


# -----------------------------------
# Main analyzer
# -----------------------------------

def analyze_files(cloud_list, iac_list):

    report = []

    cloud_dict = {}
    iac_dict = {}

    # Convert cloud list to dictionary
    for item in cloud_list:
        cloud_dict[item["id"]] = item

    # Convert IaC list to dictionary
    for item in iac_list:
        iac_dict[item["id"]] = item

    # -----------------------------------
    # Check Cloud → IaC
    # -----------------------------------

    for resource_id, cloud_resource in cloud_dict.items():

        state = "Match"
        change_log = []

        iac_resource = iac_dict.get(resource_id)

        if iac_resource is None:

            state = "Missing"

        else:

            change_log = compare_nested(cloud_resource, iac_resource)

            change_log = [c for c in change_log if c["KeyName"] != "id"]

            if len(change_log) > 0:
                state = "Modified"

        report.append({
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": iac_resource,
            "State": state,
            "ChangeLog": change_log
        })

    # -----------------------------------
    # Check IaC → Cloud (Orphaned)
    # -----------------------------------

    for resource_id, iac_resource in iac_dict.items():

        if resource_id not in cloud_dict:

            report.append({
                "CloudResourceItem": None,
                "IacResourceItem": iac_resource,
                "State": "Orphaned",
                "ChangeLog": []
            })

    return report


# -----------------------------------
# Run analyzer
# -----------------------------------

if __name__ == "__main__":

    with open("cloud_resources.json") as f:
        cloud_list = json.load(f)

    with open("iac_resources.json") as f:
        iac_list = json.load(f)

    result = analyze_files(cloud_list, iac_list)

    print(json.dumps(result, indent=2))

    with open("report.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Report generated as report.json")