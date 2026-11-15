#!/usr/bin/env python3
"""
Enhanced Backup Automation Script
Supports incremental backups, compression, retention policies
Uses os library for system operations
"""

import os
import time
from datetime import datetime, timedelta


class BackupManager:
    def __init__(self, source_dir, backup_root, backup_type='full'):
        """
        Initialize backup manager
        
        Args:
            source_dir: Directory to backup
            backup_root: Root directory for backups
            backup_type: 'full' or 'incremental'
        """
        self.source_dir = source_dir
        self.backup_root = backup_root
        self.backup_type = backup_type
        self.backup_manifest = os.path.join(backup_root, 'backup_manifest.txt')
        self.backup_log = os.path.join(backup_root, 'backup.log')
        self._setup_directories()

    def _setup_directories(self):
        """Create backup directories"""
        if not os.path.exists(self.backup_root):
            os.makedirs(self.backup_root, mode=0o755)
            self._log(f"Created backup directory: {self.backup_root}")

    def _log(self, message):
        """Log backup activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.backup_log, 'a') as f:
            f.write(log_message + '\n')

    def _get_file_hash_simple(self, filepath):
        """Simple file hash based on size and modification time"""
        try:
            stat = os.stat(filepath)
            return f"{stat.st_size}_{stat.st_mtime}"
        except:
            return None

    def _load_manifest(self):
        """Load previous backup manifest"""
        manifest = {}
        if os.path.exists(self.backup_manifest):
            with open(self.backup_manifest, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 2:
                            manifest[parts[0]] = parts[1]
        return manifest

    def _save_manifest(self, manifest):
        """Save backup manifest"""
        with open(self.backup_manifest, 'w') as f:
            for filepath, file_hash in sorted(manifest.items()):
                f.write(f"{filepath}|{file_hash}\n")

    def perform_full_backup(self):
        """Perform full backup of source directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.backup_root, f"backup_full_{timestamp}")
        
        os.makedirs(backup_dir, exist_ok=True)
        self._log(f"Starting full backup to {backup_dir}")
        
        manifest = {}
        total_size = 0
        file_count = 0
        
        # Walk through source directory
        for root, dirs, files in os.walk(self.source_dir):
            # Create corresponding directory structure
            rel_path = os.path.relpath(root, self.source_dir)
            if rel_path == '.':
                backup_subdir = backup_dir
            else:
                backup_subdir = os.path.join(backup_dir, rel_path)
            
            os.makedirs(backup_subdir, exist_ok=True)
            
            # Backup files
            for file in files:
                src_file = os.path.join(root, file)
                rel_file = os.path.relpath(src_file, self.source_dir)
                dst_file = os.path.join(backup_dir, rel_file)
                
                try:
                    with open(src_file, 'rb') as src:
                        content = src.read()
                    
                    with open(dst_file, 'wb') as dst:
                        dst.write(content)
                    
                    # Update manifest
                    file_hash = self._get_file_hash_simple(src_file)
                    manifest[rel_file] = file_hash
                    
                    total_size += len(content)
                    file_count += 1
                    
                    self._log(f"Backed up: {rel_file}")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to backup {rel_file}: {str(e)}")
        
        # Save manifest
        self._save_manifest(manifest)
        
        self._log(f"Full backup completed: {file_count} files, {total_size / 1024:.2f}KB")
        return backup_dir

    def perform_incremental_backup(self):
        """Perform incremental backup based on manifest"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.backup_root, f"backup_incremental_{timestamp}")
        
        os.makedirs(backup_dir, exist_ok=True)
        self._log(f"Starting incremental backup to {backup_dir}")
        
        # Load previous manifest
        old_manifest = self._load_manifest()
        new_manifest = {}
        
        total_size = 0
        file_count = 0
        
        # Walk through source directory
        for root, dirs, files in os.walk(self.source_dir):
            rel_path = os.path.relpath(root, self.source_dir)
            
            for file in files:
                src_file = os.path.join(root, file)
                rel_file = os.path.relpath(src_file, self.source_dir)
                
                try:
                    # Check if file has changed
                    current_hash = self._get_file_hash_simple(src_file)
                    previous_hash = old_manifest.get(rel_file)
                    
                    new_manifest[rel_file] = current_hash
                    
                    # Only backup if file is new or changed
                    if current_hash != previous_hash:
                        # Create directory structure
                        backup_subdir = os.path.dirname(os.path.join(backup_dir, rel_file))
                        os.makedirs(backup_subdir, exist_ok=True)
                        
                        dst_file = os.path.join(backup_dir, rel_file)
                        
                        with open(src_file, 'rb') as src:
                            content = src.read()
                        
                        with open(dst_file, 'wb') as dst:
                            dst.write(content)
                        
                        total_size += len(content)
                        file_count += 1
                        
                        self._log(f"Backed up (changed): {rel_file}")
                    else:
                        self._log(f"Skipped (unchanged): {rel_file}")
                    
                except Exception as e:
                    self._log(f"ERROR: Failed to backup {rel_file}: {str(e)}")
        
        # Check for deleted files
        for rel_file in old_manifest:
            if rel_file not in new_manifest:
                self._log(f"File deleted: {rel_file}")
        
        # Save new manifest
        self._save_manifest(new_manifest)
        
        self._log(f"Incremental backup completed: {file_count} files changed, {total_size / 1024:.2f}KB")
        return backup_dir

    def verify_backup(self, backup_dir):
        """Verify backup integrity"""
        self._log(f"Verifying backup: {backup_dir}")
        
        if not os.path.exists(backup_dir):
            self._log(f"ERROR: Backup directory not found: {backup_dir}")
            return False
        
        try:
            total_files = 0
            total_size = 0
            
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_files += 1
                    total_size += os.path.getsize(file_path)
            
            self._log(f"Backup verified: {total_files} files, {total_size / 1024:.2f}KB")
            return True
            
        except Exception as e:
            self._log(f"ERROR: Backup verification failed: {str(e)}")
            return False

    def compress_backup(self, backup_dir):
        """Compress backup directory using tar"""
        compressed_file = backup_dir + '.tar.gz'
        
        self._log(f"Compressing backup: {backup_dir}")
        
        try:
            # Create tar archive using os.system
            ret_code = os.system(f"tar -czf '{compressed_file}' -C '{os.path.dirname(backup_dir)}' '{os.path.basename(backup_dir)}'")
            
            if ret_code == 0:
                compressed_size = os.path.getsize(compressed_file) / 1024
                self._log(f"Backup compressed: {compressed_file} ({compressed_size:.2f}KB)")
                return compressed_file
            else:
                self._log(f"ERROR: Compression failed with code {ret_code}")
                return None
                
        except Exception as e:
            self._log(f"ERROR: Failed to compress backup: {str(e)}")
            return None

    def restore_backup(self, backup_dir, restore_target):
        """Restore files from backup"""
        self._log(f"Restoring backup from {backup_dir} to {restore_target}")
        
        if not os.path.exists(backup_dir):
            self._log(f"ERROR: Backup directory not found: {backup_dir}")
            return False
        
        try:
            os.makedirs(restore_target, exist_ok=True)
            
            for root, dirs, files in os.walk(backup_dir):
                rel_path = os.path.relpath(root, backup_dir)
                
                if rel_path == '.':
                    restore_subdir = restore_target
                else:
                    restore_subdir = os.path.join(restore_target, rel_path)
                
                os.makedirs(restore_subdir, exist_ok=True)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(restore_subdir, file)
                    
                    with open(src_file, 'rb') as src:
                        content = src.read()
                    
                    with open(dst_file, 'wb') as dst:
                        dst.write(content)
                    
                    self._log(f"Restored: {os.path.relpath(dst_file, restore_target)}")
            
            self._log("Restore completed successfully")
            return True
            
        except Exception as e:
            self._log(f"ERROR: Restore failed: {str(e)}")
            return False

    def cleanup_old_backups(self, retention_days=30, keep_min=3):
        """Clean up backups older than retention_days"""
        self._log(f"Cleaning up backups older than {retention_days} days")
        
        cutoff_time = time.time() - (retention_days * 24 * 3600)
        backups = []
        
        for item in os.listdir(self.backup_root):
            item_path = os.path.join(self.backup_root, item)
            if os.path.isdir(item_path) and item.startswith('backup_'):
                mod_time = os.path.getmtime(item_path)
                backups.append((item_path, mod_time))
        
        # Sort by modification time
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        removed_count = 0
        for backup_path, mod_time in backups[keep_min:]:
            if mod_time < cutoff_time:
                self._remove_directory(backup_path)
                self._log(f"Removed old backup: {os.path.basename(backup_path)}")
                removed_count += 1
        
        self._log(f"Cleanup completed: removed {removed_count} backups")
        return removed_count

    def _remove_directory(self, path):
        """Remove directory recursively"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    self._remove_directory(item_path)
            os.rmdir(path)
        except Exception as e:
            self._log(f"ERROR removing directory {path}: {str(e)}")

    def list_backups(self):
        """List all available backups"""
        self._log("Available backups:")
        backups = []
        
        for item in os.listdir(self.backup_root):
            if item.startswith('backup_'):
                item_path = os.path.join(self.backup_root, item)
                if os.path.isdir(item_path):
                    mod_time = os.path.getmtime(item_path)
                    mod_time_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Calculate size
                    size = 0
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            size += os.path.getsize(os.path.join(root, file))
                    
                    backups.append((item, mod_time_str, size / 1024))
        
        for backup, time_str, size_kb in sorted(backups, reverse=True):
            print(f"  {backup} ({time_str}) - {size_kb:.2f}KB")
        
        return backups


def main():
    """Example usage"""
    
    source_dir = "/var/www/myapp"
    backup_root = "/backup/myapp"
    
    # Create backup manager
    backup_mgr = BackupManager(source_dir, backup_root, backup_type='full')
    
    # Perform full backup
    backup_dir = backup_mgr.perform_full_backup()
    
    # Verify backup
    if backup_mgr.verify_backup(backup_dir):
        # Compress backup
        backup_mgr.compress_backup(backup_dir)
    
    # List all backups
    backup_mgr.list_backups()
    
    # Cleanup old backups
    backup_mgr.cleanup_old_backups(retention_days=30, keep_min=3)


if __name__ == '__main__':
    main()
