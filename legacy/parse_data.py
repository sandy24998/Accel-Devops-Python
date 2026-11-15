#Q3. Parse this JSON (simulate AWS/GCP response) and extract the list of instance IDs that are in "running" state:

data = {
    "Reservations": [
        {"Instances": [{"InstanceId": "i-123", "State": {"Name": "running"}}]},
        {"Instances": [{"InstanceId": "i-456", "State": {"Name": "stopped"}}]},
        {"Instances": [{"InstanceId": "i-789", "State": {"Name": "running"}}]}
    ]
}


running_instances = []

for r in data["Reservations"]:
    for i in r["Instances"]:
        if i["State"]["Name"] == "running":
            running_instances.append(i["InstanceId"])


print(running_instances)