# DevOps Automation Suite
# Requirements and Dependencies

## Python Version
python>=3.6

## External Dependencies
# NONE - This suite uses only the Python standard library!
# No pip packages required.

## Standard Library Modules Used
# (Built-in with Python, no installation needed)

os              # File and directory operations
sys             # System operations
time            # Time utilities
datetime        # Date and time handling
subprocess      # Execute shell commands
glob            # File pattern matching (optional)

## Optional System Tools
# These are used via shell commands, not Python imports
# Already available on most Linux systems:

tar             # File compression/archiving
gzip            # Compression
git             # Version control
make            # Build automation
docker          # Container operations (if using shell_automation)
kubectl         # Kubernetes operations (if using shell_automation)

## Installation Instructions

### Option 1: No Installation Needed
# The suite works directly with Python stdlib!
cd /path/to/Accel-Devops-Python
python3 deployment.py

### Option 2: Add to Python Path
export PYTHONPATH=$PYTHONPATH:/path/to/Accel-Devops-Python
python3 -c "from deployment import DeploymentManager; print('Ready')"

### Option 3: Create Symbolic Links
sudo ln -s /path/to/deployment.py /usr/local/bin/deploy
sudo chmod +x /usr/local/bin/deploy
deploy  # Run directly

### Option 4: Virtual Environment (Recommended)
python3 -m venv devops_env
source devops_env/bin/activate
# No pip install needed - just use the modules!

## Verification

# Verify Python version
python3 --version

# Verify all modules can be imported
python3 -c "
from deployment import DeploymentManager
from backup_enhanced import BackupManager
from file_cleanup import FileCleanupManager
from log_rotation import LogRotationManager
from shell_automation import ShellCommandExecutor
print('✓ All modules imported successfully!')
"

# Test basic functionality
python3 examples.py

## System Requirements (not Python packages)

- Linux/Unix system
- Python 3.6+
- Standard Unix tools: tar, gzip
- Sufficient disk space for backups
- File permissions to access source/target directories

## Why No External Dependencies?

✓ Minimal dependencies = more secure
✓ No version conflicts to manage
✓ Faster deployment and startup
✓ Works on any Python 3.6+ installation
✓ Lightweight and portable
✓ Easy to deploy to production servers

## Optional Performance Enhancements

For better performance with large operations:
- Consider installing: PyYAML (for config files)
- Use: paramiko (for remote operations)
- Try: click (for better CLI interface)

But these are completely optional!

## Troubleshooting

If you get "ModuleNotFoundError":
1. Ensure you're in the correct directory
2. Check Python version (python3 --version)
3. Verify PYTHONPATH if set manually
4. All modules use only standard library - no install needed

## Size & Performance

- Total suite size: ~150KB (5 Python files)
- Memory usage: <50MB typical operation
- Startup time: <1 second
- No build/compilation needed
- Works on any Python 3.6+ installation
