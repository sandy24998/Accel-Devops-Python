# DevOps Automation Suite - Documentation

**Using OS Library Only** - Pure Python with standard library modules

## Overview

Complete DevOps automation toolkit with 5 core modules:
- **Deployment Scripts** - Application deployment with rollback
- **Backup Automation** - Full/incremental backups with verification
- **File Cleanup** - Automated file and directory cleanup
- **Log Rotation** - Log file management and rotation
- **Shell Automation** - Command execution and automation

## Modules

### 1. Deployment Scripts (`deployment.py`)

Handle application deployments with automatic backups and rollback capability.

#### Key Features:
- ✓ System resource verification before deployment
- ✓ Automatic backup before deployment
- ✓ File deployment from source directory
- ✓ Deployment verification
- ✓ One-click rollback to previous version
- ✓ Deployment history and versioning
- ✓ Automatic cleanup of old deployments

#### Usage:
```python
from deployment import DeploymentManager

# Initialize
deployer = DeploymentManager('/var/www/myapp')

# Check system resources
if deployer.check_system_resources():
    # Backup current version
    deployer.backup_current_deployment('v1.0.0')
    
    # Deploy new files
    deployer.deploy_files('/tmp/release/v2.0.0')
    
    # Verify deployment
    if deployer.verify_deployment(['app.py', 'config.yaml']):
        print("Deployment successful!")
    else:
        # Rollback if verification fails
        deployer.rollback()

# List all deployments
deployer.list_deployments()

# Cleanup old deployments (keep 5 most recent)
deployer.cleanup_old_deployments(keep_count=5)
```

#### Methods:
- `check_system_resources()` - Verify disk space and system health
- `backup_current_deployment(version_name)` - Backup current deployment
- `deploy_files(source_dir, file_list)` - Deploy files from source
- `verify_deployment(expected_files)` - Verify all files deployed
- `rollback(backup_version)` - Rollback to previous deployment
- `list_deployments()` - List all available deployments
- `cleanup_old_deployments(keep_count)` - Clean old backups

---

### 2. Backup Automation (`backup_enhanced.py`)

Comprehensive backup management with full and incremental backups.

#### Key Features:
- ✓ Full backup of entire directory structure
- ✓ Incremental backup (only changed files)
- ✓ Backup verification and integrity checks
- ✓ Automatic compression (tar.gz)
- ✓ Restore from backup
- ✓ Cleanup old backups with retention policy
- ✓ Manifest tracking for incremental backups
- ✓ Detailed logging of all operations

#### Usage:
```python
from backup_enhanced import BackupManager

# Initialize
backup_mgr = BackupManager('/var/www', '/backup/myapp')

# Perform full backup
backup_dir = backup_mgr.perform_full_backup()

# Verify backup integrity
if backup_mgr.verify_backup(backup_dir):
    # Compress backup
    compressed = backup_mgr.compress_backup(backup_dir)

# Restore from backup
backup_mgr.restore_backup(backup_dir, '/var/www/restored')

# Cleanup old backups (keep at least 3, older than 30 days)
backup_mgr.cleanup_old_backups(retention_days=30, keep_min=3)

# List all backups
backup_mgr.list_backups()
```

#### Methods:
- `perform_full_backup()` - Create full backup
- `perform_incremental_backup()` - Create incremental backup
- `verify_backup(backup_dir)` - Verify backup integrity
- `compress_backup(backup_dir)` - Compress backup to tar.gz
- `restore_backup(backup_dir, restore_target)` - Restore from backup
- `cleanup_old_backups(retention_days, keep_min)` - Clean old backups
- `list_backups()` - List all available backups

---

### 3. File Cleanup (`file_cleanup.py`)

Automated cleanup of old files, temporary files, and directory optimization.

#### Key Features:
- ✓ Remove files older than specified days
- ✓ Remove empty directories recursively
- ✓ Cleanup temporary files (.tmp, .log, .bak, etc.)
- ✓ Identify and list large files
- ✓ Detect duplicate files
- ✓ Pattern-based cleanup
- ✓ Dry-run mode for safe testing
- ✓ Detailed cleanup reports
- ✓ Space utilization analysis

#### Usage:
```python
from file_cleanup import FileCleanupManager

# Initialize
cleanup = FileCleanupManager('/var/log')

# Enable dry-run to see what would be deleted
cleanup.set_dry_run(enabled=True)

# Remove files older than 30 days
cleanup.cleanup_old_files(age_days=30)

# Remove temporary files
cleanup.cleanup_temp_files()

# Remove empty directories
cleanup.cleanup_empty_directories()

# Find large files (>100MB)
large_files = cleanup.cleanup_large_files(min_size_mb=100)

# Find duplicates
duplicates = cleanup.cleanup_duplicate_files()

# Cleanup files matching pattern
cleanup.cleanup_by_pattern('*.tmp', remove=True)

# Generate report
cleanup.generate_cleanup_report()

# Actually perform cleanup (disable dry-run)
cleanup.set_dry_run(enabled=False)
cleanup.cleanup_old_files(age_days=30)
```

#### Methods:
- `cleanup_old_files(age_days, file_pattern)` - Remove old files
- `cleanup_empty_directories()` - Remove empty dirs
- `cleanup_temp_files()` - Remove temporary files
- `cleanup_large_files(min_size_mb)` - Find large files
- `cleanup_duplicate_files()` - Find duplicate files
- `cleanup_by_pattern(pattern, remove)` - Pattern-based cleanup
- `generate_cleanup_report()` - Generate usage report
- `set_dry_run(enabled)` - Enable/disable dry-run mode

---

### 4. Log Rotation (`log_rotation.py`)

Automatic log file management with rotation, compression, and archival.

#### Key Features:
- ✓ Size-based log rotation
- ✓ Automatic log file compression
- ✓ Backup directory management
- ✓ Retention policy enforcement
- ✓ Backup count limiting
- ✓ Log file analysis and reporting
- ✓ Rotation statistics
- ✓ Configuration file support

#### Usage:
```python
from log_rotation import LogRotationManager

# Initialize with default config
logs = LogRotationManager('/var/log/myapp')

# Or with custom config
config = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'max_files': 10,
    'retention_days': 60,
    'backup_dir': '/var/log/backups'
}
logs = LogRotationManager('/var/log/myapp', config)

# Rotate all logs
logs.rotate_all_logs()

# Rotate specific pattern
logs.rotate_all_logs(pattern='app')

# Compress old backups
logs.compress_old_backups()

# Cleanup old backups (> 30 days)
logs.cleanup_old_backups()

# Limit backup count to 10
logs.limit_backup_count()

# Analyze log files
logs.analyze_log_sizes()

# Get statistics
stats = logs.get_rotation_stats()
print(f"Total backups: {stats['total_backups']}")
print(f"Backup size: {stats['total_backup_size'] / 1024 / 1024:.2f}MB")

# Create config file
logs.create_config_file('/etc/devops/log_rotation.cfg')
```

#### Methods:
- `rotate_log_file(log_file_path)` - Rotate single log file
- `rotate_all_logs(pattern)` - Rotate all logs matching pattern
- `compress_old_backups()` - Compress backup files
- `cleanup_old_backups()` - Remove old backups
- `limit_backup_count()` - Enforce max backup limit
- `analyze_log_sizes()` - Analyze log file sizes
- `get_rotation_stats()` - Get rotation statistics
- `create_config_file(path)` - Create configuration file

---

### 5. Shell Automation (`shell_automation.py`)

Execute and manage system commands with advanced features.

#### Key Features:
- ✓ Execute single or batch commands
- ✓ Capture output or display to console
- ✓ Automatic retry with exponential backoff
- ✓ Conditional execution (if/else)
- ✓ Parallel command execution
- ✓ Command piping support
- ✓ Script file creation and execution
- ✓ Command history tracking
- ✓ History export and logging

#### Usage:
```python
from shell_automation import ShellCommandExecutor

# Initialize
executor = ShellCommandExecutor(work_dir='/app')

# Execute single command
ret_code, stdout, stderr = executor.execute_command('ls -la')

# Execute with output capture
executor.execute_command('make build', capture_output=True)

# Batch execution (stop on error)
commands = ['npm install', 'npm run build', 'npm run test']
results = executor.execute_command_batch(commands, stop_on_error=True)

# Execute with retry
executor.execute_command_with_retry(
    'npm run deploy',
    max_retries=3,
    retry_delay=5
)

# Conditional execution
executor.execute_if_condition(
    'test -f config.yaml',
    'echo "Config loaded"',
    'cp config.default.yaml config.yaml'
)

# Parallel execution
tasks = ['npm run build', 'npm run lint', 'npm run test']
results = executor.execute_parallel_commands(tasks)

# Piped commands
executor.pipe_commands([
    'find . -name "*.js"',
    'xargs wc -l',
    'sort -n'
])

# Create and execute script
script_path = '/tmp/deploy.sh'
executor.create_script_file(script_path, [
    'echo "Starting deployment"',
    'git pull',
    'make build',
    'make deploy'
])
executor.execute_script_file(script_path)

# View command history
executor.print_command_history()

# Export history
executor.export_history('/var/log/command_history.txt')
```

#### Methods:
- `execute_command(command, capture_output, check_return)` - Execute command
- `execute_command_batch(commands, stop_on_error)` - Batch execution
- `execute_command_with_retry(command, max_retries, retry_delay)` - Retry logic
- `execute_if_condition(condition, true_cmd, false_cmd)` - Conditional exec
- `execute_parallel_commands(commands)` - Parallel execution
- `pipe_commands(commands)` - Piped execution
- `execute_script_file(script_path)` - Execute shell script
- `create_script_file(script_path, commands)` - Create shell script
- `print_command_history()` - Display history
- `export_history(output_file)` - Export to file

---

## Complete Workflows

### Workflow 1: Daily Production Deployment

```python
#!/usr/bin/env python3
from deployment import DeploymentManager
from backup_enhanced import BackupManager
from log_rotation import LogRotationManager
from shell_automation import ShellCommandExecutor

app_root = '/var/www/production'

# 1. Run tests
print("Step 1: Running tests...")
executor = ShellCommandExecutor()
ret_code, _, _ = executor.execute_command_with_retry(
    'cd /app && make test',
    max_retries=2,
    retry_delay=10
)

if ret_code != 0:
    print("✗ Tests failed - aborting deployment")
    exit(1)

# 2. Backup current deployment
print("Step 2: Backing up current deployment...")
deployer = DeploymentManager(app_root)
deployer.backup_current_deployment('pre-deployment')

# 3. Deploy new version
print("Step 3: Deploying new version...")
if deployer.deploy_files('/tmp/release'):
    # 4. Verify deployment
    print("Step 4: Verifying deployment...")
    if deployer.verify_deployment(['app.py', 'requirements.txt']):
        print("✓ Deployment successful!")
        
        # 5. Rotate logs
        print("Step 5: Rotating logs...")
        logs = LogRotationManager('/var/log/app')
        logs.rotate_all_logs()
        
        # 6. Cleanup
        print("Step 6: Cleanup...")
        deployer.cleanup_old_deployments(keep_count=5)
        logs.cleanup_old_backups()
    else:
        print("✗ Verification failed - rolling back")
        deployer.rollback()
else:
    print("✗ Deployment failed - rolling back")
    deployer.rollback()
```

### Workflow 2: Automated Backup & Cleanup

```python
#!/usr/bin/env python3
from backup_enhanced import BackupManager
from file_cleanup import FileCleanupManager
from shell_automation import ShellCommandExecutor

# 1. Backup databases
print("Step 1: Backing up databases...")
executor = ShellCommandExecutor()
executor.execute_command('mysqldump -u root -p database > /backup/db.sql')

# 2. Backup application files
print("Step 2: Backing up application files...")
backup_mgr = BackupManager('/var/www', '/backup')
backup_dir = backup_mgr.perform_full_backup()
backup_mgr.verify_backup(backup_dir)
backup_mgr.compress_backup(backup_dir)

# 3. Cleanup temp files
print("Step 3: Cleaning temporary files...")
cleanup = FileCleanupManager('/var/www')
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()
cleanup.cleanup_empty_directories()

# 4. Cleanup old backups
print("Step 4: Cleaning old backups...")
backup_mgr.cleanup_old_backups(retention_days=30, keep_min=5)

# 5. Report
print("Step 5: Generating report...")
cleanup.generate_cleanup_report()
backup_mgr.list_backups()

print("✓ Backup and cleanup complete!")
```

### Workflow 3: System Maintenance Task

```python
#!/usr/bin/env python3
from log_rotation import LogRotationManager
from file_cleanup import FileCleanupManager
from shell_automation import ShellCommandExecutor

# 1. Rotate application logs
print("Rotating application logs...")
app_logs = LogRotationManager('/var/log/app')
app_logs.rotate_all_logs()
app_logs.compress_old_backups()
app_logs.cleanup_old_backups()

# 2. Rotate system logs
print("Rotating system logs...")
sys_logs = LogRotationManager('/var/log')
sys_logs.rotate_all_logs()

# 3. Cleanup cache
print("Cleaning cache files...")
cleanup = FileCleanupManager('/tmp')
cleanup.set_dry_run(False)
cleanup.cleanup_old_files(age_days=7)
cleanup.cleanup_temp_files()

# 4. Cleanup old downloads
print("Cleaning downloads...")
cleanup = FileCleanupManager('/home/user/Downloads')
cleanup.cleanup_old_files(age_days=30)

# 5. Execute maintenance scripts
print("Running maintenance scripts...")
executor = ShellCommandExecutor()
executor.parallel_commands([
    'apt-get update',
    'apt-get upgrade -y',
    'apt-get autoclean'
])

print("✓ System maintenance complete!")
```

---

## Advanced Features

### Error Handling
```python
from deployment import DeploymentManager

deployer = DeploymentManager('/app')

try:
    deployer.deploy_files('/tmp/release')
except Exception as e:
    print(f"Deployment failed: {e}")
    deployer.rollback()
```

### Dry-Run Mode
```python
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager('/tmp')

# Test what would be deleted
cleanup.set_dry_run(True)
cleanup.cleanup_old_files(age_days=30)

# Actually delete
cleanup.set_dry_run(False)
cleanup.cleanup_old_files(age_days=30)
```

### Custom Logging
All modules log to both console and log files. Check:
- Deployment: `.deployments/deployment.log`
- Backup: `backup_root/backup.log`
- Cleanup: `cleanup_root/cleanup.log`
- Logs: `log_dir/rotation.log`
- Shell: `work_dir/commands.log`

---

## Configuration Files

### Log Rotation Configuration Example
```ini
# Log Rotation Configuration
max_file_size = 10485760  # 10 MB in bytes
max_files = 10
retention_days = 30
backup_dir = /var/log/backups
```

---

## Requirements

- Python 3.6+
- No external dependencies (uses only os, datetime, time, subprocess)
- Linux/Unix system (or Windows with proper path handling)

---

## Performance Notes

- **Full Backup**: O(n) where n = total files
- **Incremental Backup**: O(m) where m = changed files
- **File Cleanup**: O(n) filesystem walk
- **Log Rotation**: O(n) for file processing
- **Shell Execution**: Varies by command complexity

---

## Security Considerations

1. File permissions are preserved during operations
2. Backups include manifest for integrity checking
3. Log files are created with restricted permissions (0o755)
4. Sensitive data should be encrypted separately
5. Review deployment files before rollback

---

## Troubleshooting

### Deployment fails
1. Check `check_system_resources()` output
2. Verify source directory exists
3. Check file permissions
4. Review `.deployments/deployment.log`

### Backup fails
1. Verify disk space with `df -h`
2. Check directory permissions
3. Review `backup.log` for errors
4. Ensure restore target exists

### Cleanup too aggressive
1. Use `set_dry_run(True)` first
2. Adjust age_days parameter
3. Check `cleanup.log` for warnings

### Log rotation stuck
1. Check backup directory permissions
2. Verify max_file_size is reasonable
3. Review `rotation.log` for errors
4. Check available disk space

---

## Interactive Hub

Run the interactive menu:
```bash
python3 devops_hub.py
```

This provides guided access to all modules and examples.

---

## License

MIT License - Free to use and modify

## Support

For issues or questions, check the module docstrings:
```python
from deployment import DeploymentManager
help(DeploymentManager)
```
