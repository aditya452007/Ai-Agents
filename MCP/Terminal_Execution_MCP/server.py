#!/usr/bin/env python3
"""
Multi-Shell MCP Server
Provides command execution capabilities for CMD, PowerShell, WSL/Ubuntu, and Git Bash
"""

import asyncio
import subprocess
import sys
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import json

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


class ShellExecutor:
    """Handles execution of commands across different shell environments"""
    
    def __init__(self):
        self.default_timeout = 30
        self.git_bash_path = self._find_git_bash()
    
    def _find_git_bash(self) -> Optional[str]:
        """Locate Git Bash installation"""
        common_paths = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\bash.exe")
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # Try to find via PATH
        git_bash = shutil.which("bash")
        if git_bash and "git" in git_bash.lower():
            return git_bash
        
        return None
    
    async def execute_cmd(
        self, 
        command: str, 
        working_dir: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute command in Windows CMD"""
        try:
            timeout_val = timeout or self.default_timeout
            
            process = await asyncio.create_subprocess_exec(
                "cmd.exe",
                "/c",
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_val
            )
            
            return {
                "success": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "shell": "CMD"
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Command timed out after {timeout_val} seconds",
                "shell": "CMD"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "shell": "CMD"
            }
    
    async def execute_powershell(
        self,
        command: str,
        working_dir: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute command in PowerShell"""
        try:
            timeout_val = timeout or self.default_timeout
            
            # Use -NoProfile for faster startup and -NonInteractive for automation
            process = await asyncio.create_subprocess_exec(
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_val
            )
            
            return {
                "success": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "shell": "PowerShell"
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Command timed out after {timeout_val} seconds",
                "shell": "PowerShell"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "shell": "PowerShell"
            }
    
    async def execute_wsl(
        self,
        command: str,
        working_dir: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute command in WSL/Ubuntu"""
        try:
            timeout_val = timeout or self.default_timeout
            
            # Check if WSL is available
            wsl_check = await asyncio.create_subprocess_exec(
                "wsl.exe",
                "--status",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await wsl_check.communicate()
            
            if wsl_check.returncode != 0:
                return {
                    "success": False,
                    "error": "WSL is not installed or not configured properly",
                    "shell": "WSL"
                }
            
            # Convert Windows path to WSL path if working_dir is provided
            wsl_command = command
            if working_dir:
                # Convert Windows path to WSL path
                wsl_path = working_dir.replace("\\", "/").replace("C:", "/mnt/c")
                wsl_command = f"cd {wsl_path} && {command}"
            
            process = await asyncio.create_subprocess_exec(
                "wsl.exe",
                "-e",
                "bash",
                "-c",
                wsl_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_val
            )
            
            return {
                "success": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "shell": "WSL/Ubuntu"
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Command timed out after {timeout_val} seconds",
                "shell": "WSL"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "shell": "WSL"
            }
    
    async def execute_gitbash(
        self,
        command: str,
        working_dir: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute command in Git Bash"""
        try:
            if not self.git_bash_path:
                return {
                    "success": False,
                    "error": "Git Bash not found. Please install Git for Windows.",
                    "shell": "Git Bash"
                }
            
            timeout_val = timeout or self.default_timeout
            
            # Convert Windows path to Git Bash format if needed
            bash_command = command
            if working_dir:
                # Convert to Git Bash path format
                git_path = working_dir.replace("\\", "/")
                if git_path[1] == ":":
                    git_path = "/" + git_path[0].lower() + git_path[2:]
                bash_command = f"cd {git_path} && {command}"
            
            process = await asyncio.create_subprocess_exec(
                self.git_bash_path,
                "-c",
                bash_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_val
            )
            
            return {
                "success": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "shell": "Git Bash"
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Command timed out after {timeout_val} seconds",
                "shell": "Git Bash"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "shell": "Git Bash"
            }


# Initialize MCP Server
app = Server("shell-executor")
executor = ShellExecutor()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available shell execution tools"""
    return [
        Tool(
            name="execute_cmd",
            description="Execute a command in Windows Command Prompt (CMD). "
                       "Use for Windows-native commands like dir, copy, del, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in CMD"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Optional working directory for command execution"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Optional timeout in seconds (default: 30)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="execute_powershell",
            description="Execute a command or script in PowerShell. "
                       "Use for PowerShell cmdlets, .NET operations, and advanced Windows scripting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The PowerShell command or script to execute"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Optional working directory for command execution"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Optional timeout in seconds (default: 30)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="execute_wsl",
            description="Execute a command in WSL (Windows Subsystem for Linux) / Ubuntu. "
                       "Use for Linux commands, bash scripts, and Unix utilities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The bash/Linux command to execute in WSL"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Optional Windows working directory (will be converted to WSL path)"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Optional timeout in seconds (default: 30)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="execute_gitbash",
            description="Execute a command in Git Bash. "
                       "Use for Git operations and Unix-like commands on Windows.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The bash command to execute in Git Bash"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Optional Windows working directory"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Optional timeout in seconds (default: 30)"
                    }
                },
                "required": ["command"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests"""
    
    try:
        command = arguments.get("command")
        working_dir = arguments.get("working_dir")
        timeout = arguments.get("timeout")
        
        if not command:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": "Command parameter is required"
                }, indent=2)
            )]
        
        # Execute based on tool name
        if name == "execute_cmd":
            result = await executor.execute_cmd(command, working_dir, timeout)
        elif name == "execute_powershell":
            result = await executor.execute_powershell(command, working_dir, timeout)
        elif name == "execute_wsl":
            result = await executor.execute_wsl(command, working_dir, timeout)
        elif name == "execute_gitbash":
            result = await executor.execute_gitbash(command, working_dir, timeout)
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Unknown tool: {name}"
                }, indent=2)
            )]
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }, indent=2)
        )]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
