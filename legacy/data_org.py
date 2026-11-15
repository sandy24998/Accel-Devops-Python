file_path="requirements.txt"

with open(file_path, "r") as file:
    lines = file.readlines() ## store as list

print(lines )


packages = [
    line.strip()
    for line in lines
    if line.strip() and not line.strip().startswith("#")
]

print(f"before sorting - {packages}" )

packages.sort()

print(f"After sorting - {packages}" )


with open(file_path, "w") as file:
    for p in packages:
        file.write(p + "\n")


print(f"Final file Updates" )
