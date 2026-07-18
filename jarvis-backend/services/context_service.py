"""Context Service

Manages desktop context awareness
"""

from typing import Dict, Any, Optional


class ContextManager:
    """Track desktop context"""
    
    def __init__(self):
        self.context: Dict[str, Any] = {
            "active_window": None,
            "current_file": None,
            "open_tabs": [],
            "clipboard": None,
            "cursor_position": None,
            "timestamp": None
        }
    
    async def update_context(self, **kwargs):
        """Update context data"""
        self.context.update(kwargs)
        
        from datetime import datetime
        self.context["timestamp"] = datetime.now().isoformat()
    
    def get_context(self) -> Dict[str, Any]:
        """Get current context"""
        return self.context.copy()
    
    def format_for_llm(self) -> str:
        """Format context as string for LLM injection"""
        lines = ["=== Current Desktop Context ==="]
        
        if self.context.get("active_window"):
            lines.append(f"Active Window: {self.context['active_window']}")
        
        if self.context.get("current_file"):
            lines.append(f"Current File: {self.context['current_file']}")
        
        if self.context.get("open_tabs"):
            tabs = ", ".join(self.context['open_tabs'][:3])
            lines.append(f"Open Tabs: {tabs}")
        
        if self.context.get("clipboard"):
            clipboard_preview = self.context["clipboard"][:100]
            lines.append(f"Clipboard: {clipboard_preview}...")
        
        return "\n".join(lines)
    
    def detect_active_window(self) -> Optional[str]:
        """Detect active window title (Windows only)"""
        try:
            import pygetwindow as gw
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
        except Exception as e:
            print(f"⚠️ Window detection: {e}")
        return None
    
    def get_clipboard(self) -> Optional[str]:
        """Get clipboard content"""
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception as e:
            print(f"⚠️ Clipboard access: {e}")
        return None
    
    def get_cursor_position(self) -> Optional[tuple]:
        """Get mouse cursor position"""
        try:
            import pyautogui
            return pyautogui.position()
        except Exception as e:
            print(f"⚠️ Cursor position: {e}")
        return None
