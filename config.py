"""
Configuration file for Jarvis Offline Assistant
Centralizes all settings for easy customization
"""

# Voice Assistant Configuration
ASSISTANT_NAME = "Jarvis"
WAKE_WORD = "hey jarvis"
WAKE_WORD_ALTERNATIVES = ["jarvis", "hey jarvis", "wake up jarvis"]

# Audio Configuration
SAMPLE_RATE = 16000
CHUNK_DURATION = 0.1  # seconds
SILENCE_THRESHOLD = 0.8  # seconds of silence to end recording
MAX_RECORDING_DURATION = 20  # maximum recording time in seconds

# TTS (Text-to-Speech) Configuration
TTS_ENGINE = "bark"  # Options: "bark", "pyttsx3", "hybrid"
BARK_VOICE_PRESET = "v2/en_speaker_6"  # Default voice
BARK_FALLBACK_ENABLED = True

# Available Bark voice presets
BARK_VOICES = [
    "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2",
    "v2/en_speaker_3", "v2/en_speaker_4", "v2/en_speaker_5",
    "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", "v2/en_speaker_9"
]

# STT (Speech-to-Text) Configuration
STT_ENGINE = "whisper"  # Options: "whisper", "enhanced"
WHISPER_MODEL = "large-v3"  # Options: "tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"
WHISPER_DEVICE = "cpu"  # Options: "cpu", "cuda" (if available)

# LLM Configuration
LLM_PROVIDER = "ollama"  # Options: "ollama", "local", "api"
LLM_MODEL = "llama3.1:8b"  # Default model
LLM_TEMPERATURE = 0.7
LLM_TOP_P = 0.9
LLM_MAX_TOKENS = 150  # Optimized for voice responses

# Conversation Configuration
MAX_CONVERSATION_HISTORY = 10  # Number of exchanges to keep in context
CONVERSATION_STYLE = "friendly"  # Options: "friendly", "professional", "casual"
RESPONSE_LENGTH = "concise"  # Options: "concise", "detailed", "natural"

# Voice Commands Configuration
VOICE_COMMANDS = {
    "reset": ["reset", "new context", "clear memory", "start over", "forget everything"],
    "quit": ["quit", "exit", "goodbye", "stop", "bye", "shut down"],
    "voice": ["change voice", "different voice", "new voice", "switch voice"],
    "model": ["change model", "different model", "switch model", "use different model"],
    "summary": ["conversation summary", "what did we talk about", "recap", "summary"],
    "help": ["help", "commands", "what can you do", "instructions", "capabilities"],
    "status": ["status", "how are you", "are you working", "system status"]
}

# UI Configuration
ENABLE_CONSOLE_OUTPUT = True
ENABLE_EMOJIS = True
ENABLE_TIMESTAMPS = True
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"

# Performance Configuration
ENABLE_MODEL_PRELOADING = True
ENABLE_AUDIO_CACHING = False
MAX_AUDIO_CACHE_SIZE = 100  # MB

# Error Handling Configuration
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds
ENABLE_FALLBACK_MODE = True

# Development Configuration
DEBUG_MODE = False
SAVE_AUDIO_FILES = False
AUDIO_OUTPUT_DIR = "audio_outputs"

def get_config():
    """Return a dictionary with all configuration values"""
    return {key: value for key, value in globals().items() 
            if not key.startswith('_') and key.isupper()}

def update_config(**kwargs):
    """Update configuration values"""
    for key, value in kwargs.items():
        if key.upper() in globals():
            globals()[key.upper()] = value
        else:
            print(f"Warning: Unknown configuration key '{key}'")

def print_config():
    """Print current configuration"""
    print("🔧 Current Configuration:")
    for key, value in get_config().items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print_config()
