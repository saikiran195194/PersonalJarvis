# Example using Ollama local API (replace with your preferred offline model setup)
import subprocess
import json
import time

class VoiceChatLLM:
    """
    Enhanced LLM class specifically designed for voice conversations
    """
    def __init__(self, model="llama3.1:8b"):
        self.model = model
        self.history = []
        self.conversation_context = {
            "user_name": "User",
            "assistant_name": "Jarvis",
            "conversation_style": "friendly",
            "response_length": "concise"
        }
        
        # Voice-specific system prompt
        self.system_prompt = """You are Jarvis, a helpful AI assistant. You communicate through voice, so:
1. Keep responses concise and natural for speech (1-2 sentences max)
2. Use conversational language, not formal writing
3. Be helpful, friendly, and engaging
4. Avoid long lists or complex formatting
5. Respond as if in a natural conversation"""
    
    def ask(self, prompt: str, context: str = None) -> str:
        """
        Sends prompt + conversation history to local LLM and returns response.
        Optimized for voice conversations.
        """
        # Add context if provided
        if context:
            full_prompt = f"Context: {context}\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        # Add to conversation history
        self.history.append({"role": "user", "content": full_prompt})
        
        try:
            # Prepare messages for the model
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.history[-10:])  # Keep last 10 exchanges for context
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 150  # Limit for voice responses
                }
            }
            
            # Call Ollama CLI and capture output
            result = subprocess.run(
                ["ollama", "chat", "--model", self.model, "--json"],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=30  # Add timeout
            )
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response = response_data.get("response", "I'm sorry, I didn't get that.")
            else:
                response = f"Error: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            response = "I'm taking too long to respond. Please try again."
        except Exception as e:
            response = f"Error querying LLM: {e}"
        
        # Clean up response for voice
        response = self._clean_response_for_voice(response)
        
        # Add to conversation history
        self.history.append({"role": "assistant", "content": response})
        
        return response
    
    def _clean_response_for_voice(self, response: str) -> str:
        """
        Clean up LLM response to be more suitable for voice output
        """
        # Remove markdown formatting
        response = response.replace("*", "").replace("_", "").replace("`", "")
        
        # Remove URLs or replace with simple text
        import re
        response = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                         'a website', response)
        
        # Limit length for voice
        if len(response) > 200:
            response = response[:200] + "..."
        
        # Ensure it ends with proper punctuation
        if not response.endswith(('.', '!', '?')):
            response += '.'
        
        return response.strip()
    
    def reset(self):
        """Reset conversation history"""
        self.history.clear()
        print("Conversation history cleared.")
    
    def set_context(self, **kwargs):
        """Set conversation context parameters"""
        self.conversation_context.update(kwargs)
    
    def get_conversation_summary(self) -> str:
        """Get a brief summary of the conversation"""
        if not self.history:
            return "No conversation yet."
        
        user_messages = [msg["content"] for msg in self.history if msg["role"] == "user"]
        if len(user_messages) <= 3:
            return f"Recent topics: {', '.join(user_messages[-3:])}"
        else:
            return f"Recent topics: {', '.join(user_messages[-3:])} and {len(user_messages)-3} more"
    
    def change_model(self, new_model: str):
        """Change the LLM model being used"""
        self.model = new_model
        print(f"LLM model changed to: {new_model}")

class ChatLLM:
    def __init__(self):
        self.history = []

    def ask(self, prompt: str) -> str:
        """
        Sends prompt + conversation history to local LLM and returns response.
        Example uses Ollama CLI.
        """
        self.history.append({"role": "user", "content": prompt})
        try:
            payload = {
                "model": "llama3.1:8b",
                "messages": self.history
            }
            # Call Ollama CLI and capture output
            result = subprocess.run(
                ["ollama", "chat", "--model", "llama3.1:8b", "--json"],
                input=json.dumps(payload),
                text=True,
                capture_output=True
            )
            response = json.loads(result.stdout)["response"]
        except Exception as e:
            response = f"Error querying LLM: {e}"

        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.history.clear()

# Global helpers for convenience
_brain = VoiceChatLLM()  # Use enhanced voice-optimized LLM

def query_llm(prompt: str, context: str = None):
    return _brain.ask(prompt, context)

def reset_llm():
    _brain.reset()

def set_conversation_context(**kwargs):
    """Set conversation context parameters"""
    _brain.set_context(**kwargs)

def get_conversation_summary():
    """Get conversation summary"""
    return _brain.get_conversation_summary()

def change_llm_model(model_name: str):
    """Change the LLM model"""
    _brain.change_model(model_name)
