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
        self.system_prompt = (
            "You are JARVIS, an intelligent desktop AI companion for developers and founders.\n"
            "Your design is inspired by HeyClicky, but you are focused on productivity, coding, and startup workflows.\n"
            "You operate locally via Ollama. Be concise, helpful, and direct."
        )
    
    def chat(self, message: str, context: str = "") -> Optional[str]:
        """
        Send message to Ollama and get response
        
        Args:
            message: User message
            context: Optional context to prepend to the system prompt
        
        Returns:
            Response text or None if error
        """
        try:
            # Add the user message cleanly to conversation history
            self.conversation.append({
                "role": "user",
                "content": message
            })
            
            # Construct the dynamic messages list starting with a system message
            system_content = self.system_prompt
            if context:
                system_content += f"\n\n{context}"
                
            messages = [{
                "role": "system",
                "content": system_content
            }]
            
            # Extend with current conversation history
            messages.extend(self.conversation)
            
            # Call Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["message"]["content"]
                
                # Add assistant response to conversation history
                self.conversation.append({
                    "role": "assistant",
                    "content": reply
                })
                
                # Keep conversation bounded to last 20 messages (10 turns)
                if len(self.conversation) > 20:
                    self.conversation = self.conversation[-20:]
                
                return reply
            else:
                print(f"❌ Ollama error: {response.status_code}")
                # Remove the user message we just added since it failed to get a response
                if self.conversation:
                    self.conversation.pop()
                return None
        
        except requests.ConnectionError:
            print("❌ Cannot connect to Ollama. Ensure Ollama is running: ollama serve")
            if self.conversation:
                self.conversation.pop()
            return None
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            if self.conversation:
                self.conversation.pop()
            return None
    
    def set_model(self, model: str):
        """Set the model to use"""
        self.model = model
        
    def set_system_prompt(self, prompt: str):
        """Set custom system prompt"""
        self.system_prompt = prompt
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation = []

