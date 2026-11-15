# DevOps Automation Suite - Setup & Quick Start Guide

## System Requirements

- **Python**: 3.6 or higher
- **OS**: Linux/Unix (MacOS compatible, Windows with WSL)
- **Disk Space**: 500MB+ for backups and logs (depends on usage)
- **Permissions**: Root/sudo access for system-level operations

## Installation

### Option 1: Direct Installation

```bash
# 1. Clone or download the repository
cd /home/sandeep/Devops/python/Accel-Devops-Python

# 2. Make scripts executable
chmod +x *.py

# 3. Verify Python version
python3 --version  # Should be 3.6+

# 4. Test basic import
python3 -c "from deployment import DeploymentManager; print('✓ Ready to use')"
```

### Option 2: Virtual Environment (Recommended)

```bash
# 1. Create virtual environment
python3 -m venv devops_env
source devops_env/bin/activate

# 2. No additional packages needed!
# All modules use only standard library
```

## Quick Start (5 minutes)

### 1. Test Shell Automation

```bash
python3 -c "
from shell_automation import ShellCommandExecutor

executor = ShellCommandExecutor()
executor.execute_command('echo \"Hello from DevOps Suite!\"')
"
```

### 2. Test File Cleanup (Dry-Run)

```bash
python3 -c "
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager('/tmp')
cleanup.set_dry_run(True)
cleanup.cleanup_old_files(age_days=30)
print('✓ Dry-run successful')
"
```

### 3. Test Backup Creation

```bash
python3 -c "
from backup_enhanced import BackupManager
import os

# Create test directory
os.makedirs('/tmp/test_backup/source', exist_ok=True)
with open('/tmp/test_backup/source/test.txt', 'w') as f:
    f.write('test data')

# Create backup
backup = BackupManager('/tmp/test_backup/source', '/tmp/test_backup/backups')
backup_dir = backup.perform_full_backup()
backup.verify_backup(backup_dir)
print('✓ Backup successful')
"
```

## File Structure

```
Accel-Devops-Python/
├── deployment.py              # Deployment & rollback
├── backup_enhanced.py         # Backup management
├── file_cleanup.py            # File cleanup
├── log_rotation.py            # Log rotation
├── shell_automation.py        # Command execution
├── devops_hub.py              # Interactive menu
├── examples.py                # Practical examples
├── DEVOPS_SUITE_README.md    # Full documentation
├── SETUP_GUIDE.md            # This file
├── requirements.txt           # Dependencies (empty - uses stdlib)
└── README.md                  # Project info
```

## Common Usage Patterns

### Pattern 1: Daily Backup at 2 AM

Create `/etc/cron.d/devops_backup`:
```bash
0 2 * * * /usr/bin/python3 /path/to/backup_enhanced.py
```

Or create `daily_backup.py`:
```python
#!/usr/bin/env python3
from backup_enhanced import BackupManager

backup = BackupManager('/var/www', '/backup')
backup_dir = backup.perform_full_backup()
backup.verify_backup(backup_dir)
backup.compress_backup(backup_dir)
backup.cleanup_old_backups(retention_days=30)
```

Then in crontab:
```bash
0 2 * * * /usr/bin/python3 /path/to/daily_backup.py
```

### Pattern 2: Log Rotation on Deployment

```python
#!/usr/bin/env python3
from deployment import DeploymentManager
from log_rotation import LogRotationManager

deployer = DeploymentManager('/app')
logs = LogRotationManager('/var/log/app')

# Before deployment
logs.rotate_all_logs()

# Deploy
deployer.deploy_files('/tmp/release')

# After deployment
logs.rotate_all_logs()
```

### Pattern 3: Scheduled Cleanup

Create `/opt/devops/cleanup_script.py`:
```python
#!/usr/bin/env python3
from file_cleanup import FileCleanupManager
from log_rotation import LogRotationManager

# Clean old files (> 30 days)
cleanup = FileCleanupManager('/var/log')
cleanup.set_dry_run(False)
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()

# Rotate logs
logs = LogRotationManager('/var/log/app')
logs.rotate_all_logs()
logs.cleanup_old_backups(retention_days=60)
```

Schedule with cron:
```bash
# Every Sunday at 3 AM
0 3 * * 0 /usr/bin/python3 /opt/devops/cleanup_script.py
```

## Configuration Examples

### Deployment Configuration

```python
from deployment import DeploymentManager

deployer = DeploymentManager(
    app_root='/var/www/production',
    backup_dir='/backup/production'
)

deployer.check_system_resources()
deployer.backup_current_deployment()
deployer.deploy_files('/tmp/release')
deployer.verify_deployment(['app.py', 'config.yaml'])
deployer.cleanup_old_deployments(keep_count=10)
```

### Backup Configuration

```python
from backup_enhanced import BackupManager

backup = BackupManager(
    source_dir='/var/www',
    backup_root='/backup',
    backup_type='incremental'  # or 'full'
)

backup.perform_incremental_backup()
backup.cleanup_old_backups(retention_days=30, keep_min=5)
```

### Log Rotation Configuration

```python
from log_rotation import LogRotationManager

config = {
    'max_file_size': 100 * 1024 * 1024,   # 100MB
    'max_files': 20,                       # Keep 20 backups
    'retention_days': 90,                  # Delete after 90 days
    'backup_dir': '/var/log/backups'
}

logs = LogRotationManager('/var/log/app', config)
logs.rotate_all_logs()
logs.cleanup_old_backups()
```

### Cleanup Configuration

```python
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager(
    cleanup_root='/tmp',
    log_file='/var/log/cleanup.log'
)

# Dry-run first
cleanup.set_dry_run(True)
cleanup.cleanup_old_files(age_days=30)

# Then execute
cleanup.set_dry_run(False)
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()
cleanup.cleanup_empty_directories()
```

## Troubleshooting

### Issue: Permission Denied

```bash
# Solution: Make scripts executable
chmod +x *.py

# Or run with sudo
sudo python3 deployment.py
```

### Issue: Module Not Found

```bash
# Solution: Ensure you're in the correct directory
cd /path/to/Accel-Devops-Python

# Or add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/path/to/Accel-Devops-Python
```

### Issue: Backup Failed - Disk Space

```bash
# Check available space
df -h /backup

# Clean old backups
python3 -c "
from backup_enhanced import BackupManager
backup = BackupManager('/var/www', '/backup')
backup.cleanup_old_backups(retention_days=7, keep_min=2)
"
```

### Issue: Log Rotation Not Working

```bash
# Check log file path exists
ls -la /var/log/myapp

# Check permissions
chmod 755 /var/log/myapp

# Test rotation manually
python3 -c "
from log_rotation import LogRotationManager
logs = LogRotationManager('/var/log/myapp')
logs.rotate_all_logs()
"
```

## Best Practices

### 1. Always Use Dry-Run First
```python
cleanup.set_dry_run(True)
cleanup.cleanup_old_files(age_days=30)  # Preview
cleanup.set_dry_run(False)
cleanup.cleanup_old_files(age_days=30)  # Execute
```

### 2. Test Rollback Procedure
```python
# Test that rollback works
deployer.list_deployments()
deployer.rollback('backup_20240101_120000')
```

### 3. Monitor Backup Sizes
```python
backup.list_backups()  # Check sizes regularly
backup.cleanup_old_backups(retention_days=30)  # Clean regularly
```

### 4. Enable Command History
```python
executor = ShellCommandExecutor()
executor.execute_command('some_command')
executor.export_history('/var/log/command_history.txt')
```

### 5. Regular Testing
```bash
# Monthly test
python3 -c "
from backup_enhanced import BackupManager
backup = BackupManager('/var/www', '/backup')
# Test restore
backup.restore_backup('/backup/latest', '/tmp/restore_test')
"
```

## Performance Tips

### For Large Deployments
```python
# Use incremental backup
backup = BackupManager(source, backup_root, backup_type='incremental')
backup.perform_incremental_backup()  # Faster than full
```

### For Many Log Files
```python
# Rotate only specific pattern
logs.rotate_all_logs(pattern='app')  # Only app*.log

# Increase max file size to reduce rotations
config['max_file_size'] = 200 * 1024 * 1024  # 200MB
```

### For Large File Cleanup
```python
# Process in batches
cleanup.cleanup_old_files(age_days=60)    # First pass
cleanup.cleanup_old_files(age_days=30)    # Second pass
cleanup.cleanup_empty_directories()        # Final cleanup
```

## Monitoring & Alerting

### Check Backup Status
```python
from backup_enhanced import BackupManager

backup = BackupManager('/var/www', '/backup')
backups = backup.list_backups()

if not backups:
    print("ALERT: No backups found!")
elif len(backups) < 3:
    print("WARNING: Only", len(backups), "backups available")
```

### Monitor Log Rotation
```python
from log_rotation import LogRotationManager

logs = LogRotationManager('/var/log/app')
stats = logs.get_rotation_stats()

if stats['total_backup_size'] > 100 * 1024 * 1024 * 1024:  # 100GB
    print("ALERT: Backup size exceeds 100GB")
```

## Integration Examples

### With Cron

```bash
# /etc/cron.d/devops

# Daily backup at 2 AM
0 2 * * * root /usr/bin/python3 /opt/devops/backup_script.py >> /var/log/devops_backup.log 2>&1

# Log rotation every 6 hours
0 */6 * * * root /usr/bin/python3 /opt/devops/log_rotation_script.py >> /var/log/devops_rotation.log 2>&1

# Cleanup every Sunday at 3 AM
0 3 * * 0 root /usr/bin/python3 /opt/devops/cleanup_script.py >> /var/log/devops_cleanup.log 2>&1
```

### With Systemd Timer

Create `/etc/systemd/system/devops-backup.service`:
```ini
[Unit]
Description=DevOps Backup Service
After=network.target

[Service]
Type=oneshot
User=devops
ExecStart=/usr/bin/python3 /opt/devops/backup_script.py
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/devops-backup.timer`:
```ini
[Unit]
Description=DevOps Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=02:00
Unit=devops-backup.service

[Install]
WantedBy=timers.target
```

Enable:
```bash
systemctl daemon-reload
systemctl enable devops-backup.timer
systemctl start devops-backup.timer
```

## Documentation Links

- [Full Documentation](./DEVOPS_SUITE_README.md)
- [Practical Examples](./examples.py)
- [Individual Module Docs](./DEVOPS_SUITE_README.md)

## Support & Troubleshooting

### Get Help
```python
from deployment import DeploymentManager
help(DeploymentManager)  # Show class documentation

from deployment import DeploymentManager
dm = DeploymentManager('/app')
help(dm.deploy_files)  # Show method documentation
```

### View Logs
```bash
# Deployment logs
cat /app/.deployments/deployment.log

# Backup logs
cat /backup/myapp/backup.log

# Cleanup logs
cat /tmp/cleanup.log

# Log rotation logs
cat /var/log/myapp/rotation.log

# Shell command logs
cat /tmp/commands.log
```

## Version Info

- **Suite Version**: 1.0
- **Python**: 3.6+
- **Dependencies**: None (stdlib only)
- **License**: MIT

---

**Ready to automate your DevOps tasks? Start with the examples or run the interactive hub!**

```bash
python3 devops_hub.py        # Interactive menu
python3 examples.py           # Practical examples
```
