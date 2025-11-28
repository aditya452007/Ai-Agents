# Multi-Shell MCP Server

A Model Context Protocol (MCP) server that enables Claude to execute commands across multiple shell environments on Windows:
- **CMD** (Windows Command Prompt)
- **PowerShell**
- **WSL/Ubuntu** (Windows Subsystem for Linux)
- **Git Bash**

## Features

- ✅ Execute commands in 4 different shell environments
- ✅ Configurable working directories
- ✅ Timeout protection (default: 30 seconds)
- ✅ Captures stdout, stderr, and exit codes
- ✅ Automatic shell detection and configuration
- ✅ Path conversion for WSL and Git Bash
- ✅ Comprehensive error handling

## Prerequisites

- **Windows 10/11**
- **Python 3.10+**
- **Git for Windows** (for Git Bash support)
- **WSL/Ubuntu** (for WSL support) - Optional
- **Claude Desktop App**

## Installation

### 1. Navigate to the MCP Server Directory

```cmd
cd %USERPROFILE%\shell_mcp_server
```

### 2. Create Virtual Environment

```cmd
python -m venv venv
```

### 3. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 5. Test the Server (Optional)

```cmd
python server.py
```

Press `Ctrl+C` to stop the test.

## Configuration

The server is configured in Claude Desktop's configuration file located at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

See the setup script output for the exact configuration to add.

## Usage Examples

### CMD Commands
```
Execute command: dir C:\Users
```

### PowerShell Commands
```
Execute PowerShell: Get-Process | Select-Object -First 5
```

### WSL/Ubuntu Commands
```
Execute in WSL: ls -la /home
```

### Git Bash Commands
```
Execute in Git Bash: git status
```

## Security Considerations

⚠️ **WARNING**: This MCP server executes arbitrary commands on your system. Only use it in trusted environments.

- Commands run with the same permissions as Claude Desktop
- Default timeout of 30 seconds prevents runaway processes
- Working directory restrictions can be added for enhanced security
- Consider running Claude Desktop with restricted user permissions

## Troubleshooting

### Git Bash Not Found
Install Git for Windows from: https://git-scm.com/download/win

### WSL Not Available
Install WSL:
```cmd
wsl --install
```

### Permission Errors
Run commands that require elevation through the appropriate shell with `runas` or `sudo`.

### Timeout Errors
Increase timeout parameter for long-running commands:
```json
{"command": "long-running-task", "timeout": 60}
```

## Architecture

```
shell_mcp_server/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

MIT License - Use at your own risk.

## Contributing

This is a standalone MCP server. Modify `server.py` to add additional shell types or features.

## Version

1.0.0 - Initial release with CMD, PowerShell, WSL, and Git Bash support.
