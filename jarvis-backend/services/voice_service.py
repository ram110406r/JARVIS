"""Voice Service

Handles speech-to-text (Whisper) and text-to-speech (Piper)
"""

from typing import Optional
import io


class VoiceService:
    """Manages voice input/output"""
    
    def __init__(self):
        self.whisper_model = None
        self.tts_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize Whisper and Piper (lazy load)"""
        # Will be initialized on first use
        pass
    
    def transcribe_audio(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transcribe audio bytes using Whisper
        
        Args:
            audio_bytes: Raw audio data
        
        Returns:
            Transcribed text or None
        """
        try:
            # Lazy load Whisper
            if self.whisper_model is None:
                import whisper
                self.whisper_model = whisper.load_model("base")
            
            # Save audio to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            # Transcribe
            result = self.whisper_model.transcribe(tmp_path)
            text = result["text"]
            
            # Cleanup
            import os
            os.remove(tmp_path)
            
            return text
        
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def synthesize_speech(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech using Piper
        
        Args:
            text: Text to synthesize
        
        Returns:
            Audio bytes or None
        """
        try:
            # Option 1: Use Piper (local)
            # from piper.tts import PiperTTS
            # tts = PiperTTS()
            # audio = tts.synthesize(text)
            
            # Option 2: Use gTTS (simple fallback)
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to bytes
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            
            return audio_bytes.getvalue()
        
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return None
