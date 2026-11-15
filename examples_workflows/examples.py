#!/usr/bin/env python3
"""
Practical Examples - Real-world usage scenarios
Demonstrates how to use the DevOps suite in production environments
"""

import os
import sys
from datetime import datetime, timedelta


# ============================================================================
# EXAMPLE 1: Daily Production Deployment Pipeline
# ============================================================================

def example_production_deployment():
    """
    Complete production deployment with:
    - Pre-deployment checks
    - Backup of current version
    - New version deployment
    - Verification and rollback on failure
    - Cleanup of old deployments
    """
    from deployment import DeploymentManager
    from shell_automation import ShellCommandExecutor
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Production Deployment Pipeline")
    print("="*60)
    
    # Configuration
    app_root = "/var/www/production"
    release_dir = "/tmp/release/v2.0.0"
    
    # Initialize
    deployer = DeploymentManager(app_root)
    executor = ShellCommandExecutor(work_dir=app_root)
    
    # Step 1: Pre-deployment checks
    print("\n[1/6] Checking system resources...")
    if not deployer.check_system_resources():
        print("ERROR: Insufficient resources")
        return False
    
    # Step 2: Run smoke tests
    print("\n[2/6] Running smoke tests...")
    ret_code, _, _ = executor.execute_command_with_retry(
        "python3 -m pytest tests/ --co",
        max_retries=1
    )
    if ret_code != 0:
        print("ERROR: Smoke tests failed")
        return False
    
    # Step 3: Backup current deployment
    print("\n[3/6] Backing up current deployment...")
    backup_path = deployer.backup_current_deployment('pre-2.0.0')
    print(f"✓ Backup created: {backup_path}")
    
    # Step 4: Deploy new version
    print("\n[4/6] Deploying new version...")
    if not deployer.deploy_files(release_dir):
        print("ERROR: Deployment failed")
        deployer.rollback()
        return False
    
    # Step 5: Verify deployment
    print("\n[5/6] Verifying deployment...")
    required_files = ['app.py', 'requirements.txt', 'config.yaml']
    if not deployer.verify_deployment(required_files):
        print("ERROR: Verification failed - rolling back")
        deployer.rollback()
        return False
    
    # Step 6: Cleanup and report
    print("\n[6/6] Cleanup...")
    deployer.cleanup_old_deployments(keep_count=5)
    deployer.list_deployments()
    
    print("\n✓ Production deployment completed successfully!")
    return True


# ============================================================================
# EXAMPLE 2: Automated Nightly Backup and Maintenance
# ============================================================================

def example_nightly_backup_maintenance():
    """
    Complete nightly maintenance:
    - Database backup
    - Application backup (full)
    - Log rotation
    - Cleanup old files and backups
    - Generate report
    """
    from backup_enhanced import BackupManager
    from log_rotation import LogRotationManager
    from file_cleanup import FileCleanupManager
    from shell_automation import ShellCommandExecutor
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Nightly Backup & Maintenance")
    print("="*60)
    
    # Configuration
    app_root = "/var/www/myapp"
    backup_root = "/backup/myapp"
    log_dir = "/var/log/myapp"
    
    # Initialize
    backup_mgr = BackupManager(app_root, backup_root)
    log_mgr = LogRotationManager(log_dir)
    file_cleanup = FileCleanupManager(app_root)
    executor = ShellCommandExecutor()
    
    # Step 1: Backup database
    print("\n[1/5] Backing up database...")
    executor.execute_command(
        "mysqldump -u root myapp > /backup/myapp.sql 2>/dev/null"
    )
    print("✓ Database backed up")
    
    # Step 2: Backup application files
    print("\n[2/5] Backing up application files...")
    backup_dir = backup_mgr.perform_full_backup()
    if backup_mgr.verify_backup(backup_dir):
        compressed = backup_mgr.compress_backup(backup_dir)
        print(f"✓ Backup verified and compressed")
    
    # Step 3: Rotate logs
    print("\n[3/5] Rotating logs...")
    log_mgr.rotate_all_logs()
    log_mgr.compress_old_backups()
    print("✓ Logs rotated and compressed")
    
    # Step 4: Cleanup old files
    print("\n[4/5] Cleaning up old files...")
    file_cleanup.set_dry_run(False)
    old_count, freed = file_cleanup.cleanup_old_files(age_days=30)
    temp_count, freed_temp = file_cleanup.cleanup_temp_files()
    empty_count = file_cleanup.cleanup_empty_directories()
    
    print(f"✓ Removed {old_count} old files ({freed/1024/1024:.2f}MB)")
    print(f"✓ Removed {temp_count} temp files ({freed_temp/1024/1024:.2f}MB)")
    print(f"✓ Removed {empty_count} empty directories")
    
    # Step 5: Cleanup old backups
    print("\n[5/5] Cleaning old backups...")
    backup_mgr.cleanup_old_backups(retention_days=30, keep_min=5)
    log_mgr.cleanup_old_backups(retention_days=30)
    log_mgr.limit_backup_count()
    
    # Generate report
    print("\n--- Backup Report ---")
    backup_mgr.list_backups()
    
    print("\n--- Log Rotation Stats ---")
    stats = log_mgr.get_rotation_stats()
    print(f"Total backups: {stats['total_backups']}")
    print(f"Total size: {stats['total_backup_size']/1024/1024:.2f}MB")
    
    print("\n✓ Nightly maintenance completed successfully!")
    return True


# ============================================================================
# EXAMPLE 3: Safe File Cleanup with Dry-Run and Analysis
# ============================================================================

def example_safe_cleanup_with_analysis():
    """
    Safe file cleanup process:
    - Generate cleanup report
    - Find large and duplicate files
    - Use dry-run to preview
    - Execute actual cleanup
    """
    from file_cleanup import FileCleanupManager
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Safe File Cleanup with Analysis")
    print("="*60)
    
    cleanup_root = "/var/log"
    
    cleanup = FileCleanupManager(cleanup_root)
    
    # Step 1: Analyze
    print("\n[1/4] Analyzing directory...")
    report = cleanup.generate_cleanup_report()
    print(report)
    
    # Step 2: Find large files
    print("\n[2/4] Finding large files (>50MB)...")
    large_files = cleanup.cleanup_large_files(min_size_mb=50)
    for file, size in large_files[:10]:
        print(f"  {file}: {size/1024/1024:.2f}MB")
    
    # Step 3: Find duplicates
    print("\n[3/4] Finding duplicate files...")
    duplicates = cleanup.cleanup_duplicate_files()
    if duplicates:
        for dup in duplicates[:5]:
            print(f"  Duplicate: {dup}")
    else:
        print("  No duplicates found")
    
    # Step 4: Dry-run cleanup
    print("\n[4/4] Dry-run cleanup (no files deleted)...")
    cleanup.set_dry_run(True)
    
    print("  Scanning for old files (>30 days)...")
    cleanup.cleanup_old_files(age_days=30)
    
    print("  Scanning for temp files...")
    cleanup.cleanup_temp_files()
    
    print("\n✓ Cleanup analysis complete (files NOT deleted)")
    print("  To actually delete files, call with set_dry_run(False)")
    return True


# ============================================================================
# EXAMPLE 4: Log Rotation with Monitoring
# ============================================================================

def example_log_rotation_with_monitoring():
    """
    Log rotation with monitoring:
    - Configure custom rotation settings
    - Rotate logs
    - Monitor log sizes
    - Cleanup and compress
    - Get statistics
    """
    from log_rotation import LogRotationManager
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Log Rotation with Monitoring")
    print("="*60)
    
    log_dir = "/var/log/myapp"
    
    # Custom configuration
    config = {
        'max_file_size': 100 * 1024 * 1024,  # 100MB
        'max_files': 15,
        'retention_days': 60,
        'backup_dir': os.path.join(log_dir, 'backups')
    }
    
    logs = LogRotationManager(log_dir, config)
    
    # Step 1: Analyze current state
    print("\n[1/5] Analyzing current log state...")
    total_size, log_files = logs.analyze_log_sizes()
    print(f"Total log size: {total_size/1024/1024:.2f}MB")
    print(f"Log files: {len(log_files)}")
    
    # Step 2: Rotate logs
    print("\n[2/5] Rotating logs...")
    logs.rotate_all_logs()
    
    # Step 3: Compress backups
    print("\n[3/5] Compressing old backups...")
    compressed_count = logs.compress_old_backups()
    print(f"Compressed {compressed_count} backup files")
    
    # Step 4: Cleanup old backups
    print("\n[4/5] Cleaning up old backups...")
    removed, freed = logs.cleanup_old_backups()
    print(f"Removed {removed} files, freed {freed/1024/1024:.2f}MB")
    
    # Step 5: Enforce limits
    print("\n[5/5] Enforcing backup limits...")
    logs.limit_backup_count()
    
    # Report
    print("\n--- Statistics ---")
    stats = logs.get_rotation_stats()
    print(f"Oldest backup: {stats['oldest_backup']}")
    print(f"Newest backup: {stats['newest_backup']}")
    print(f"Total backups: {stats['total_backups']}")
    print(f"Total backup size: {stats['total_backup_size']/1024/1024:.2f}MB")
    
    print("\n✓ Log rotation completed successfully!")
    return True


# ============================================================================
# EXAMPLE 5: Complex Shell Command Automation
# ============================================================================

def example_complex_shell_automation():
    """
    Complex shell automation:
    - Sequential command execution with error handling
    - Parallel execution of independent tasks
    - Piped commands
    - Conditional execution
    - Retry logic
    """
    from shell_automation import ShellCommandExecutor
    
    print("\n" + "="*60)
    print("EXAMPLE 5: Complex Shell Command Automation")
    print("="*60)
    
    executor = ShellCommandExecutor(work_dir="/tmp")
    
    # Step 1: Sequential commands
    print("\n[1/4] Sequential command execution...")
    commands = [
        "echo 'Creating test environment...'",
        "mkdir -p test_app",
        "cd test_app && echo 'test' > file.txt",
        "ls -la test_app"
    ]
    results = executor.execute_command_batch(commands, stop_on_error=True)
    print(f"✓ Executed {len(results)} commands")
    
    # Step 2: Retry logic
    print("\n[2/4] Command with retry logic...")
    ret_code, _, _ = executor.execute_command_with_retry(
        "test -f test_app/file.txt && echo 'File found'",
        max_retries=2,
        retry_delay=1
    )
    if ret_code == 0:
        print("✓ Command succeeded")
    
    # Step 3: Conditional execution
    print("\n[3/4] Conditional execution...")
    executor.execute_if_condition(
        "test -d test_app",
        "echo 'Directory exists'",
        "echo 'Directory not found'"
    )
    
    # Step 4: Piped commands
    print("\n[4/4] Piped commands...")
    executor.pipe_commands([
        "echo -e 'line1\\nline2\\nline3'",
        "sort -r"
    ])
    
    # Show history
    print("\n--- Command History ---")
    executor.print_command_history()
    
    print("\n✓ Shell automation examples completed!")
    return True


# ============================================================================
# EXAMPLE 6: Complete CI/CD Pipeline Simulation
# ============================================================================

def example_cicd_pipeline():
    """
    Simulate a complete CI/CD pipeline:
    - Build and test
    - Backup production
    - Deploy to staging
    - Verify deployment
    - Promote to production
    - Cleanup and report
    """
    from deployment import DeploymentManager
    from backup_enhanced import BackupManager
    from shell_automation import ShellCommandExecutor
    
    print("\n" + "="*60)
    print("EXAMPLE 6: CI/CD Pipeline Simulation")
    print("="*60)
    
    # Configuration
    source_repo = "/tmp/myapp"
    staging_root = "/var/www/staging"
    production_root = "/var/www/production"
    backup_root = "/backup"
    
    executor = ShellCommandExecutor()
    
    # Step 1: Build
    print("\n[1/7] Building application...")
    executor.execute_command(f"cd {source_repo} && make build")
    
    # Step 2: Test
    print("\n[2/7] Running tests...")
    ret_code, _, _ = executor.execute_command(
        f"cd {source_repo} && make test",
        capture_output=True
    )
    if ret_code != 0:
        print("✗ Tests failed - stopping pipeline")
        return False
    
    # Step 3: Deploy to staging
    print("\n[3/7] Deploying to staging...")
    staging_deployer = DeploymentManager(staging_root)
    staging_deployer.deploy_files(source_repo)
    
    # Step 4: Smoke test on staging
    print("\n[4/7] Smoke testing on staging...")
    executor.execute_command(f"curl -f http://localhost:8000/health || exit 1")
    
    # Step 5: Backup production
    print("\n[5/7] Backing up production...")
    prod_backup = BackupManager(production_root, backup_root)
    backup_dir = prod_backup.perform_full_backup()
    prod_backup.verify_backup(backup_dir)
    
    # Step 6: Deploy to production
    print("\n[6/7] Deploying to production...")
    prod_deployer = DeploymentManager(production_root)
    prod_deployer.backup_current_deployment('pre-production-deploy')
    prod_deployer.deploy_files(source_repo)
    
    # Step 7: Verify and report
    print("\n[7/7] Verifying production deployment...")
    if prod_deployer.verify_deployment(['app.py', 'requirements.txt']):
        print("✓ Production deployment successful!")
        prod_deployer.list_deployments()
    else:
        print("✗ Production verification failed - rolling back")
        prod_deployer.rollback()
        return False
    
    print("\n✓ CI/CD pipeline completed successfully!")
    return True


# ============================================================================
# EXAMPLE 7: Disaster Recovery Scenario
# ============================================================================

def example_disaster_recovery():
    """
    Disaster recovery scenario:
    - List available backups
    - Restore from backup
    - Verify restored data
    - Update systems
    """
    from backup_enhanced import BackupManager
    
    print("\n" + "="*60)
    print("EXAMPLE 7: Disaster Recovery Scenario")
    print("="*60)
    
    app_root = "/var/www/production"
    backup_root = "/backup/production"
    restore_temp = "/tmp/restore"
    
    backup_mgr = BackupManager(app_root, backup_root)
    
    # Step 1: List available backups
    print("\n[1/4] Available backups...")
    backups = backup_mgr.list_backups()
    
    if not backups:
        print("✗ No backups available!")
        return False
    
    # Step 2: Restore from latest backup
    print("\n[2/4] Restoring from latest backup...")
    latest_backup = sorted(backups)[0][0]
    restore_path = os.path.join(backup_root, latest_backup)
    
    backup_mgr.restore_backup(restore_path, restore_temp)
    print(f"✓ Data restored to {restore_temp}")
    
    # Step 3: Verify restored data
    print("\n[3/4] Verifying restored data...")
    if backup_mgr.verify_backup(restore_temp):
        print("✓ Restore verification passed")
    else:
        print("✗ Restore verification failed")
    
    # Step 4: Options
    print("\n[4/4] Recovery options:")
    print("  1. Replace production with restored data")
    print("  2. Restore to alternate location")
    print("  3. Partial restore (specific files)")
    
    print("\n✓ Disaster recovery process demonstrated!")
    return True


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Run all examples"""
    
    examples = [
        ("Production Deployment Pipeline", example_production_deployment),
        ("Nightly Backup & Maintenance", example_nightly_backup_maintenance),
        ("Safe Cleanup with Analysis", example_safe_cleanup_with_analysis),
        ("Log Rotation with Monitoring", example_log_rotation_with_monitoring),
        ("Complex Shell Automation", example_complex_shell_automation),
        ("CI/CD Pipeline Simulation", example_cicd_pipeline),
        ("Disaster Recovery Scenario", example_disaster_recovery),
    ]
    
    print("\n" + "="*60)
    print("DevOps Suite - Practical Examples")
    print("="*60)
    print("\nAvailable Examples:\n")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"  [{i}] {name}")
    
    print(f"  [0] Exit")
    print("\nNote: These are demonstration examples.")
    print("Modify paths and parameters for your environment.\n")
    
    while True:
        try:
            choice = input("Select example (0-7): ").strip()
            
            if choice == '0':
                print("Exiting...")
                break
            
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(examples):
                name, func = examples[choice_num]
                print(f"\nRunning: {name}")
                
                try:
                    func()
                except Exception as e:
                    print(f"\n✗ Example error: {str(e)}")
            else:
                print("Invalid choice")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
