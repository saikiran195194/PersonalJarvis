#!/usr/bin/env python3
"""
Clean startup script for Jarvis Offline Assistant
This script initializes the system and runs Jarvis with the end-to-end voice model
"""

import sys
import time

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        ("numpy", "numpy"),
        ("sounddevice", "sounddevice"),
        ("scipy", "scipy"),
        ("faster_whisper", "faster-whisper"),
        ("webrtcvad", "webrtcvad"),
        ("torch", "torch"),
        ("pyttsx3", "pyttsx3")
    ]
    
    missing_modules = []
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_modules.append(package_name)
    
    # Check Bark separately (optional)
    try:
        from bark import SAMPLE_RATE
        print("✅ Bark TTS - Available")
        bark_available = True
    except ImportError:
        print("⚠️ Bark TTS - Not available (fallback TTS will be used)")
        bark_available = False
    
    if missing_modules:
        print(f"\n❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are available!")
    return True

def initialize_system():
    """Initialize the voice assistant system"""
    print("\n🚀 Initializing Jarvis...")
    
    try:
        # Import core modules
        from tts import speak
        from stt import listen
        from llm import query_llm
        
        print("✅ Core modules loaded successfully")
        
        # Test TTS
        print("🎤 Testing voice synthesis...")
        speak("System initialized successfully.")
        
        return True
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return False

def main():
    """Main startup function"""
    print("🤖 Jarvis Offline Assistant - Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start due to missing dependencies.")
        sys.exit(1)
    
    # Initialize system
    if not initialize_system():
        print("\n❌ System initialization failed.")
        sys.exit(1)
    
    print("\n🎉 Jarvis is ready!")
    print("\n📝 Next steps:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Download a model: ollama pull llama3.1:8b")
    print("3. Run Jarvis: python main.py")
    
    print("\n💡 Tips:")
    print("- Say 'Hey Jarvis' to wake up the assistant")
    print("- Use voice commands like 'help', 'reset', 'change voice'")
    print("- The system will automatically fall back to simpler TTS if needed")
    
    print("\n🚀 Ready to launch Jarvis!")

if __name__ == "__main__":
    main()
