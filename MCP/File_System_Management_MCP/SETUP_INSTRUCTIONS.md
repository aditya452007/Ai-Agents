# Setup Instructions for File System Management MCP

This directory contains an MCP (Model Context Protocol) server for managing the file system.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

## Installation

1.  Navigate to this directory:
    ```bash
    cd MCP/File_System_Management_MCP
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

You can configure the server using environment variables:

-   `MCP_BASE_DIR`: The base directory for file operations (default: current working directory).
-   `MCP_ALLOW_WRITE`: Enable write operations (default: `true`). Set to `false` to disable.
-   `MCP_ALLOW_DELETE`: Enable delete operations (default: `true`). Set to `false` to disable.

## Running the Server

Run the server using the following command:

```bash
python filesystem_mcp_server.py
```

## Usage with MCP Client

To use this server with an MCP client (like Claude Desktop or an IDE plugin):

1.  Ensure the server is running or configure your client to run the python script.
2.  The server exposes tools for:
    -   `list_directory`: List files and directories.
    -   `read_file`: Read file contents.
    -   `write_file`: Create or overwrite files.
    -   `append_file`: Append content to files.
    -   `update_file`: Replace text in files.
    -   `delete_file`: Delete files.
    -   `create_directory`: Create directories.
    -   `delete_directory`: Delete directories.
    -   `search_file`: Search for text within files.

## Security Note

This server provides access to the file system. Ensure `MCP_BASE_DIR` is set to a safe directory if you are running this in a sensitive environment. By default, it uses the current working directory.
