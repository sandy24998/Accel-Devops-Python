print("Hello Sandeep")


name="Sandeep"

if name == "Sandeep":
    print("inside If")

# This is a comment


name = "Sandeep"
experience = 5
devops_experience = 3.5
is_certified = True

print(type(name))
print(type(experience))
print(type(devops_experience))
print(type(is_certified))


instance_id = "i-0123456789"
cpu_utilization = 76.5
is_running = True
instance_count = 5
server_ip = None

print(type(instance_id))
print(type(cpu_utilization))
print(type(is_running))
print(type(instance_count))
print(type(server_ip))



# String to integer
instance_count = "10"
instance_count = int(instance_count)

# Integer to string
server_port = 8080
server_port = str(server_port)

# String to float
cpu_usage = "75.5"
cpu_usage = float(cpu_usage)

# Integer to float
memory = float(16)

print(instance_count)
print(server_port)
print(cpu_usage)
print(memory)


value = "100"

print(value + "200")       # 100200
print(int(value) + 200)    # 300

#Arithmetic operators
a = 10
b = 20

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** 2)

# Comparison operators
cpu_usage = 85

print(cpu_usage == 85)
print(cpu_usage != 85)
print(cpu_usage > 80)
print(cpu_usage < 90)
print(cpu_usage >= 85)
print(cpu_usage <= 90)


# Logical operators
cpu_usage = 85
memory_usage = 70

if cpu_usage > 80 and memory_usage > 60:
    print("High resource utilization")

if cpu_usage > 90 or memory_usage > 90:
    print("Critical alert")

if not cpu_usage < 90:
    print("CPU is at or above 90%")


# Membership operators
services = ["nginx", "docker", "jenkins"]

print("membership is","docker" in services)
print("mysql" not in services)    


# Identity operators
a = None
b = None

print(a is b)
print(a is not b)



#Strings and string methods

service = "Amazon EC2"

print(service)
print(service[0])
print(service[-1])
print(service[0:6])
print(len(service))


#string methods:

server = "  production-ec2  "

print(server.upper())
print(server.lower())
print(server.strip())
print(server.replace("ec2", "eks"))
print(server.startswith("production"))
print(server.endswith("ec2"))
print(server.find("ec2"))
print(server.split("-"))

# String formatting using f-strings:

server = "web-server-01"
cpu_usage = 85

print(f"Server: {server}")
print(f"CPU utilization: {cpu_usage}%")
print(f"ALERT: {server} CPU utilization is {cpu_usage}%")


#String slicing:

name = "sandeep"

print(name[0:5])
print(name[:5])
print(name[2:])
print(name[-5:])
print(name[::2])


#Lists and list methods

services = ["nginx", "docker", "jenkins", "kubernetes"]

print(services)
print(services[0])
print(services[-1])

services.append("terraform")
services.insert(1, "prometheus")
services.remove("docker")
services.pop()
print(services)


numbers = [40, 10, 30, 20]

numbers.sort()
print(numbers)

numbers.reverse()
print(numbers)

print(len(numbers))
print(max(numbers))
print(min(numbers))
print(sum(numbers))


#Tuples and tuple operations

aws_regions = ("ap-south-1", "us-east-1", "eu-west-1")

print(aws_regions[0])
print(aws_regions[1])
print(len(aws_regions))

# Tuple operations:
regions = ("ap-south-1", "us-east-1", "ap-south-1")

print(regions.count("ap-south-1"))
print(regions.index("us-east-1"))

#Tuple unpacking:
server = ("web01", "10.0.1.10", "running")

name, ip, status = server

print(name)
print(ip)
print(status)


# Sets and set operations

ports = {22, 80, 443, 8080, 80}
print(ports)

ports.add(3306)
ports.remove(22)
ports.discard(9999)
print(ports)

# Set operations:

production_ports = {22, 80, 443, 8080}
development_ports = {22, 3000, 8080}

# Common elements
print(production_ports.intersection(development_ports))

# All unique elements
print(production_ports.union(development_ports))

# Elements only in production
print(production_ports.difference(development_ports))



# Dictionaries and dictionary methods

server = {
    "name": "web-server-01",
    "ip": "10.0.1.10",
    "status": "running",
    "cpu": 75
}

print(server)
print(server["name"])
print(server["ip"])
print(server["status"])

# Accessing values safely:
print(server.get("name"))

print(server.get("memory", 0))

# Adding and updating values:
server["memory"] = 65
server["status"] = "stopped"
server.update({"environment": "production"})
print(server)

# Removing values:
server.pop("cpu")
del server["ip"]
print(server)

# dictionary methods:
print(server.keys())
print(server.values())
print(server.items())


# Looping through dictionaries:

server = {
    "name": "web01",
    "environment": "production",
    "status": "running"
}

for key, value in server.items():
    print(f"{key}: {value}")

# Nested dictionaries:

ec2_instance = {
    "InstanceId": "i-123456789",
    "InstanceType": "t3.medium",
    "State": {
        "Name": "running"
    },
    "Tags": {
        "Environment": "production",
        "Owner": "DevOps"
    }
}

print(ec2_instance["InstanceId"])
print(ec2_instance["State"]["Name"])
print(ec2_instance["Tags"]["Environment"])

# Conditional statements (if, elif, else)

cpu_usage = 85

if cpu_usage > 90:
    print("Critical CPU alert")

elif cpu_usage > 75:
    print("Warning: High CPU usage")

else:
    print("CPU utilization is normal")

cpu = 45
memory = 60
disk = 70
service_status = "running"

if cpu < 80 and memory < 80 and disk < 80 and service_status == "running":
    print("Server is ready for deployment")
else:
    print("Server is not ready for deployment")  


# Loops (for, while)

servers = ["web01", "web02", "db01", "app01"]

for server in servers:
    print(f"Checking {server}")    

for i in range(1, 6):
    print(i)

servers = ["web01", "web02", "db01"]

for index, server in enumerate(servers, start=1):
    print(index, server)