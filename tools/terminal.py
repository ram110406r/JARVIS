import re
import platform


def parse_command(text: str):
    """
    Extract command from terminal tool call.
    Returns command or None if not safe/clear.
    """
    # Look for quoted commands: run "ls -la"
    quoted_match = re.search(r'["\']([^"\']+)["\']', text)
    if quoted_match:
        return quoted_match.group(1).strip()
    
    # Look for common command patterns
    # Support: list, dir, pwd, whoami, echo
    for cmd in ["list", "dir", "pwd", "whoami", "echo"]:
        if cmd in text.lower():
            # Extract the rest of the line as arguments
            match = re.search(rf'{cmd}\s+(.*?)(?:\s|$)', text, re.IGNORECASE)
            args = match.group(1) if match else ""
            return f"{cmd} {args}".strip()
    
    return None


def format_command_help():
    """Return help text for terminal operations."""
    return (
        "🖥️ Terminal tool (dry-run only):\n"
        "Supported commands: list, dir, pwd, whoami, echo\n"
        "Example: run 'ls -la' or 'echo hello'"
    )


def handle_terminal(text: str):
    """
    Handle terminal commands in dry-run mode.
    Never executes real commands. Returns description of what would be executed.
    """
    try:
        command = parse_command(text)
        
        if not command:
            return format_command_help()
        
        # Normalize command to cross-platform equivalent
        cmd_lower = command.lower()
        
        # Handle platform-specific commands
        if cmd_lower.startswith("ls"):
            # ls → dir on Windows
            os_type = platform.system()
            if os_type == "Windows":
                dry_run = "🔍 DRY RUN: dir"
                args = command[2:].strip()
                if args:
                    dry_run += f" {args}"
            else:
                dry_run = f"🔍 DRY RUN: {command}"
            
            return (
                f"{dry_run}\n"
                "→ Would list files in current directory"
            )
        
        elif cmd_lower.startswith("dir"):
            return (
                f"🔍 DRY RUN: {command}\n"
                "→ Would list files in current directory"
            )
        
        elif cmd_lower.startswith("pwd"):
            return (
                f"🔍 DRY RUN: {command}\n"
                "→ Would display current working directory"
            )
        
        elif cmd_lower.startswith("whoami"):
            return (
                f"🔍 DRY RUN: {command}\n"
                "→ Would display current user"
            )
        
        elif cmd_lower.startswith("echo"):
            # Extract echo argument
            args = command[4:].strip() if len(command) > 4 else ""
            return (
                f"🔍 DRY RUN: {command}\n"
                f"→ Would output: {args}"
            )
        
        else:
            return (
                f"🔍 DRY RUN: {command}\n"
                "⚠️ Command type not recognized. "
                "Supported: list, dir, pwd, whoami, echo"
            )
    
    except Exception as e:
        return f"❌ Terminal error: {e}"
