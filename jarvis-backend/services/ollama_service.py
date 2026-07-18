"""Ollama LLM Service

Handles communication with local Ollama instance
"""

import requests
from typing import Optional


class OllamaService:
    """Interface to Ollama local LLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama2"  # Default model
        self.conversation = []
    
    def chat(self, message: str, context: str = "") -> Optional[str]:
        """
        Send message to Ollama and get response
        
        Args:
            message: User message
            context: Optional context to prepend
        
        Returns:
            Response text or None if error
        """
        try:
            # Prepare context
            full_message = f"{context}\n\n{message}" if context else message
            
            # Add to conversation
            self.conversation.append({
                "role": "user",
                "content": full_message
            })
            
            # Call Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.conversation,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["message"]["content"]
                
                # Add to conversation
                self.conversation.append({
                    "role": "assistant",
                    "content": reply
                })
                
                # Keep conversation bounded
                if len(self.conversation) > 20:
                    self.conversation = self.conversation[-20:]
                
                return reply
            else:
                print(f"❌ Ollama error: {response.status_code}")
                return None
        
        except requests.ConnectionError:
            print("❌ Cannot connect to Ollama. Ensure Ollama is running: ollama serve")
            return None
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return None
    
    def set_model(self, model: str):
        """Set the model to use"""
        self.model = model
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation = []
