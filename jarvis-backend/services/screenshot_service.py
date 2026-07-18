"""Screenshot Service

Handles desktop screenshot capture and analysis
"""

from typing import Optional, Dict
import os


class ScreenshotService:
    """Capture and analyze screenshots"""
    
    def __init__(self):
        self.last_screenshot_path = None
        self.vision_model = None
    
    def capture_screenshot(self, save_path: str = "screenshot.png") -> Optional[str]:
        """
        Capture current desktop screenshot
        
        Args:
            save_path: Where to save screenshot
        
        Returns:
            Path to screenshot or None
        """
        try:
            import mss
            from PIL import Image
            
            with mss.mss() as sct:
                # Capture primary monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Save
                img.save(save_path)
                
                self.last_screenshot_path = save_path
                return save_path
        
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def extract_text_ocr(self, image_path: str) -> Optional[str]:
        """
        Extract text from image using PaddleOCR
        
        Args:
            image_path: Path to image file
        
        Returns:
            Extracted text or None
        """
        try:
            from paddleocr import PaddleOCR
            
            if self.vision_model is None:
                self.vision_model = PaddleOCR(use_angle_cls=True, lang='en')
            
            result = self.vision_model.ocr(image_path, cls=True)
            if not result or not result[0]:
                return ""
            
            # Extract text
            text_lines = []
            for line in result:
                if not line:
                    continue
                for word_info in line:
                    text = word_info[1][0]
                    confidence = word_info[1][1]
                    if confidence > 0.5:  # Filter low confidence
                        text_lines.append(text)
            
            return " ".join(text_lines)
        
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return None
    
    def analyze_screenshot(self, image_path: str, question: str) -> Optional[str]:
        """
        Analyze screenshot with vision model
        
        Args:
            image_path: Path to image
            question: What to ask about the image
        
        Returns:
            Analysis or None
        """
        try:
            # TODO: Implement vision model analysis
            # Options: Qwen2.5-VL, Moondream, LLaVA
            
            # For now, use OCR + basic analysis
            text = self.extract_text_ocr(image_path)
            
            if text:
                return f"Text found in screenshot: {text[:200]}..."
            else:
                return "No text detected in screenshot"
        
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return None
