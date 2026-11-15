#!/usr/bin/env python3
"""
Log Rotation Script
Manages log file rotation, compression, and archival
Uses os library for system operations
"""

import os
import time
from datetime import datetime, timedelta


class LogRotationManager:
    def __init__(self, log_dir, config=None):
        """
        Initialize log rotation manager
        
        Args:
            log_dir: Directory containing log files
            config: Dict with rotation config
        """
        self.log_dir = log_dir
        self.config = config or {
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'max_files': 10,
            'retention_days': 30,
            'backup_dir': os.path.join(log_dir, 'backups')
        }
        self.rotation_log = os.path.join(log_dir, 'rotation.log')
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary directories"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, mode=0o755)
        
        if not os.path.exists(self.config['backup_dir']):
            os.makedirs(self.config['backup_dir'], mode=0o755)

    def _log(self, message):
        """Log rotation activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.rotation_log, 'a') as f:
            f.write(log_message + '\n')

    def rotate_log_file(self, log_file_path):
        """
        Rotate a single log file if it exceeds max size
        
        Args:
            log_file_path: Path to log file to check
        """
        if not os.path.exists(log_file_path):
            self._log(f"Log file not found: {log_file_path}")
            return False
        
        try:
            file_size = os.path.getsize(log_file_path)
            max_size = self.config['max_file_size']
            
            if file_size > max_size:
                self._log(f"Rotating log file: {log_file_path} (size: {file_size / 1024:.2f}KB)")
                
                # Create backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(log_file_path)
                backup_name = f"{base_name}.{timestamp}"
                backup_path = os.path.join(self.config['backup_dir'], backup_name)
                
                # Copy current log to backup
                with open(log_file_path, 'rb') as src:
                    content = src.read()
                
                with open(backup_path, 'wb') as dst:
                    dst.write(content)
                
                self._log(f"Created backup: {backup_name}")
                
                # Truncate original log file
                with open(log_file_path, 'w') as f:
                    f.write('')
                
                self._log(f"Truncated: {os.path.basename(log_file_path)}")
                
                return True
            else:
                return False
                
        except Exception as e:
            self._log(f"ERROR: Failed to rotate {log_file_path}: {str(e)}")
            return False

    def rotate_all_logs(self, pattern=None):
        """Rotate all log files matching pattern"""
        self._log("Starting rotation of all log files")
        
        rotated_count = 0
        
        for file in os.listdir(self.log_dir):
            if file.endswith('.log') or file.endswith('.txt'):
                # Skip rotation log itself
                if file == 'rotation.log':
                    continue
                
                # Check pattern if specified
                if pattern and pattern not in file:
                    continue
                
                log_file_path = os.path.join(self.log_dir, file)
                
                if os.path.isfile(log_file_path):
                    if self.rotate_log_file(log_file_path):
                        rotated_count += 1
        
        self._log(f"Log rotation complete: {rotated_count} files rotated")
        return rotated_count

    def compress_old_backups(self):
        """Compress backup log files"""
        self._log("Compressing old backup log files")
        
        backup_dir = self.config['backup_dir']
        compressed_count = 0
        freed_space = 0
        
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            
            if os.path.isfile(file_path) and not file.endswith('.gz'):
                try:
                    # Compress using gzip
                    ret_code = os.system(f"gzip '{file_path}'")
                    
                    if ret_code == 0:
                        original_size = os.path.getsize(file_path + '.gz')
                        compressed_count += 1
                        self._log(f"Compressed: {file} -> {file}.gz")
                    else:
                        self._log(f"WARNING: Failed to compress {file}")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to compress {file_path}: {str(e)}")
        
        self._log(f"Compression complete: {compressed_count} files compressed")
        return compressed_count

    def cleanup_old_backups(self):
        """Remove backup files older than retention days"""
        self._log(f"Cleaning up backups older than {self.config['retention_days']} days")
        
        cutoff_time = time.time() - (self.config['retention_days'] * 24 * 3600)
        backup_dir = self.config['backup_dir']
        removed_count = 0
        freed_space = 0
        
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                
                if mod_time < cutoff_time:
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        freed_space += file_size
                        removed_count += 1
                        self._log(f"Deleted old backup: {file} ({file_size / 1024:.2f}KB)")
                    except Exception as e:
                        self._log(f"ERROR: Failed to delete {file_path}: {str(e)}")
        
        self._log(f"Cleanup complete: removed {removed_count} files, freed {freed_space / 1024:.2f}KB")
        return removed_count, freed_space

    def limit_backup_count(self):
        """Limit number of backup files"""
        self._log(f"Limiting backup count to {self.config['max_files']}")
        
        backup_dir = self.config['backup_dir']
        backups = []
        
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                backups.append((file_path, mod_time))
        
        # Sort by modification time (oldest first)
        backups.sort(key=lambda x: x[1])
        
        # Remove oldest files if count exceeds max
        removed_count = 0
        if len(backups) > self.config['max_files']:
            for file_path, _ in backups[:len(backups) - self.config['max_files']]:
                try:
                    os.remove(file_path)
                    removed_count += 1
                    self._log(f"Removed oldest backup: {os.path.basename(file_path)}")
                except Exception as e:
                    self._log(f"ERROR: Failed to remove {file_path}: {str(e)}")
        
        self._log(f"Backup count limit applied: removed {removed_count} files")
        return removed_count

    def analyze_log_sizes(self):
        """Analyze log file sizes"""
        self._log("Analyzing log file sizes")
        
        total_size = 0
        log_files = []
        
        # Analyze active logs
        for file in os.listdir(self.log_dir):
            if file.endswith('.log') or file.endswith('.txt'):
                if file == 'rotation.log':
                    continue
                
                file_path = os.path.join(self.log_dir, file)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    log_files.append((file, file_size))
        
        # Analyze backups
        backup_dir = self.config['backup_dir']
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                total_size += file_size
                log_files.append((f"backup/{file}", file_size))
        
        print("\n=== Log File Analysis ===")
        print(f"Total log size: {total_size / 1024 / 1024:.2f}MB\n")
        print("Files:")
        
        for filename, size in sorted(log_files, key=lambda x: x[1], reverse=True):
            print(f"  {filename}: {size / 1024:.2f}KB")
        
        return total_size, log_files

    def get_rotation_stats(self):
        """Get rotation statistics"""
        self._log("Calculating rotation statistics")
        
        stats = {
            'total_backups': 0,
            'total_backup_size': 0,
            'oldest_backup': None,
            'newest_backup': None
        }
        
        backup_dir = self.config['backup_dir']
        backups = []
        
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)
                
                stats['total_backups'] += 1
                stats['total_backup_size'] += file_size
                
                backups.append((file, mod_time))
        
        if backups:
            backups.sort(key=lambda x: x[1])
            stats['oldest_backup'] = datetime.fromtimestamp(backups[0][1]).strftime("%Y-%m-%d %H:%M:%S")
            stats['newest_backup'] = datetime.fromtimestamp(backups[-1][1]).strftime("%Y-%m-%d %H:%M:%S")
        
        return stats

    def create_config_file(self, config_file_path):
        """Create a configuration file"""
        config_content = f"""# Log Rotation Configuration

# Maximum log file size before rotation (in bytes)
# Default: 10 MB
max_file_size = {self.config['max_file_size']}

# Maximum number of backup files to keep
# Default: 10
max_files = {self.config['max_files']}

# Retention period for backups (in days)
# Default: 30
retention_days = {self.config['retention_days']}

# Backup directory
# Default: {self.config['backup_dir']}
backup_dir = {self.config['backup_dir']}
"""
        
        try:
            with open(config_file_path, 'w') as f:
                f.write(config_content)
            self._log(f"Created config file: {config_file_path}")
            return True
        except Exception as e:
            self._log(f"ERROR: Failed to create config file: {str(e)}")
            return False


def main():
    """Example usage"""
    
    log_dir = "/var/log/myapp"
    
    # Create rotation manager
    rotation_mgr = LogRotationManager(log_dir)
    
    # Rotate logs
    rotation_mgr.rotate_all_logs()
    
    # Compress old backups
    rotation_mgr.compress_old_backups()
    
    # Cleanup old backups
    rotation_mgr.cleanup_old_backups()
    
    # Limit backup count
    rotation_mgr.limit_backup_count()
    
    # Analyze log sizes
    rotation_mgr.analyze_log_sizes()
    
    # Get statistics
    stats = rotation_mgr.get_rotation_stats()
    print(f"\nRotation Stats: {stats}")


if __name__ == '__main__':
    main()
