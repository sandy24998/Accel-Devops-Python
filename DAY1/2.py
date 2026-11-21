import time

servers=["web1","web2","web3"]
for server in servers:
    print("Restarting",server)
    print(f"Restarting {server}") # Recommended Way


servers={"a":"web1","b":"web2","c":"web3"}
for i, s in servers.items():
    print(f"Restarting {i}={s}")


attempts = 0
max_attempts = 5
service_ready = False

while not service_ready and attempts < max_attempts:
    attempts += 1
    print(f"Attempt {attempts}: Checking if database is ready...")
    # Simulate becoming ready on attempt 3
    if attempts == 3:
        service_ready = True
    else:
        time.sleep(0.1)

print("Database connected!" if service_ready else "Timed out waiting for DB.")


#Break, continue and pass
servers = ["web01", "web02", "web03", "web04"]
for server in servers:
    if server == "web03":
        print("Critical server found")
        break
    print(f"Checking {server}")

servers = ["web01", "web02", "web03", "web04"]
for server in servers:
    if server == "web03":
        continue
    print(f"Checking {server}")

environment = "productiqon"
if environment == "production":
    pass
else:
    print("Non-production environment")

#Functions
def demo(name:str) -> str:
    return f"hello {name}"
msg=demo("Sandeep")
print(msg)


#Function Arguments
#Postional Arguments
def demo(name:str, age:int) -> str:
    return f"hello {name}, my age is {age}"
msg=demo("Sandeep", 28)  # Order matters here
msg=demo(28, "sandeep")  # Order matters here
print(msg)

#keywords Arguments
def demo(name:str, age:int) -> str:
    return f"hello {name}, my age is {age}"
msg=demo(age=28,name="Sandeep") # Order does'nt matters here
print(msg)

#Default Arguments
def demo(name:str, age:int=20) -> str:  # Here Default Passed if no age passed in function call
    return f"hello {name}, my age is {age}"
msg=demo(name="Sandeep") # Order does'nt matters here
print(msg)