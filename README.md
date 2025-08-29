# Jarvis Offline Assistant

A sophisticated offline voice assistant powered by local AI models, featuring an **end-to-end voice model approach** for natural conversations.

## 🚀 New End-to-End Voice Model Features

### What Changed
- **Bark TTS Integration**: High-quality, natural-sounding speech synthesis
- **Enhanced STT**: Better speech detection with Voice Activity Detection (VAD)
- **Voice-Optimized LLM**: Responses specifically designed for voice conversations
- **Real-time Processing**: Continuous audio processing with intelligent silence detection
- **Voice Commands**: Natural voice control for system functions

### Benefits Over Traditional Approach
- **Lower Latency**: No intermediate text conversion delays
- **More Natural**: Conversational responses optimized for speech
- **Better Quality**: High-fidelity voice synthesis with Bark
- **Smarter Listening**: Intelligent speech detection and processing
- **Voice Control**: Complete hands-free operation

## 🎯 Key Features

### Voice Interaction
- **Wake Word Detection**: "Hey Jarvis" to activate
- **Natural Conversations**: Speak naturally, get intelligent responses
- **Voice Commands**: Control system functions with your voice
- **Multiple Voices**: Choose from 10 different Bark voice presets

### AI Capabilities
- **Local LLM**: Powered by Ollama with Llama models
- **Conversation Memory**: Remembers context across exchanges
- **Smart Responses**: Concise, natural language optimized for voice
- **Offline Operation**: Works completely without internet

### Advanced Audio Processing
- **Voice Activity Detection**: Intelligent speech detection
- **Real-time Processing**: Continuous audio analysis
- **Noise Handling**: Robust audio processing in various environments
- **Silence Detection**: Automatically stops recording when you finish speaking

## 🛠️ Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Check System Status
```bash
python start.py
```

### 3. Install Ollama & Download Model
```bash
# Install Ollama from https://ollama.ai/
ollama serve
ollama pull llama3.1:8b
```

### 4. Run Jarvis
```bash
python main.py
```

## 🎤 Voice Commands

### System Control
- **"Reset"** - Clear conversation memory
- **"Change voice"** - Switch to different voice preset
- **"Help"** - Get list of available commands
- **"Quit"** - Exit the application

### Information
- **"Conversation summary"** - Hear what you've discussed
- **"Change model"** - Switch Whisper or LLM models
- **"Status"** - Check system status

## ⚙️ Configuration

### Voice Settings
```python
# In config.py
BARK_VOICE_PRESET = "v2/en_speaker_6"  # Change voice
TTS_ENGINE = "bark"  # Use Bark TTS
```

### Audio Settings
```python
SILENCE_THRESHOLD = 0.8  # Seconds of silence to end recording
MAX_RECORDING_DURATION = 20  # Maximum recording time
```

### LLM Settings
```python
LLM_MODEL = "llama3.1:8b"  # Change AI model
LLM_TEMPERATURE = 0.7  # Response creativity
```

## 🔧 Customization

### Adding New Voice Commands
```python
# In main.py, add to VOICE_COMMANDS dictionary
VOICE_COMMANDS["custom"] = ["custom command", "do something"]
```

### Changing Voice Presets
```python
from tts import change_voice
change_voice("v2/en_speaker_0")  # Different voice
```

### Modifying LLM Behavior
```python
from llm import set_conversation_context
set_conversation_context(conversation_style="professional")
```

## 📁 Clean Repository Structure

```
jarvis_offline_assistant/
├── main.py              # Main application with voice commands
├── tts.py              # Enhanced TTS with Bark integration
├── stt.py              # Advanced STT with VAD
├── llm.py              # Voice-optimized LLM interface
├── config.py           # Centralized configuration
├── start.py            # System startup and dependency checker
├── requirements.txt    # Essential dependencies only
└── README.md          # This file
```

## 🎭 Voice Presets

Bark TTS provides 10 different voice presets:
- `v2/en_speaker_0` through `v2/en_speaker_9`
- Each has unique characteristics and personality
- Change voices dynamically with voice commands

## 🔍 Troubleshooting

### Common Issues

**Bark TTS not working:**
- Ensure you have sufficient RAM (Bark models are large)
- Try fallback mode: `toggle_bark()`
- Check PyTorch installation

**Audio not recording:**
- Verify microphone permissions
- Check audio device settings
- Try different audio devices

**LLM responses slow:**
- Use smaller models (e.g., `llama3.1:3b`)
- Ensure Ollama is running locally
- Check system resources

### Performance Tips
- Use `tiny` or `base` Whisper models for faster STT
- Enable GPU acceleration if available
- Close unnecessary applications to free RAM

## 🚀 Getting Started

1. **Check system status:**
   ```bash
   python start.py
   ```

2. **Install dependencies if needed:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama and download model:**
   ```bash
   ollama serve
   ollama pull llama3.1:8b
   ```

4. **Run Jarvis:**
   ```bash
   python main.py
   ```

5. **Start talking:**
   - Say "Hey Jarvis" to wake up
   - Speak naturally - the system detects when you finish
   - Get intelligent, voice-optimized responses

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional voice commands
- More TTS voices
- Better audio processing
- Enhanced conversation capabilities

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🙏 Acknowledgments

- **Bark TTS** - High-quality voice synthesis
- **Whisper** - Accurate speech recognition
- **Ollama** - Local LLM inference
- **OpenAI** - Whisper and Bark models

---

**Ready to experience natural voice conversations?** Run `python start.py` to check your system, then `python main.py` to begin!
