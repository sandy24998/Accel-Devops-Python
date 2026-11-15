#!/usr/bin/env python3
"""
Deployment Script - Handles application deployment with rollback capability
Uses os library for system operations
"""

import os
import sys
import time
from datetime import datetime


class DeploymentManager:
    def __init__(self, app_root, backup_dir=None):
        """Initialize deployment manager"""
        self.app_root = app_root
        self.backup_dir = backup_dir or os.path.join(app_root, '.deployments')
        self.deployment_log = os.path.join(self.backup_dir, 'deployment.log')
        self.current_version_file = os.path.join(self.backup_dir, 'current_version.txt')
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary directories"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, mode=0o755)
            self._log(f"Created backup directory: {self.backup_dir}")

    def _log(self, message):
        """Log deployment activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        # Print to console
        print(log_message)
        
        # Write to log file
        with open(self.deployment_log, 'a') as f:
            f.write(log_message + '\n')

    def check_system_resources(self):
        """Check system resources before deployment"""
        self._log("Checking system resources...")
        
        # Check disk space
        stat = os.statvfs(self.app_root)
        free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
        
        if free_space_gb < 1:
            self._log(f"WARNING: Low disk space - {free_space_gb:.2f}GB available")
            return False
        
        self._log(f"Disk space available: {free_space_gb:.2f}GB")
        return True

    def backup_current_deployment(self, version_name=None):
        """Backup current deployment before deploying new version"""
        if version_name is None:
            version_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_path = os.path.join(self.backup_dir, f"backup_{version_name}")
        
        self._log(f"Backing up current deployment to {backup_path}")
        
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy app files
        for item in os.listdir(self.app_root):
            src = os.path.join(self.app_root, item)
            dst = os.path.join(backup_path, item)
            
            # Skip backup directory and log directory
            if item in ['.deployments', 'logs']:
                continue
            
            if os.path.isfile(src):
                with open(src, 'rb') as src_file:
                    content = src_file.read()
                with open(dst, 'wb') as dst_file:
                    dst_file.write(content)
                self._log(f"Backed up file: {item}")
        
        self._log(f"Backup completed: {backup_path}")
        return backup_path

    def deploy_files(self, source_dir, file_list=None):
        """Deploy files from source directory"""
        self._log(f"Starting deployment from {source_dir}")
        
        if not os.path.exists(source_dir):
            self._log(f"ERROR: Source directory not found: {source_dir}")
            return False
        
        try:
            if file_list:
                # Deploy specific files
                for file_name in file_list:
                    src = os.path.join(source_dir, file_name)
                    dst = os.path.join(self.app_root, file_name)
                    
                    if os.path.exists(src):
                        with open(src, 'rb') as src_file:
                            content = src_file.read()
                        with open(dst, 'wb') as dst_file:
                            dst_file.write(content)
                        self._log(f"Deployed: {file_name}")
                    else:
                        self._log(f"WARNING: File not found in source: {file_name}")
            else:
                # Deploy all files
                for item in os.listdir(source_dir):
                    src = os.path.join(source_dir, item)
                    dst = os.path.join(self.app_root, item)
                    
                    if os.path.isfile(src):
                        with open(src, 'rb') as src_file:
                            content = src_file.read()
                        with open(dst, 'wb') as dst_file:
                            dst_file.write(content)
                        self._log(f"Deployed: {item}")
            
            self._log("Deployment completed successfully")
            return True
            
        except Exception as e:
            self._log(f"ERROR during deployment: {str(e)}")
            return False

    def verify_deployment(self, expected_files):
        """Verify deployment was successful"""
        self._log("Verifying deployment...")
        
        all_present = True
        for file_name in expected_files:
            file_path = os.path.join(self.app_root, file_name)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                self._log(f"Verified: {file_name} ({file_size} bytes)")
            else:
                self._log(f"ERROR: Required file missing: {file_name}")
                all_present = False
        
        return all_present

    def rollback(self, backup_version=None):
        """Rollback to previous deployment"""
        if backup_version is None:
            # Find latest backup
            backups = []
            for item in os.listdir(self.backup_dir):
                if item.startswith('backup_'):
                    backups.append(item)
            
            if not backups:
                self._log("ERROR: No backups available for rollback")
                return False
            
            backup_version = sorted(backups)[-1]
        
        backup_path = os.path.join(self.backup_dir, backup_version)
        
        self._log(f"Rolling back to {backup_version}")
        
        if not os.path.exists(backup_path):
            self._log(f"ERROR: Backup not found: {backup_path}")
            return False
        
        try:
            # Restore files from backup
            for item in os.listdir(backup_path):
                src = os.path.join(backup_path, item)
                dst = os.path.join(self.app_root, item)
                
                if os.path.isfile(src):
                    with open(src, 'rb') as src_file:
                        content = src_file.read()
                    with open(dst, 'wb') as dst_file:
                        dst_file.write(content)
                    self._log(f"Restored: {item}")
            
            self._log("Rollback completed successfully")
            return True
            
        except Exception as e:
            self._log(f"ERROR during rollback: {str(e)}")
            return False

    def list_deployments(self):
        """List all deployment backups"""
        self._log("Available deployments:")
        backups = []
        for item in os.listdir(self.backup_dir):
            if item.startswith('backup_'):
                backup_path = os.path.join(self.backup_dir, item)
                mod_time = os.path.getmtime(backup_path)
                mod_time_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
                backups.append((item, mod_time_str))
        
        for backup, time_str in sorted(backups):
            print(f"  {backup} ({time_str})")
        
        return backups

    def cleanup_old_deployments(self, keep_count=5):
        """Clean up old deployment backups"""
        self._log(f"Cleaning up old deployments (keeping {keep_count})")
        
        backups = []
        for item in os.listdir(self.backup_dir):
            if item.startswith('backup_'):
                backup_path = os.path.join(self.backup_dir, item)
                mod_time = os.path.getmtime(backup_path)
                backups.append((backup_path, mod_time))
        
        # Sort by modification time
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        for backup_path, _ in backups[keep_count:]:
            self._remove_directory(backup_path)
            self._log(f"Removed old backup: {os.path.basename(backup_path)}")

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


def main():
    """Example usage of DeploymentManager"""
    
    # Initialize deployment manager
    app_root = "/var/www/myapp"
    deployer = DeploymentManager(app_root)
    
    # Check resources
    if not deployer.check_system_resources():
        print("Deployment cancelled due to insufficient resources")
        sys.exit(1)
    
    # Backup current deployment
    deployer.backup_current_deployment()
    
    # Deploy new files
    source_dir = "/tmp/release"
    if deployer.deploy_files(source_dir):
        # Verify deployment
        expected_files = ['app.py', 'config.yaml', 'requirements.txt']
        if deployer.verify_deployment(expected_files):
            print("Deployment successful!")
        else:
            print("Deployment verification failed, rolling back...")
            deployer.rollback()
    else:
        print("Deployment failed!")
    
    # List all deployments
    deployer.list_deployments()
    
    # Cleanup old deployments
    deployer.cleanup_old_deployments(keep_count=3)


if __name__ == '__main__':
    main()
