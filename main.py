from stt import listen, listen_enhanced, change_whisper_model, get_available_whisper_models
from tts import speak, change_voice, toggle_bark
from llm import query_llm, reset_llm, set_conversation_context, get_conversation_summary, change_llm_model
import time

# Configuration
WAKE_WORD = "jarvis"
conversation_history = []

# Voice commands for system control
VOICE_COMMANDS = {
    "reset": ["reset", "new context", "clear memory", "start over"],
    "quit": ["quit", "exit", "goodbye", "stop", "bye"],
    "voice": ["change voice", "different voice", "new voice"],
    "model": ["change model", "different model", "switch model"],
    "summary": ["conversation summary", "what did we talk about", "recap"],
    "help": ["help", "commands", "what can you do", "instructions"]
}

def process_voice_command(command_lower):
    """Process voice commands and return True if handled"""
    
    # Reset conversation
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["reset"]):
        reset_llm()
        speak("Conversation context has been reset. How can I help you?")
        return True
    
    # Quit application
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["quit"]):
        speak("Goodbye! It was nice talking with you.")
        return True
    
    # Change voice
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["voice"]):
        # Cycle through available voices
        voices = ["v2/en_speaker_6", "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2"]
        current_voice = getattr(speak, '_current_voice', voices[0])
        try:
            next_voice = voices[(voices.index(current_voice) + 1) % len(voices)]
            change_voice(next_voice)
            speak(f"Voice changed to speaker {next_voice.split('_')[-1]}")
        except Exception as e:
            speak("I can't change voices right now, but I can toggle between Bark and fallback TTS.")
            toggle_bark()
        return True
    
    # Change LLM model
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["model"]):
        models = get_available_whisper_models()
        speak(f"Available models are: {', '.join(models[:5])}. Say 'change to [model name]' to switch.")
        return True
    
    # Get conversation summary
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["summary"]):
        summary = get_conversation_summary()
        speak(summary)
        return True
    
    # Help
    if any(cmd in command_lower for cmd in VOICE_COMMANDS["help"]):
        help_text = """I can help you with various tasks. Here are some voice commands:
        Say 'reset' to clear our conversation, 'change voice' for a different voice,
        'conversation summary' to hear what we discussed, or just ask me anything!"""
        speak(help_text)
        return True
    
    # Check for model change command
    if "change to" in command_lower:
        for model in get_available_whisper_models():
            if model in command_lower:
                change_whisper_model(model)
                speak(f"Whisper model changed to {model}")
                return True
    
    return False

def main():
    """Main conversation loop with enhanced voice interaction and debugging"""
    
    print("🤖 Jarvis is starting up...")
    speak("Hello! I'm Jarvis, your AI assistant. Say 'Hey Jarvis' to wake me up.")
    
    # Set conversation context
    set_conversation_context(
        user_name="User",
        assistant_name="Jarvis",
        conversation_style="friendly",
        response_length="concise"
    )
    
    print("✅ Jarvis is ready! Say 'Hey Jarvis' to begin.")
    print(f"🎯 Listening for wake word: '{WAKE_WORD}'")
    
    while True:
        try:
            # Record short chunk to detect wake word
            print("\n👂 Listening for wake word... (2 second window)")
            text = listen(duration=2.0).lower()
            
            # DEBUG: Show exactly what was heard
            print(f"🔍 Heard: '{text}' (length: {len(text)})")
            
            if text.strip():
                print(f"📝 Transcribed text: '{text}'")
                print(f"🎯 Looking for wake word: '{WAKE_WORD}'")
                print(f"🔍 Contains wake word? {WAKE_WORD in text}")
            else:
                print("⚠️ No audio detected or transcription failed")
            
            if WAKE_WORD in text:
                print("🎯 Wake word detected!")
                speak("Yes? I'm listening.")
                
                # Record actual command with enhanced listening
                print("🎤 Recording your request...")
                command = listen_enhanced(duration=20, silence_threshold=1.0)
                
                if not command.strip():
                    speak("I didn't catch that. Could you repeat?")
                    continue
                
                print(f"📝 You said: {command}")
                
                # Process voice commands first
                if process_voice_command(command.lower()):
                    continue
                
                # Get LLM response
                print("🧠 Processing with AI...")
                response = query_llm(command)
                print(f"🤖 AI Response: {response}")
                
                # Speak the response
                speak(response)
                
                # Small delay before listening again
                time.sleep(0.5)
            else:
                print("⏳ Wake word not detected, continuing to listen...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            speak("Goodbye! Have a great day.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            speak("I encountered an error. Let me try to recover.")
            time.sleep(1)

if __name__ == "__main__":
    main()
