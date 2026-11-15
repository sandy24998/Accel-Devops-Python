# DevOps Automation Suite - Quick Reference Card

## 📦 What You Get

5 Production-Ready Python Modules + Interactive Tools + Comprehensive Documentation

**No external dependencies - uses only Python stdlib**

---

## 🚀 Start in 30 Seconds

```bash
# Run the interactive menu
python3 devops_hub.py

# Or run practical examples
python3 examples.py

# Or use directly in Python
python3 -c "from deployment import DeploymentManager; help(DeploymentManager)"
```

---

## 🔧 5 Core Modules

### 1. Deployment (deployment.py)
```python
from deployment import DeploymentManager

deployer = DeploymentManager('/app')
deployer.backup_current_deployment()
deployer.deploy_files('/tmp/release')
deployer.verify_deployment(['app.py'])
deployer.rollback()  # If needed
```
**Use for**: Safe application deployments with automatic rollback

---

### 2. Backup (backup_enhanced.py)
```python
from backup_enhanced import BackupManager

backup = BackupManager('/var/www', '/backup')
backup.perform_full_backup()
backup.verify_backup(backup_dir)
backup.compress_backup(backup_dir)
backup.cleanup_old_backups(retention_days=30)
```
**Use for**: Automated backups with verification and restore

---

### 3. File Cleanup (file_cleanup.py)
```python
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager('/tmp')
cleanup.set_dry_run(True)  # Preview
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()
cleanup.cleanup_empty_directories()
```
**Use for**: Clean old files and optimize disk space

---

### 4. Log Rotation (log_rotation.py)
```python
from log_rotation import LogRotationManager

logs = LogRotationManager('/var/log/app')
logs.rotate_all_logs()
logs.compress_old_backups()
logs.cleanup_old_backups()
logs.analyze_log_sizes()
```
**Use for**: Automatic log management and rotation

---

### 5. Shell Automation (shell_automation.py)
```python
from shell_automation import ShellCommandExecutor

executor = ShellCommandExecutor()
executor.execute_command('ls -la')
executor.execute_command_batch(['cmd1', 'cmd2'])
executor.execute_command_with_retry('deploy.sh', max_retries=3)
executor.execute_parallel_commands(['task1', 'task2'])
executor.pipe_commands(['find .', 'xargs wc -l'])
```
**Use for**: Complex shell command automation

---

## 📁 File Structure

```
Module Files:
├── deployment.py              (Deployment & rollback)
├── backup_enhanced.py         (Backup management)
├── file_cleanup.py            (File cleanup)
├── log_rotation.py            (Log rotation)
└── shell_automation.py        (Command automation)

Tools & Utilities:
├── devops_hub.py              (Interactive menu)
└── examples.py                (7 real-world examples)

Documentation:
├── INDEX.md                   (Quick reference - START HERE)
├── DEVOPS_SUITE_README.md     (Complete docs)
├── SETUP_GUIDE.md             (Setup & config)
└── REQUIREMENTS_NOTES.md      (No dependencies!)
```

---

## 🎯 Common Tasks

### Deploy a New Version
```python
from deployment import DeploymentManager

deployer = DeploymentManager('/app')
deployer.backup_current_deployment()
deployer.deploy_files('/tmp/release/v2.0.0')
deployer.verify_deployment(['app.py', 'config.yaml'])
deployer.cleanup_old_deployments(keep_count=5)
```

### Create Daily Backup
```python
from backup_enhanced import BackupManager

backup = BackupManager('/var/www', '/backup')
backup_dir = backup.perform_full_backup()
backup.verify_backup(backup_dir)
backup.compress_backup(backup_dir)
backup.cleanup_old_backups(retention_days=30, keep_min=3)
```

### Clean Old Files
```python
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager('/tmp')
cleanup.cleanup_old_files(age_days=30)      # Files older than 30 days
cleanup.cleanup_temp_files()                 # .tmp, .log, .bak files
cleanup.cleanup_empty_directories()          # Remove empty dirs
```

### Rotate Logs
```python
from log_rotation import LogRotationManager

logs = LogRotationManager('/var/log/app', config={
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'retention_days': 60,
    'max_files': 10
})

logs.rotate_all_logs()
logs.compress_old_backups()
logs.cleanup_old_backups()
```

### Execute Commands
```python
from shell_automation import ShellCommandExecutor

executor = ShellCommandExecutor()

# Single command
executor.execute_command('make build')

# Batch with error handling
executor.execute_command_batch([
    'npm install',
    'npm run build',
    'npm run test'
], stop_on_error=True)

# With retry
executor.execute_command_with_retry('deploy.sh', max_retries=3, retry_delay=5)

# Parallel
executor.execute_parallel_commands([
    'npm run build',
    'npm run lint',
    'npm run test'
])

# Show history
executor.print_command_history()
```

---

## ⚙️ Configuration Patterns

### Deployment
```python
DeploymentManager(
    app_root='/var/www/app',
    backup_dir='/backups'
)
```

### Backup
```python
BackupManager(
    source_dir='/var/www',
    backup_root='/backup',
    backup_type='full'  # or 'incremental'
)
```

### Log Rotation
```python
config = {
    'max_file_size': 100 * 1024 * 1024,
    'max_files': 10,
    'retention_days': 30,
    'backup_dir': '/var/log/backups'
}
LogRotationManager('/var/log/app', config)
```

### File Cleanup
```python
FileCleanupManager(
    cleanup_root='/tmp',
    log_file='/var/log/cleanup.log'
).set_dry_run(True)  # Preview first
```

---

## 📋 Cron Examples

### Daily Backup (2 AM)
```bash
0 2 * * * /usr/bin/python3 /opt/devops/backup.py
```

### Log Rotation (Every 6 hours)
```bash
0 */6 * * * /usr/bin/python3 /opt/devops/logs.py
```

### Weekly Cleanup (Sunday 3 AM)
```bash
0 3 * * 0 /usr/bin/python3 /opt/devops/cleanup.py
```

---

## 🔍 Debug & Inspect

### Check Module Documentation
```python
from deployment import DeploymentManager
help(DeploymentManager)
help(DeploymentManager.deploy_files)
```

### View Logs
```bash
# Deployment
cat /app/.deployments/deployment.log

# Backup
cat /backup/myapp/backup.log

# Cleanup
cat /tmp/cleanup.log

# Log rotation
cat /var/log/myapp/rotation.log

# Shell commands
cat /tmp/commands.log
```

### Test Dry-Run
```python
cleanup = FileCleanupManager('/tmp')
cleanup.set_dry_run(True)
cleanup.cleanup_old_files(age_days=30)  # Preview only
```

---

## ⚠️ Best Practices

✅ **DO**:
- Use dry-run mode first
- Backup before deployment
- Test restore procedures
- Monitor backup sizes
- Keep multiple versions
- Check logs regularly

❌ **DON'T**:
- Skip verification steps
- Forget to backup
- Clean without dry-run
- Ignore disk space warnings
- Delete all old backups
- Run untested commands in production

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" | Run with `sudo` or fix ownership |
| "Module not found" | Check PYTHONPATH or cd to directory |
| "Disk full" | Run `backup.cleanup_old_backups()` |
| "Deployment failed" | Check `.deployments/deployment.log` |
| "Restore broken" | Verify backup: `backup.list_backups()` |

---

## 📚 Learn More

| Resource | Location |
|----------|----------|
| **Complete Docs** | DEVOPS_SUITE_README.md |
| **Setup Guide** | SETUP_GUIDE.md |
| **Examples** | examples.py |
| **Interactive** | devops_hub.py |
| **This File** | INDEX.md |

---

## 🎓 Learning Path

1. **Beginner** → Run `python3 devops_hub.py`
2. **Intermediate** → Run `python3 examples.py`
3. **Advanced** → Modify examples for your use case
4. **Expert** → Integrate into production CI/CD

---

## 💾 System Requirements

- Python 3.6+
- Linux/Unix (or WSL on Windows)
- Basic Unix tools (tar, gzip)
- File permissions to access directories

**That's it! No external packages needed.**

---

## 🚀 Get Started Now

### Option 1: Interactive Menu
```bash
python3 devops_hub.py
```

### Option 2: See Examples
```bash
python3 examples.py
```

### Option 3: Use Directly
```bash
python3 -c "
from deployment import DeploymentManager
DeploymentManager('/app').deploy_files('/tmp/release')
"
```

### Option 4: Read Documentation
```bash
cat INDEX.md          # This file
cat DEVOPS_SUITE_README.md
cat SETUP_GUIDE.md
```

---

## 📞 Quick Help

```bash
# Show this quick reference
less QUICK_REFERENCE.md

# Run interactive menu
python3 devops_hub.py

# See examples
python3 examples.py

# Get module help
python3 -c "from deployment import DeploymentManager; help(DeploymentManager)"

# View logs
tail -f /path/to/*.log

# Check Python version
python3 --version  # Should be 3.6+
```

---

**Version**: 1.0  
**Status**: ✅ Production Ready  
**Updated**: May 2024

**Quick links**:
- Start: `python3 devops_hub.py`
- Examples: `python3 examples.py`
- Docs: `DEVOPS_SUITE_README.md`
- Setup: `SETUP_GUIDE.md`
- Index: `INDEX.md`

---

## 📞 One Last Thing...

**No external dependencies!**

Everything uses only Python stdlib:
- `os` - File operations
- `datetime` - Date/time
- `subprocess` - Shell commands
- `time` - Timing operations

Just `python3 file.py` and go!

---

**Ready? Type this:**
```bash
python3 devops_hub.py
```

**Let's automate! 🚀**
