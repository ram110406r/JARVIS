"""Groq LLM Service

Handles communication with Groq Cloud API
"""

import requests
from typing import Optional


class GroqService:
    """Interface to Groq Cloud API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.groq.com/openai/v1"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = "llama3-8b-8192"  # Default model
        self.conversation = []
        self.system_prompt = (
            "You are JARVIS, an intelligent desktop AI companion for developers and founders.\n"
            "Your design is inspired by HeyClicky, but you are focused on productivity, coding, and startup workflows.\n"
            "Be concise, helpful, and direct."
        )
    
    def chat(self, message: str, context: str = "") -> Optional[str]:
        """
        Send message to Groq and get response
        
        Args:
            message: User message
            context: Optional context to prepend to the system prompt
        
        Returns:
            Response text or None if error
        """
        if not self.api_key:
            print("❌ Groq API key is not configured.")
            return "Error: Groq API key is missing. Please set GROQ_API_KEY in your .env file."
            
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
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Call Groq API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                
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
                print(f"❌ Groq API error: {response.status_code} - {response.text}")
                # Remove the user message we just added since it failed to get a response
                if self.conversation:
                    self.conversation.pop()
                return None
        
        except requests.ConnectionError:
            print("❌ Cannot connect to Groq API. Ensure you have internet access.")
            if self.conversation:
                self.conversation.pop()
            return None
        except Exception as e:
            print(f"❌ Groq error: {e}")
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
