
#!/usr/bin/env python3

"""
MCP Server: File System Manager
Exposes full CRUD file system access via MCP protocol
Version: 2.0.0
Features: List, Read, Write, Update, Delete operations with comprehensive security
"""

import asyncio
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# ====================================================================
# CONFIGURATION
# ====================================================================

BASE_DIRECTORY = Path(os.getenv("MCP_BASE_DIR", os.getcwd())).resolve()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_SEARCH_RESULTS = 100
ALLOWED_WRITE = os.getenv("MCP_ALLOW_WRITE", "true").lower() == "true"
ALLOWED_DELETE = os.getenv("MCP_ALLOW_DELETE", "true").lower() == "true"

# ====================================================================
# SECURITY UTILITIES
# ====================================================================

def sanitize_path(input_path: str) -> Path:
    """
    Sanitize and resolve path to prevent directory traversal attacks.

    Args:
        input_path (str): The path to sanitize.

    Returns:
        Path: The resolved absolute path.

    Raises:
        ValueError: If the path attempts to traverse outside the base directory.
    """
    try:
        # Normalize and resolve the path
        requested = Path(input_path).expanduser()
        if requested.is_absolute():
            resolved = requested.resolve()
        else:
            resolved = (BASE_DIRECTORY / requested).resolve()

        # Ensure resolved path is within BASE_DIRECTORY
        resolved.relative_to(BASE_DIRECTORY)

        return resolved
    except (ValueError, RuntimeError) as e:
        raise ValueError(f"Access denied: Path traversal attempt detected - {e}")


def validate_file_size(file_path: Path) -> None:
    """
    Check if file size is within acceptable limits.

    Args:
        file_path (Path): The path to the file to check.

    Returns:
        None

    Raises:
        ValueError: If the file size exceeds MAX_FILE_SIZE.
    """
    size = file_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File exceeds maximum size of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )


def validate_write_size(content: str) -> None:
    """
    Validate content size before writing.

    Args:
        content (str): The content to check.

    Returns:
        None

    Raises:
        ValueError: If the content size exceeds MAX_FILE_SIZE.
    """
    size = len(content.encode('utf-8'))
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"Content exceeds maximum size of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )


def check_write_permission() -> None:
    """
    Check if write operations are allowed.

    Args:
        None

    Returns:
        None

    Raises:
        PermissionError: If write operations are disabled by configuration.
    """
    if not ALLOWED_WRITE:
        raise PermissionError("Write operations are disabled")


def check_delete_permission() -> None:
    """
    Check if delete operations are allowed.

    Args:
        None

    Returns:
        None

    Raises:
        PermissionError: If delete operations are disabled by configuration.
    """
    if not ALLOWED_DELETE:
        raise PermissionError("Delete operations are disabled")


def read_file_with_fallback(file_path: Path) -> str:
    """
    Read file with encoding fallback (utf-8, latin-1, cp1252).

    Args:
        file_path (Path): The path to the file to read.

    Returns:
        str: The content of the file.
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except (UnicodeDecodeError, LookupError):
            continue

    # Final fallback: read as binary and decode with errors='replace'
    return file_path.read_bytes().decode("utf-8", errors="replace")


# ====================================================================
# CORE FUNCTIONS - READ OPERATIONS
# ====================================================================

async def list_files_in_directory(directory_path: str) -> list[dict[str, Any]]:
    """
    List all files and directories in a given path.

    Args:
        directory_path (str): The relative path to list.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing files/directories,
                              each containing 'name', 'path', 'type', 'modified', and optionally 'size'.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ValueError: If the path is not a directory.
        PermissionError: If permission is denied.
    """
    safe_path = sanitize_path(directory_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not safe_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")

    items = []

    try:
        for entry in safe_path.iterdir():
            try:
                stat = entry.stat()
                relative_path = entry.relative_to(BASE_DIRECTORY)

                item = {
                    "name": entry.name,
                    "path": str(relative_path),
                    "type": "directory" if entry.is_dir() else "file",
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }

                if entry.is_file():
                    item["size"] = stat.st_size

                items.append(item)
            except (PermissionError, OSError) as e:
                items.append({
                    "name": entry.name,
                    "type": "error",
                    "error": str(e),
                })
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {e}")

    # Sort: directories first, then files, alphabetically
    items.sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))

    return items


async def read_file(file_path: str) -> dict[str, Any]:
    """
    Read the complete contents of a file.

    Args:
        file_path (str): The relative path to the file.

    Returns:
        dict[str, Any]: A dictionary containing 'path', 'content', 'size', 'modified', and 'encoding'.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file or size is too large.
    """
    safe_path = sanitize_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    validate_file_size(safe_path)

    content = read_file_with_fallback(safe_path)
    stat = safe_path.stat()

    return {
        "path": str(safe_path.relative_to(BASE_DIRECTORY)),
        "content": content,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "encoding": "utf-8"
    }


async def search_file(
    file_path: str,
    search_string: str,
    case_sensitive: bool = False
) -> dict[str, Any]:
    """
    Search for a string within a file.

    Args:
        file_path (str): The relative path to the file.
        search_string (str): The string to search for.
        case_sensitive (bool): Whether the search is case-sensitive. Defaults to False.

    Returns:
        dict[str, Any]: A dictionary containing search results, including 'matches' (line number and content).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file.
    """
    safe_path = sanitize_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    validate_file_size(safe_path)

    content = read_file_with_fallback(safe_path)
    lines = content.splitlines()

    matches = []
    needle = search_string if case_sensitive else search_string.lower()

    for line_num, line in enumerate(lines, start=1):
        haystack = line if case_sensitive else line.lower()
        if needle in haystack:
            matches.append({
                "lineNumber": line_num,
                "line": line.strip(),
            })

            if len(matches) >= MAX_SEARCH_RESULTS:
                break

    return {
        "file": str(safe_path.relative_to(BASE_DIRECTORY)),
        "searchString": search_string,
        "caseSensitive": case_sensitive,
        "totalMatches": len(matches),
        "matches": matches,
    }


# ====================================================================
# CORE FUNCTIONS - WRITE OPERATIONS
# ====================================================================

async def write_file(
    file_path: str,
    content: str,
    create_dirs: bool = False
) -> dict[str, Any]:
    """
    Write content to a file (create or overwrite).

    Args:
        file_path (str): The relative path to the file.
        content (str): The content to write.
        create_dirs (bool): Whether to create parent directories if they don't exist. Defaults to False.

    Returns:
        dict[str, Any]: Metadata about the written file ('path', 'operation', 'size', 'modified').

    Raises:
        PermissionError: If write operations are disabled.
        FileNotFoundError: If parent directory does not exist and create_dirs is False.
        IOError: If writing fails.
    """
    check_write_permission()

    safe_path = sanitize_path(file_path)
    validate_write_size(content)

    # Create parent directories if requested
    if create_dirs:
        safe_path.parent.mkdir(parents=True, exist_ok=True)
    elif not safe_path.parent.exists():
        raise FileNotFoundError(f"Parent directory does not exist: {safe_path.parent}")

    # Check if overwriting existing file
    existed = safe_path.exists()

    try:
        safe_path.write_text(content, encoding='utf-8')
        stat = safe_path.stat()

        return {
            "path": str(safe_path.relative_to(BASE_DIRECTORY)),
            "operation": "overwritten" if existed else "created",
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception as e:
        raise IOError(f"Failed to write file: {e}")


async def append_file(
    file_path: str,
    content: str
) -> dict[str, Any]:
    """
    Append content to an existing file.

    Args:
        file_path (str): The relative path to the file.
        content (str): The content to append.

    Returns:
        dict[str, Any]: Metadata about the updated file.

    Raises:
        PermissionError: If write operations are disabled.
        FileNotFoundError: If the file does not exist.
        ValueError: If the file becomes too large.
        IOError: If appending fails.
    """
    check_write_permission()

    safe_path = sanitize_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Check combined size
    current_size = safe_path.stat().st_size
    new_content_size = len(content.encode('utf-8'))
    if current_size + new_content_size > MAX_FILE_SIZE:
        raise ValueError(f"Appending would exceed maximum file size")

    try:
        with safe_path.open('a', encoding='utf-8') as f:
            f.write(content)

        stat = safe_path.stat()

        return {
            "path": str(safe_path.relative_to(BASE_DIRECTORY)),
            "operation": "appended",
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception as e:
        raise IOError(f"Failed to append to file: {e}")


async def update_file(
    file_path: str,
    search_string: str,
    replace_string: str,
    case_sensitive: bool = False,
    max_replacements: Optional[int] = None
) -> dict[str, Any]:
    """
    Update file by replacing occurrences of a string.

    Args:
        file_path (str): The relative path to the file.
        search_string (str): The string to find.
        replace_string (str): The string to replace with.
        case_sensitive (bool): Case sensitive search. Defaults to False.
        max_replacements (Optional[int]): Max replacement count. Defaults to None (unlimited).

    Returns:
        dict[str, Any]: Metadata including number of replacements made.

    Raises:
        PermissionError: If write operations are disabled.
        FileNotFoundError: If the file does not exist.
        IOError: If update fails.
    """
    check_write_permission()

    safe_path = sanitize_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    validate_file_size(safe_path)

    content = read_file_with_fallback(safe_path)

    # Perform replacement
    if case_sensitive:
        if max_replacements:
            updated_content = content.replace(search_string, replace_string, max_replacements)
        else:
            updated_content = content.replace(search_string, replace_string)
        replacements = content.count(search_string)
    else:
        # Case-insensitive replacement
        import re
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        matches = pattern.findall(content)
        replacements = len(matches)
        if max_replacements:
            updated_content = pattern.sub(replace_string, content, count=max_replacements)
        else:
            updated_content = pattern.sub(replace_string, content)

    validate_write_size(updated_content)

    try:
        safe_path.write_text(updated_content, encoding='utf-8')
        stat = safe_path.stat()

        return {
            "path": str(safe_path.relative_to(BASE_DIRECTORY)),
            "operation": "updated",
            "replacements": min(replacements, max_replacements) if max_replacements else replacements,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception as e:
        raise IOError(f"Failed to update file: {e}")


# ====================================================================
# CORE FUNCTIONS - DELETE OPERATIONS
# ====================================================================

async def delete_file(file_path: str) -> dict[str, Any]:
    """
    Delete a file.

    Args:
        file_path (str): The relative path to the file.

    Returns:
        dict[str, Any]: Metadata about the deleted file.

    Raises:
        PermissionError: If delete operations are disabled.
        FileNotFoundError: If the file does not exist.
        IOError: If deletion fails.
    """
    check_delete_permission()

    safe_path = sanitize_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        relative_path = str(safe_path.relative_to(BASE_DIRECTORY))
        safe_path.unlink()

        return {
            "path": relative_path,
            "operation": "deleted",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise IOError(f"Failed to delete file: {e}")


async def delete_directory(
    directory_path: str,
    recursive: bool = False
) -> dict[str, Any]:
    """
    Delete a directory (optionally recursive).

    Args:
        directory_path (str): The relative path to the directory.
        recursive (bool): Whether to delete recursively. Defaults to False.

    Returns:
        dict[str, Any]: Metadata about the deleted directory.

    Raises:
        PermissionError: If delete operations are disabled.
        FileNotFoundError: If the directory does not exist.
        ValueError: If directory is not empty and recursive is False.
        IOError: If deletion fails.
    """
    check_delete_permission()

    safe_path = sanitize_path(directory_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not safe_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")

    # Prevent deletion of base directory
    if safe_path == BASE_DIRECTORY:
        raise PermissionError("Cannot delete base directory")

    try:
        relative_path = str(safe_path.relative_to(BASE_DIRECTORY))

        if recursive:
            shutil.rmtree(safe_path)
        else:
            safe_path.rmdir()  # Only works if empty

        return {
            "path": relative_path,
            "operation": "deleted",
            "recursive": recursive,
            "timestamp": datetime.now().isoformat(),
        }
    except OSError as e:
        if "Directory not empty" in str(e):
            raise ValueError("Directory not empty. Use recursive=true to delete non-empty directories")
        raise IOError(f"Failed to delete directory: {e}")


# ====================================================================
# CORE FUNCTIONS - CREATE OPERATIONS
# ====================================================================

async def create_directory(
    directory_path: str,
    parents: bool = False
) -> dict[str, Any]:
    """
    Create a new directory.

    Args:
        directory_path (str): The relative path to the directory.
        parents (bool): Whether to create parent directories. Defaults to False.

    Returns:
        dict[str, Any]: Metadata about the created directory.

    Raises:
        PermissionError: If write operations are disabled.
        ValueError: If path already exists.
        IOError: If creation fails.
    """
    check_write_permission()

    safe_path = sanitize_path(directory_path)

    if safe_path.exists():
        raise ValueError(f"Path already exists: {directory_path}")

    try:
        safe_path.mkdir(parents=parents, exist_ok=False)

        return {
            "path": str(safe_path.relative_to(BASE_DIRECTORY)),
            "operation": "created",
            "type": "directory",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise IOError(f"Failed to create directory: {e}")


# ====================================================================
# MCP SERVER INITIALIZATION
# ====================================================================

app = Server("filesystem-manager")


# ====================================================================
# RESOURCE HANDLERS
# ====================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List available resources.

    Returns:
        list[Resource]: A list of available file system resources.
    """
    return [
        Resource(
            uri=f"file:///{BASE_DIRECTORY}",
            name="File System Root",
            description=f"Full CRUD access to files and directories from: {BASE_DIRECTORY}",
            mimeType="application/json",
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a resource by URI.

    Args:
        uri (str): The URI of the resource to read.

    Returns:
        str: JSON representation of the resource content.

    Raises:
        ValueError: If URI is invalid.
    """
    if not uri.startswith("file:///"):
        raise ValueError("Invalid resource URI")

    requested_path = uri.replace("file:///", "")
    items = await list_files_in_directory(requested_path or ".")

    return json.dumps(items, indent=2)


# ====================================================================
# TOOL HANDLERS
# ====================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.

    Returns:
        list[Tool]: A list of Tool objects describing available operations.
    """
    tools = [
        Tool(
            name="list_directory",
            description="List all files and directories in a specified path. Returns name, type, size, and modification date for each item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list (relative to base directory). Use '.' for current directory.",
                    }
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="read_file",
            description="Read the complete contents of a file. Returns the file content, size, and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read (relative to base directory)",
                    }
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="search_file",
            description="Search for a specific string within a file. Returns all matching lines with line numbers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to search (relative to base directory)",
                    },
                    "search_string": {
                        "type": "string",
                        "description": "String to search for within the file",
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether the search should be case-sensitive (default: false)",
                        "default": False,
                    },
                },
                "required": ["file_path", "search_string"],
            },
        ),
    ]

    if ALLOWED_WRITE:
        tools.extend([
            Tool(
                name="write_file",
                description="Write content to a file. Creates new file or overwrites existing one. Optionally creates parent directories.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to write (relative to base directory)",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file",
                        },
                        "create_dirs": {
                            "type": "boolean",
                            "description": "Create parent directories if they don't exist (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["file_path", "content"],
                },
            ),
            Tool(
                name="append_file",
                description="Append content to the end of an existing file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to append to (relative to base directory)",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to append to the file",
                        },
                    },
                    "required": ["file_path", "content"],
                },
            ),
            Tool(
                name="update_file",
                description="Update file by replacing occurrences of a string with another string. Supports case-sensitive and case-insensitive replacement.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to update (relative to base directory)",
                        },
                        "search_string": {
                            "type": "string",
                            "description": "String to search for and replace",
                        },
                        "replace_string": {
                            "type": "string",
                            "description": "String to replace matches with",
                        },
                        "case_sensitive": {
                            "type": "boolean",
                            "description": "Whether the search should be case-sensitive (default: false)",
                            "default": False,
                        },
                        "max_replacements": {
                            "type": "integer",
                            "description": "Maximum number of replacements to make (default: unlimited)",
                        },
                    },
                    "required": ["file_path", "search_string", "replace_string"],
                },
            ),
            Tool(
                name="create_directory",
                description="Create a new directory. Optionally creates parent directories.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "Path to the directory to create (relative to base directory)",
                        },
                        "parents": {
                            "type": "boolean",
                            "description": "Create parent directories if they don't exist (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["directory_path"],
                },
            ),
        ])

    if ALLOWED_DELETE:
        tools.extend([
            Tool(
                name="delete_file",
                description="Delete a file. This operation is irreversible.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to delete (relative to base directory)",
                        },
                    },
                    "required": ["file_path"],
                },
            ),
            Tool(
                name="delete_directory",
                description="Delete a directory. Optionally deletes recursively including all contents.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "Path to the directory to delete (relative to base directory)",
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "Delete directory and all its contents recursively (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["directory_path"],
                },
            ),
        ])

    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls.

    Args:
        name (str): The name of the tool to call.
        arguments (Any): The arguments for the tool.

    Returns:
        list[TextContent]: A list of TextContent objects with the results.

    Raises:
        ValueError: If the tool is unknown.
    """
    try:
        # READ OPERATIONS
        if name == "list_directory":
            items = await list_files_in_directory(arguments.get("path", "."))
            return [TextContent(type="text", text=json.dumps(items, indent=2))]

        elif name == "read_file":
            result = await read_file(file_path=arguments["file_path"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "search_file":
            result = await search_file(
                file_path=arguments["file_path"],
                search_string=arguments["search_string"],
                case_sensitive=arguments.get("case_sensitive", False),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # WRITE OPERATIONS
        elif name == "write_file":
            result = await write_file(
                file_path=arguments["file_path"],
                content=arguments["content"],
                create_dirs=arguments.get("create_dirs", False),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "append_file":
            result = await append_file(
                file_path=arguments["file_path"],
                content=arguments["content"],
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "update_file":
            result = await update_file(
                file_path=arguments["file_path"],
                search_string=arguments["search_string"],
                replace_string=arguments["replace_string"],
                case_sensitive=arguments.get("case_sensitive", False),
                max_replacements=arguments.get("max_replacements"),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "create_directory":
            result = await create_directory(
                directory_path=arguments["directory_path"],
                parents=arguments.get("parents", False),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # DELETE OPERATIONS
        elif name == "delete_file":
            result = await delete_file(file_path=arguments["file_path"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "delete_directory":
            result = await delete_directory(
                directory_path=arguments["directory_path"],
                recursive=arguments.get("recursive", False),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# ====================================================================
# SERVER STARTUP
# ====================================================================

async def main():
    """
    Main entry point for the MCP server.

    Starts the server using stdio transport.

    Args:
        None

    Returns:
        None
    """
    async with stdio_server() as (read_stream, write_stream):
        print(f"MCP File System Manager running", file=sys.stderr)
        print(f"Base directory: {BASE_DIRECTORY}", file=sys.stderr)
        print(f"Write operations: {'ENABLED' if ALLOWED_WRITE else 'DISABLED'}", file=sys.stderr)
        print(f"Delete operations: {'ENABLED' if ALLOWED_DELETE else 'DISABLED'}", file=sys.stderr)

        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
