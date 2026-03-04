import json

# Load JSON files

with open("cloud_resources.json") as f:
    cloud_list = json.load(f)

with open("iac_resources.json") as f:
    iac_list = json.load(f)

# Convert IaC list to dictionary to be able to find any IaC resource by id

iac_dict = {}

for item in iac_list:
    resource_id = item["id"]
    iac_dict[resource_id] = item


# Compare resources

report = []

for cloud_resource in cloud_list:

    resource_id = cloud_resource["id"]

    state = "Match"
    change_log = []

    # Try to find matching IaC resource
    iac_resource = iac_dict.get(resource_id)

    if iac_resource is None:
        # Resource exists in Cloud but not in IaC
        state = "Missing"
    else:
        # Compare each field inside the Cloud resource, skipping id first of all.
        for key in cloud_resource:

            if key == "id":
                continue

            cloud_value = cloud_resource.get(key)
            iac_value = iac_resource.get(key)

            if cloud_value != iac_value:
                state = "Modified"
                change_log.append({
                    "KeyName": key,
                    "CloudValue": cloud_value,
                    "IacValue": iac_value
                })

    report.append({
        "CloudResourceItem": cloud_resource,
        "IacResourceItem": iac_resource,
        "State": state,
        "ChangeLog": change_log
    })


print(json.dumps(report, indent=2))

with open("report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Report generated locally as report.json")