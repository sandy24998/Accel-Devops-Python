#!/usr/bin/env python3
"""
Shell Command Automation Script
Execute, schedule, and manage system commands
Uses os library for system operations
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta


class ShellCommandExecutor:
    def __init__(self, work_dir=None, log_file=None):
        """Initialize command executor"""
        self.work_dir = work_dir or os.getcwd()
        self.log_file = log_file or os.path.join(self.work_dir, 'commands.log')
        self.command_history = []

    def _log(self, message, level="INFO"):
        """Log command activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        print(log_message)
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_message + '\n')
        except:
            pass

    def execute_command(self, command, capture_output=False, check_return=True):
        """
        Execute a shell command
        
        Args:
            command: Command string to execute
            capture_output: If True, capture stdout/stderr
            check_return: If True, raise error on non-zero return code
        
        Returns:
            (return_code, stdout, stderr)
        """
        self._log(f"Executing: {command}")
        
        try:
            if capture_output:
                # Execute with output capture
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.work_dir,
                    capture_output=True,
                    text=True
                )
                
                stdout = result.stdout
                stderr = result.stderr
                return_code = result.returncode
            else:
                # Execute with output to console
                return_code = os.system(f"cd {self.work_dir} && {command}")
                stdout = ""
                stderr = ""
            
            # Store in history
            self.command_history.append({
                'command': command,
                'return_code': return_code,
                'timestamp': datetime.now(),
                'stdout': stdout,
                'stderr': stderr
            })
            
            if return_code != 0:
                self._log(f"Command failed with return code: {return_code}", level="ERROR")
                if stderr:
                    self._log(f"Error: {stderr}", level="ERROR")
            else:
                self._log(f"Command completed successfully")
                if stdout:
                    self._log(f"Output: {stdout}")
            
            return return_code, stdout, stderr
            
        except Exception as e:
            self._log(f"ERROR: Failed to execute command: {str(e)}", level="ERROR")
            return 1, "", str(e)

    def execute_command_batch(self, commands, stop_on_error=False):
        """
        Execute multiple commands in sequence
        
        Args:
            commands: List of command strings
            stop_on_error: If True, stop on first error
        
        Returns:
            List of (return_code, stdout, stderr)
        """
        self._log(f"Executing batch of {len(commands)} commands")
        
        results = []
        
        for i, command in enumerate(commands, 1):
            self._log(f"Batch command {i}/{len(commands)}")
            ret_code, stdout, stderr = self.execute_command(command, capture_output=True)
            results.append((ret_code, stdout, stderr))
            
            if stop_on_error and ret_code != 0:
                self._log(f"Stopping batch execution due to error in command {i}")
                break
        
        self._log(f"Batch execution complete: {len(results)}/{len(commands)} completed")
        return results

    def execute_command_with_retry(self, command, max_retries=3, retry_delay=5):
        """
        Execute command with retry on failure
        
        Args:
            command: Command to execute
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
        
        Returns:
            (return_code, stdout, stderr)
        """
        self._log(f"Executing with retry (max {max_retries} retries): {command}")
        
        for attempt in range(1, max_retries + 1):
            self._log(f"Attempt {attempt}/{max_retries}")
            
            ret_code, stdout, stderr = self.execute_command(command, capture_output=True)
            
            if ret_code == 0:
                self._log(f"Command succeeded on attempt {attempt}")
                return ret_code, stdout, stderr
            
            if attempt < max_retries:
                self._log(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
        self._log(f"Command failed after {max_retries} attempts", level="ERROR")
        return ret_code, stdout, stderr

    def execute_if_condition(self, condition_cmd, true_cmd, false_cmd=None):
        """
        Execute command conditionally based on result of condition command
        
        Args:
            condition_cmd: Command that determines condition
            true_cmd: Command to execute if condition is true (return code 0)
            false_cmd: Command to execute if condition is false
        
        Returns:
            Results of executed command
        """
        self._log(f"Evaluating condition: {condition_cmd}")
        
        ret_code, _, _ = self.execute_command(condition_cmd, capture_output=True)
        
        if ret_code == 0:
            self._log("Condition is true, executing true command")
            return self.execute_command(true_cmd, capture_output=True)
        else:
            if false_cmd:
                self._log("Condition is false, executing false command")
                return self.execute_command(false_cmd, capture_output=True)
            else:
                self._log("Condition is false, no false command specified")
                return ret_code, "", ""

    def execute_parallel_commands(self, commands):
        """
        Execute multiple commands in parallel
        
        Args:
            commands: List of command strings
        
        Returns:
            List of (return_code, stdout, stderr)
        """
        self._log(f"Executing {len(commands)} commands in parallel")
        
        # Create background processes
        processes = []
        
        for command in commands:
            self._log(f"Starting parallel command: {command}")
            
            try:
                # Create subprocess
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=self.work_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                processes.append((command, proc))
            except Exception as e:
                self._log(f"ERROR: Failed to start command: {str(e)}", level="ERROR")
        
        # Wait for all processes
        results = []
        for command, proc in processes:
            stdout, stderr = proc.communicate()
            return_code = proc.returncode
            results.append((return_code, stdout, stderr))
            
            if return_code != 0:
                self._log(f"Parallel command failed: {command}", level="ERROR")
            else:
                self._log(f"Parallel command completed: {command}")
        
        self._log(f"All parallel commands completed")
        return results

    def pipe_commands(self, commands):
        """
        Execute commands with piping (cmd1 | cmd2 | cmd3)
        
        Args:
            commands: List of command strings
        
        Returns:
            (return_code, final_output)
        """
        self._log(f"Piping {len(commands)} commands")
        
        pipe_cmd = " | ".join(commands)
        self._log(f"Full command: {pipe_cmd}")
        
        return self.execute_command(pipe_cmd, capture_output=True)

    def execute_script_file(self, script_path):
        """Execute a shell script file"""
        self._log(f"Executing script: {script_path}")
        
        if not os.path.exists(script_path):
            self._log(f"ERROR: Script file not found: {script_path}", level="ERROR")
            return 1, "", "Script not found"
        
        # Make script executable
        os.chmod(script_path, 0o755)
        
        return self.execute_command(script_path, capture_output=True)

    def create_script_file(self, script_path, commands):
        """
        Create a shell script file
        
        Args:
            script_path: Path to create script
            commands: List of command strings
        """
        self._log(f"Creating script: {script_path}")
        
        try:
            with open(script_path, 'w') as f:
                f.write("#!/bin/bash\n\n")
                f.write("# Auto-generated script\n")
                f.write(f"# Created: {datetime.now()}\n\n")
                
                for command in commands:
                    f.write(f"{command}\n")
            
            os.chmod(script_path, 0o755)
            self._log(f"Script created: {script_path}")
            return True
            
        except Exception as e:
            self._log(f"ERROR: Failed to create script: {str(e)}", level="ERROR")
            return False

    def get_command_history(self, limit=10):
        """Get command history"""
        return self.command_history[-limit:]

    def print_command_history(self):
        """Print command execution history"""
        print("\n=== Command History ===\n")
        
        for i, entry in enumerate(self.command_history[-20:], 1):
            timestamp = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            status = "OK" if entry['return_code'] == 0 else "FAIL"
            print(f"{i}. [{timestamp}] [{status}] {entry['command']}")
        
        print()

    def export_history(self, output_file):
        """Export command history to file"""
        self._log(f"Exporting command history to {output_file}")
        
        try:
            with open(output_file, 'w') as f:
                f.write("=== Command History Export ===\n")
                f.write(f"Exported: {datetime.now()}\n")
                f.write(f"Total commands: {len(self.command_history)}\n\n")
                
                for i, entry in enumerate(self.command_history, 1):
                    f.write(f"\n--- Command {i} ---\n")
                    f.write(f"Timestamp: {entry['timestamp']}\n")
                    f.write(f"Command: {entry['command']}\n")
                    f.write(f"Return Code: {entry['return_code']}\n")
                    if entry['stdout']:
                        f.write(f"Stdout: {entry['stdout']}\n")
                    if entry['stderr']:
                        f.write(f"Stderr: {entry['stderr']}\n")
            
            self._log(f"History exported successfully")
            return True
            
        except Exception as e:
            self._log(f"ERROR: Failed to export history: {str(e)}", level="ERROR")
            return False


def main():
    """Example usage"""
    
    executor = ShellCommandExecutor(work_dir="/tmp")
    
    # Execute single command
    print("\n=== Single Command ===")
    executor.execute_command("ls -la")
    
    # Execute batch commands
    print("\n=== Batch Commands ===")
    batch_commands = [
        "echo 'Creating test file'",
        "touch test.txt",
        "ls -l test.txt",
        "rm test.txt"
    ]
    executor.execute_command_batch(batch_commands)
    
    # Execute with retry
    print("\n=== Command with Retry ===")
    executor.execute_command_with_retry("pwd", max_retries=2, retry_delay=1)
    
    # Pipe commands
    print("\n=== Piped Commands ===")
    executor.pipe_commands(["echo 'hello world'", "wc -w"])
    
    # Conditional execution
    print("\n=== Conditional Execution ===")
    executor.execute_if_condition(
        "test -f /etc/passwd",
        "echo 'Passwd file exists'",
        "echo 'Passwd file not found'"
    )
    
    # Print history
    executor.print_command_history()
    
    # Export history
    executor.export_history("/tmp/command_history.txt")


if __name__ == '__main__':
    main()
