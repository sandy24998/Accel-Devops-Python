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