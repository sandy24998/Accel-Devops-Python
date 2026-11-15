"""
DevOps Automation Suite - Core Modules

Production-ready modules for:
- deployment.py: Application deployment with rollback
- backup_enhanced.py: Backup management and restoration
- file_cleanup.py: File and directory cleanup
- log_rotation.py: Log file rotation and management
- shell_automation.py: Advanced shell command execution
"""

from .deployment import DeploymentManager
from .backup_enhanced import BackupManager
from .file_cleanup import FileCleanupManager
from .log_rotation import LogRotationManager
from .shell_automation import ShellCommandExecutor

__version__ = "1.0"
__all__ = [
    "DeploymentManager",
    "BackupManager",
    "FileCleanupManager",
    "LogRotationManager",
    "ShellCommandExecutor",
]
