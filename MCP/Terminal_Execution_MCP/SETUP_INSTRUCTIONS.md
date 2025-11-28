# Multi-Shell MCP Server - Setup Instructions

## ✅ Installation Complete!

The MCP server files have been created in: `C:\Users\Hp\shell_mcp_server\`

---

## 🚀 Setup Steps

### Step 1: Open Command Prompt
Press `Win + R`, type `cmd`, and press Enter.

### Step 2: Navigate to the MCP Server Directory
```cmd
cd C:\Users\Hp\shell_mcp_server
```

### Step 3: Create Virtual Environment
```cmd
python -m venv venv
```

**Expected Output:** A `venv` folder will be created in the directory.

### Step 4: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

**Expected Output:** Your command prompt should now show `(venv)` at the beginning.

### Step 5: Install Dependencies
```cmd
pip install -r requirements.txt
```

**Expected Output:** 
```
Successfully installed mcp-x.x.x [and dependencies]
```

### Step 6: Verify Installation (Optional)
Test that the server can start:
```cmd
python server.py
```

You should see the server initialize. Press `Ctrl+C` to stop it.

### Step 7: Restart Claude Desktop
Close and restart the Claude Desktop application to load the new MCP server.

---

## 🎯 Verification

After restarting Claude, you should see these new tools available:
- `execute_cmd` - Execute Windows CMD commands
- `execute_powershell` - Execute PowerShell commands
- `execute_wsl` - Execute WSL/Ubuntu bash commands
- `execute_gitbash` - Execute Git Bash commands

---

## 📝 Example Commands to Test

### Test CMD
Ask Claude: "Use CMD to list files in my Downloads folder"

### Test PowerShell
Ask Claude: "Use PowerShell to get the current date and time"

### Test WSL
Ask Claude: "Use WSL to show my Linux home directory"

### Test Git Bash
Ask Claude: "Use Git Bash to show the Git version"

---

## 🔧 Troubleshooting

### Virtual Environment Not Activating
Make sure you're in the correct directory:
```cmd
cd C:\Users\Hp\shell_mcp_server
```

### Python Not Found
Install Python from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### MCP Package Installation Fails
Ensure you have the latest pip:
```cmd
python -m pip install --upgrade pip
```

Then retry:
```cmd
pip install -r requirements.txt
```

### Git Bash Not Available
Install Git for Windows from: https://git-scm.com/download/win

### WSL Not Available
Install WSL with:
```cmd
wsl --install
```

Restart your computer after installation.

---

## 📍 Configuration Location

The MCP server has been added to Claude's configuration file at:
```
C:\Users\Hp\AppData\Roaming\Claude\claude_desktop_config.json
```

Server entry added:
```json
"shell-executor": {
  "command": "C:\\Users\\Hp\\shell_mcp_server\\venv\\Scripts\\python.exe",
  "args": ["C:\\Users\\Hp\\shell_mcp_server\\server.py"]
}
```

---

## ⚠️ Security Notice

This MCP server executes commands on your system. Use it responsibly:
- Only execute commands you understand
- Be cautious with commands that modify system files
- Review command output before taking further actions
- Consider running in a limited user environment for production use

---

## 🎓 Additional Resources

- MCP Documentation: https://modelcontextprotocol.io
- Python Documentation: https://docs.python.org
- WSL Documentation: https://docs.microsoft.com/windows/wsl

---

**Installation Date:** October 30, 2025
**Version:** 1.0.0

If you encounter any issues, refer to the README.md file in the shell_mcp_server directory.
