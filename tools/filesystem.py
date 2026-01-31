import os
import re


BASE_DIR = "sandbox"

os.makedirs(BASE_DIR, exist_ok=True)


def extract_filename(text: str):
    """
    Extract filename from filesystem tool call.
    Returns filename or None if not found/safe.
    """
    # Look for quoted filenames: create file "name.txt"
    quoted_match = re.search(r'["\']([\w\-\.]+)["\']', text)
    if quoted_match:
        filename = quoted_match.group(1)
        # Safety: only allow alphanumeric, dash, underscore, single dot for extension
        if re.match(r'^[\w\-]+\.[\w]+$', filename):
            return filename
    
    # Fallback to generic name if no valid filename found
    return "data.txt"


def handle_filesystem(text: str):
    """
    Handle filesystem operations safely within sandbox directory.
    Returns result string describing what was done, or None on error.
    """
    try:
        text_lower = text.lower()
        
        # CREATE FILE operation
        if "create file" in text_lower or "write file" in text_lower:
            filename = extract_filename(text)
            filepath = os.path.join(BASE_DIR, filename)
            
            # Extract content if present, otherwise use placeholder
            content_match = re.search(r'content[:\s]+["\']?([^"\']*)["\']?(?:\s|$)', text, re.IGNORECASE)
            content = content_match.group(1) if content_match else "Created by JARVIS"
            
            # Write file
            with open(filepath, "w") as f:
                f.write(content)
            
            return f"✅ File created: {filename} ({len(content)} bytes)"
        
        # READ FILE operation
        elif "read file" in text_lower or "view file" in text_lower:
            filename = extract_filename(text)
            filepath = os.path.join(BASE_DIR, filename)
            
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    content = f.read()
                return f"✅ File contents ({len(content)} bytes):\n{content}"
            else:
                return f"❌ File not found: {filename}"
        
        # LIST FILES operation
        elif "list files" in text_lower or "show files" in text_lower:
            files = os.listdir(BASE_DIR)
            if files:
                return f"📁 Files in sandbox:\n" + "\n".join(f"  • {f}" for f in files)
            else:
                return "📁 Sandbox is empty"
        
        # DELETE FILE operation
        elif "delete file" in text_lower or "remove file" in text_lower:
            filename = extract_filename(text)
            filepath = os.path.join(BASE_DIR, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return f"✅ File deleted: {filename}"
            else:
                return f"❌ File not found: {filename}"
        
        # Unknown operation
        else:
            return "ℹ️ Supported operations: create file, read file, list files, delete file"
    
    except Exception as e:
        return f"❌ Filesystem error: {e}"
