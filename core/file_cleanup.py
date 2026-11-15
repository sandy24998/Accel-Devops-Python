#!/usr/bin/env python3
"""
File Cleanup Script
Removes old files, empty directories, temporary files, duplicates
Uses os library for system operations
"""

import os
import time
from datetime import datetime, timedelta


class FileCleanupManager:
    def __init__(self, cleanup_root, log_file=None):
        """Initialize file cleanup manager"""
        self.cleanup_root = cleanup_root
        self.log_file = log_file or os.path.join(cleanup_root, 'cleanup.log')
        self.dry_run = False

    def _log(self, message):
        """Log cleanup activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')

    def cleanup_old_files(self, age_days=30, file_pattern=None):
        """Remove files older than specified days"""
        self._log(f"Starting cleanup of files older than {age_days} days")
        
        cutoff_time = time.time() - (age_days * 24 * 3600)
        removed_count = 0
        freed_space = 0
        
        for root, dirs, files in os.walk(self.cleanup_root):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check file pattern if specified
                if file_pattern and not file.endswith(file_pattern):
                    continue
                
                try:
                    mod_time = os.path.getmtime(file_path)
                    
                    if mod_time < cutoff_time:
                        file_size = os.path.getsize(file_path)
                        
                        if not self.dry_run:
                            os.remove(file_path)
                        
                        freed_space += file_size
                        removed_count += 1
                        
                        rel_path = os.path.relpath(file_path, self.cleanup_root)
                        self._log(f"Removed old file: {rel_path} ({file_size} bytes)")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to remove {file_path}: {str(e)}")
        
        self._log(f"Cleanup complete: removed {removed_count} files, freed {freed_space / 1024:.2f}KB")
        return removed_count, freed_space

    def cleanup_empty_directories(self):
        """Remove empty directories"""
        self._log("Starting cleanup of empty directories")
        
        removed_count = 0
        
        # Process directories bottom-up
        for root, dirs, files in os.walk(self.cleanup_root, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                
                try:
                    # Check if directory is empty
                    if len(os.listdir(dir_path)) == 0:
                        if not self.dry_run:
                            os.rmdir(dir_path)
                        
                        removed_count += 1
                        rel_path = os.path.relpath(dir_path, self.cleanup_root)
                        self._log(f"Removed empty directory: {rel_path}")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to remove directory {dir_path}: {str(e)}")
        
        self._log(f"Empty directory cleanup complete: removed {removed_count} directories")
        return removed_count

    def cleanup_temp_files(self):
        """Remove temporary files"""
        self._log("Starting cleanup of temporary files")
        
        temp_extensions = ['.tmp', '.temp', '.log', '.bak', '.swp', '.swo', '~']
        removed_count = 0
        freed_space = 0
        
        for root, dirs, files in os.walk(self.cleanup_root):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if file has temp extension
                should_remove = False
                for ext in temp_extensions:
                    if file.endswith(ext):
                        should_remove = True
                        break
                
                if should_remove:
                    try:
                        file_size = os.path.getsize(file_path)
                        
                        if not self.dry_run:
                            os.remove(file_path)
                        
                        freed_space += file_size
                        removed_count += 1
                        
                        rel_path = os.path.relpath(file_path, self.cleanup_root)
                        self._log(f"Removed temp file: {rel_path} ({file_size} bytes)")
                        
                    except Exception as e:
                        self._log(f"ERROR: Failed to remove {file_path}: {str(e)}")
        
        self._log(f"Temp file cleanup complete: removed {removed_count} files, freed {freed_space / 1024:.2f}KB")
        return removed_count, freed_space

    def cleanup_large_files(self, min_size_mb=100):
        """List and optionally remove large files"""
        self._log(f"Starting scan for files larger than {min_size_mb}MB")
        
        min_size = min_size_mb * 1024 * 1024
        large_files = []
        
        for root, dirs, files in os.walk(self.cleanup_root):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    file_size = os.path.getsize(file_path)
                    
                    if file_size > min_size:
                        rel_path = os.path.relpath(file_path, self.cleanup_root)
                        large_files.append((rel_path, file_size))
                        self._log(f"Large file found: {rel_path} ({file_size / 1024 / 1024:.2f}MB)")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to check {file_path}: {str(e)}")
        
        return large_files

    def cleanup_duplicate_files(self):
        """Find and optionally remove duplicate files based on size and first 1KB"""
        self._log("Starting scan for duplicate files")
        
        file_hashes = {}
        duplicates = []
        
        for root, dirs, files in os.walk(self.cleanup_root):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    file_size = os.path.getsize(file_path)
                    
                    # Get first 1KB of file
                    try:
                        with open(file_path, 'rb') as f:
                            first_kb = f.read(1024)
                    except:
                        first_kb = b''
                    
                    # Create simple hash
                    file_hash = f"{file_size}_{len(first_kb)}"
                    
                    if file_hash in file_hashes:
                        duplicates.append((file_path, file_hash))
                        rel_path = os.path.relpath(file_path, self.cleanup_root)
                        self._log(f"Duplicate found: {rel_path}")
                    else:
                        file_hashes[file_hash] = file_path
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to check {file_path}: {str(e)}")
        
        return duplicates

    def cleanup_by_pattern(self, pattern, remove=False):
        """Cleanup files matching specific pattern"""
        self._log(f"Cleanup files matching pattern: {pattern}")
        
        removed_count = 0
        freed_space = 0
        
        for root, dirs, files in os.walk(self.cleanup_root):
            for file in files:
                if pattern in file or file.endswith(pattern):
                    file_path = os.path.join(root, file)
                    
                    try:
                        file_size = os.path.getsize(file_path)
                        
                        if remove and not self.dry_run:
                            os.remove(file_path)
                            self._log(f"Removed: {os.path.relpath(file_path, self.cleanup_root)}")
                        else:
                            self._log(f"Found: {os.path.relpath(file_path, self.cleanup_root)} ({file_size} bytes)")
                        
                        freed_space += file_size
                        removed_count += 1
                        
                    except Exception as e:
                        self._log(f"ERROR: Failed to process {file_path}: {str(e)}")
        
        return removed_count, freed_space

    def generate_cleanup_report(self):
        """Generate a report of the cleanup root"""
        self._log("Generating cleanup report")
        
        total_files = 0
        total_size = 0
        total_dirs = 0
        file_by_type = {}
        
        for root, dirs, files in os.walk(self.cleanup_root):
            total_dirs += len(dirs)
            
            for file in files:
                file_path = os.path.join(root, file)
                total_files += 1
                
                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    # Count by extension
                    _, ext = os.path.splitext(file)
                    if ext:
                        file_by_type[ext] = file_by_type.get(ext, 0) + 1
                    else:
                        file_by_type['[no extension]'] = file_by_type.get('[no extension]', 0) + 1
                    
                except:
                    pass
        
        report = f"""
=== Cleanup Report ===
Path: {self.cleanup_root}
Total Files: {total_files}
Total Directories: {total_dirs}
Total Size: {total_size / 1024 / 1024:.2f}MB

Files by Type:
"""
        for ext, count in sorted(file_by_type.items(), key=lambda x: x[1], reverse=True):
            report += f"  {ext}: {count}\n"
        
        self._log(report)
        return report

    def set_dry_run(self, enabled=True):
        """Enable/disable dry run mode"""
        self.dry_run = enabled
        if enabled:
            self._log("DRY RUN MODE ENABLED - No files will be deleted")
        else:
            self._log("DRY RUN MODE DISABLED - Files will be deleted")


def main():
    """Example usage"""
    
    cleanup_root = "/var/www/temp"
    cleanup_mgr = FileCleanupManager(cleanup_root)
    
    # Enable dry run first to see what would be deleted
    cleanup_mgr.set_dry_run(enabled=True)
    
    # Remove files older than 30 days
    cleanup_mgr.cleanup_old_files(age_days=30)
    
    # Remove temp files
    cleanup_mgr.cleanup_temp_files()
    
    # Remove empty directories
    cleanup_mgr.cleanup_empty_directories()
    
    # Find large files
    large_files = cleanup_mgr.cleanup_large_files(min_size_mb=100)
    
    # Find duplicates
    duplicates = cleanup_mgr.cleanup_duplicate_files()
    
    # Generate report
    cleanup_mgr.generate_cleanup_report()


if __name__ == '__main__':
    main()
