import json


# -----------------------------------
# Recursive comparison function
# -----------------------------------

def compare_nested(cloud_val, iac_val, parent_key=""):
    """
    Compares values recursively and returns list of changes.
    """

    changes = []

    # If both values are dictionaries, go deeper
    if isinstance(cloud_val, dict) and isinstance(iac_val, dict):

        # Get all keys from both dictionaries
        all_keys = set(cloud_val.keys()) | set(iac_val.keys())

        for key in all_keys:

            # Build dot notation path
            if parent_key == "":
                full_key = key
            else:
                full_key = parent_key + "." + key

            cloud_child = cloud_val.get(key)
            iac_child = iac_val.get(key)

            # Recursively compare deeper levels
            deeper_changes = compare_nested(cloud_child, iac_child, full_key)

            changes.extend(deeper_changes)

    else:
        # If values are not dictionaries, compare directly
        if cloud_val != iac_val:

            changes.append({
                "KeyName": parent_key,
                "CloudValue": cloud_val,
                "IacValue": iac_val
            })

    return changes


# -----------------------------------
# Main analyzer function
# -----------------------------------

def analyze_files(cloud_list, iac_list):

    report = []

    # Convert IaC list to dictionary for fast lookup
    iac_dict = {}

    for item in iac_list:
        resource_id = item["id"]
        iac_dict[resource_id] = item

    # Compare each cloud resource
    for cloud_resource in cloud_list:

        resource_id = cloud_resource["id"]

        state = "Match"
        change_log = []

        # Find IaC version
        iac_resource = iac_dict.get(resource_id)

        if iac_resource is None:

            state = "Missing"

        else:

            # Compare recursively
            change_log = compare_nested(cloud_resource, iac_resource)

            # Remove id comparison if it appears
            change_log = [c for c in change_log if c["KeyName"] != "id"]

            if len(change_log) > 0:
                state = "Modified"

        report.append({
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": iac_resource,
            "State": state,
            "ChangeLog": change_log
        })

    return report


# -----------------------------------
# Run analyzer from JSON files
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