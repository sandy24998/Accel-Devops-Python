import os
from datetime import datetime
print(datetime.now());
timestamp = datetime.now().strftime("%Y%m%d")
print(timestamp)

backup_name = f"backup-{timestamp}.tar.gz"
print(backup_name)

os.system(f"tar -czf {backup_name} myproject/")

print("Backup completed")