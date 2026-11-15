#!/usr/bin/env python3
"""
DevOps Utilities Hub
Unified interface for all deployment, backup, cleanup, log rotation, and shell automation
Uses os library for system operations
"""

import os
import sys
from datetime import datetime


class DevOpsHub:
    """Central hub for all DevOps operations"""
    
    def __init__(self, config_dir=None):
        """Initialize DevOps Hub"""
        self.config_dir = config_dir or os.path.expanduser("~/.devops_config")
        self.setup_dir = os.path.dirname(os.path.abspath(__file__))
        self._setup_config()
    
    def _setup_config(self):
        """Setup configuration directory"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, mode=0o755)
            print(f"Created config directory: {self.config_dir}")
    
    def show_menu(self):
        """Display main menu"""
        print("""
╔════════════════════════════════════════════════════╗
║          DevOps Automation Hub                      ║
║          (Using OS Library Only)                    ║
╚════════════════════════════════════════════════════╝

Available Modules:

  [1] Deployment Scripts       - deployment.py
      - Full/incremental deployment
      - Backup and rollback capability
      - Resource verification
      - Deployment versioning

  [2] Backup Automation        - backup_enhanced.py
      - Full and incremental backups
      - Backup verification
      - Compression support
      - Retention policies
      - Restore capability

  [3] File Cleanup             - file_cleanup.py
      - Remove old files
      - Clean empty directories
      - Temp file cleanup
      - Duplicate detection
      - Large file analysis

  [4] Log Rotation             - log_rotation.py
      - Automatic log rotation
      - Size-based rotation
      - Backup compression
      - Retention management
      - Log analysis

  [5] Shell Automation         - shell_automation.py
      - Execute shell commands
      - Batch execution
      - Parallel execution
      - Command retry logic
      - Command history

  [6] Quick Start Guide
  [7] Show Examples
  [0] Exit

Select an option (0-7):
        """)
    
    def show_quick_guide(self):
        """Show quick start guide"""
        guide = """
╔════════════════════════════════════════════════════╗
║          Quick Start Guide                         ║
╚════════════════════════════════════════════════════╝

1. DEPLOYMENT:
   >>> from deployment import DeploymentManager
   >>> deployer = DeploymentManager('/app')
   >>> deployer.backup_current_deployment()
   >>> deployer.deploy_files('/tmp/release')
   >>> deployer.verify_deployment(['app.py', 'config.yaml'])
   >>> deployer.rollback()  # If needed

2. BACKUP:
   >>> from backup_enhanced import BackupManager
   >>> backup = BackupManager('/var/www', '/backup')
   >>> backup.perform_full_backup()
   >>> backup.verify_backup(backup_dir)
   >>> backup.compress_backup(backup_dir)
   >>> backup.cleanup_old_backups(retention_days=30)

3. FILE CLEANUP:
   >>> from file_cleanup import FileCleanupManager
   >>> cleanup = FileCleanupManager('/tmp')
   >>> cleanup.cleanup_old_files(age_days=30)
   >>> cleanup.cleanup_temp_files()
   >>> cleanup.cleanup_empty_directories()

4. LOG ROTATION:
   >>> from log_rotation import LogRotationManager
   >>> logs = LogRotationManager('/var/log/app')
   >>> logs.rotate_all_logs()
   >>> logs.compress_old_backups()
   >>> logs.cleanup_old_backups()

5. SHELL AUTOMATION:
   >>> from shell_automation import ShellCommandExecutor
   >>> executor = ShellCommandExecutor()
   >>> executor.execute_command('ls -la')
   >>> executor.execute_command_batch(['cmd1', 'cmd2'])
   >>> executor.execute_command_with_retry('unstable_cmd')
        """
        print(guide)
    
    def show_examples(self):
        """Show detailed examples"""
        examples = """
╔════════════════════════════════════════════════════╗
║          Usage Examples                            ║
╚════════════════════════════════════════════════════╝

EXAMPLE 1: Daily Deployment with Backup and Verification
───────────────────────────────────────────────────────
from deployment import DeploymentManager

deployer = DeploymentManager('/var/www/myapp')

# Check resources before deployment
if not deployer.check_system_resources():
    exit(1)

# Backup current version
deployer.backup_current_deployment('v1.0.0')

# Deploy new version
if deployer.deploy_files('/tmp/release/v2.0.0'):
    # Verify deployment
    if deployer.verify_deployment(['app.py', 'requirements.txt']):
        print("✓ Deployment successful!")
    else:
        print("✗ Verification failed, rolling back...")
        deployer.rollback()

# Clean old deployments
deployer.cleanup_old_deployments(keep_count=5)


EXAMPLE 2: Automated Backup with Cleanup
────────────────────────────────────────
from backup_enhanced import BackupManager

backup_mgr = BackupManager('/var/www', '/backup/myapp')

# Full backup
backup_dir = backup_mgr.perform_full_backup()

# Verify and compress
if backup_mgr.verify_backup(backup_dir):
    backup_mgr.compress_backup(backup_dir)

# Cleanup old backups (keep 7 most recent)
backup_mgr.cleanup_old_backups(retention_days=30, keep_min=7)

# List current backups
backup_mgr.list_backups()


EXAMPLE 3: Complete Cleanup Operation
──────────────────────────────────────
from file_cleanup import FileCleanupManager

cleanup = FileCleanupManager('/var/log')

# Enable dry-run first
cleanup.set_dry_run(enabled=True)

# See what would be deleted
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()

# Actually clean
cleanup.set_dry_run(enabled=False)
cleanup.cleanup_old_files(age_days=30)
cleanup.cleanup_temp_files()
cleanup.cleanup_empty_directories()

# Report
cleanup.generate_cleanup_report()


EXAMPLE 4: Log Rotation Automation
─────────────────────────────────
from log_rotation import LogRotationManager

config = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'max_files': 10,
    'retention_days': 60,
    'backup_dir': '/var/log/backups'
}

logs = LogRotationManager('/var/log/myapp', config)

# Check and rotate if needed
logs.rotate_all_logs()

# Compress old backups
logs.compress_old_backups()

# Cleanup old backups
logs.cleanup_old_backups()

# Limit backup count
logs.limit_backup_count()

# Show stats
stats = logs.get_rotation_stats()
print(f"Total backups: {stats['total_backups']}")


EXAMPLE 5: Complex Shell Automation
────────────────────────────────────
from shell_automation import ShellCommandExecutor

executor = ShellCommandExecutor(work_dir='/app')

# Execute with retry
executor.execute_command_with_retry(
    'make deploy',
    max_retries=3,
    retry_delay=5
)

# Batch execution with error handling
commands = [
    'docker build -t myapp:latest .',
    'docker push myapp:latest',
    'kubectl apply -f deployment.yaml'
]
executor.execute_command_batch(commands, stop_on_error=True)

# Parallel execution
parallel_tasks = [
    'npm run build',
    'npm run test',
    'npm run lint'
]
executor.execute_parallel_commands(parallel_tasks)

# Piped commands
executor.pipe_commands([
    'find . -name "*.log"',
    'xargs wc -l',
    'sort -n'
])

# Conditional execution
executor.execute_if_condition(
    'test -f config.yaml',
    'echo "Config exists"',
    'echo "Config missing - copying default"'
)


EXAMPLE 6: End-to-End DevOps Workflow
─────────────────────────────────────
from deployment import DeploymentManager
from backup_enhanced import BackupManager
from log_rotation import LogRotationManager
from shell_automation import ShellCommandExecutor

# 1. Run tests
executor = ShellCommandExecutor('/app')
ret_code, _, _ = executor.execute_command_with_retry(
    'make test',
    max_retries=2
)

if ret_code == 0:
    # 2. Backup current
    backup_mgr = BackupManager('/var/www', '/backup')
    backup_dir = backup_mgr.perform_full_backup()
    
    # 3. Deploy new version
    deployer = DeploymentManager('/var/www')
    deployer.deploy_files('/tmp/release')
    
    # 4. Rotate logs
    logs = LogRotationManager('/var/log/app')
    logs.rotate_all_logs()
    
    print("✓ Complete workflow executed successfully!")
else:
    print("✗ Tests failed - deployment cancelled")
        """
        print(examples)


def main():
    """Main interactive menu"""
    hub = DevOpsHub()
    
    while True:
        hub.show_menu()
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '0':
                print("Exiting...")
                break
            elif choice == '1':
                print("\n✓ Deployment Scripts Module (deployment.py)")
                print("  Use: from deployment import DeploymentManager")
            elif choice == '2':
                print("\n✓ Backup Automation Module (backup_enhanced.py)")
                print("  Use: from backup_enhanced import BackupManager")
            elif choice == '3':
                print("\n✓ File Cleanup Module (file_cleanup.py)")
                print("  Use: from file_cleanup import FileCleanupManager")
            elif choice == '4':
                print("\n✓ Log Rotation Module (log_rotation.py)")
                print("  Use: from log_rotation import LogRotationManager")
            elif choice == '5':
                print("\n✓ Shell Automation Module (shell_automation.py)")
                print("  Use: from shell_automation import ShellCommandExecutor")
            elif choice == '6':
                hub.show_quick_guide()
            elif choice == '7':
                hub.show_examples()
            else:
                print("Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
