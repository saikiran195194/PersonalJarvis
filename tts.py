import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
import os

# Try to import Bark, but provide fallback if it fails
try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    BARK_AVAILABLE = True
    print("✅ Bark TTS successfully imported")
except ImportError as e:
    BARK_AVAILABLE = False
    print(f"⚠️ Bark TTS not available: {e}")
    print("📝 Using fallback TTS systems")

class BarkSpeaker:
    """
    Bark TTS speaker for high-quality voice synthesis
    """
    def __init__(self, voice_preset="v2/en_speaker_6"):
        """
        Initialize Bark TTS with a specific voice preset.
        Available presets: v2/en_speaker_0 through v2/en_speaker_9
        """
        if not BARK_AVAILABLE:
            raise ImportError("Bark TTS is not available. Please install it first.")
            
        self.voice_preset = voice_preset
        self.sample_rate = SAMPLE_RATE
        
        # Preload models for faster inference
        print("🔄 Loading Bark TTS models...")
        preload_models()
        print("✅ Bark TTS models loaded!")
    
    def say(self, text, output_file=None):
        """
        Generate and play audio from text using Bark TTS.
        
        Args:
            text (str): Text to convert to speech
            output_file (str, optional): Path to save audio file
        """
        try:
            # Generate audio using Bark
            audio_array = generate_audio(text, history_prompt=self.voice_preset)
            
            # Normalize audio to prevent clipping
            audio_array = audio_array / np.max(np.abs(audio_array)) * 0.8
            
            # Save to file if specified
            if output_file:
                wavfile.write(output_file, self.sample_rate, audio_array)
            
            # Play audio
            sd.play(audio_array, self.sample_rate)
            sd.wait()  # Wait for audio to finish playing
            
        except Exception as e:
            print(f"Error in Bark TTS: {e}")
            # Fallback to simple beep
            self._fallback_beep()
    
    def _fallback_beep(self):
        """Fallback method if Bark fails"""
        duration = 0.5
        frequency = 440
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        sd.play(audio, self.sample_rate)
        sd.wait()
    
    def change_voice(self, voice_preset):
        """Change the voice preset"""
        self.voice_preset = voice_preset
        print(f"Voice changed to: {voice_preset}")

class FallbackSpeaker:
    """
    Fallback speaker using pyttsx3 or simple audio generation
    """
    def __init__(self):
        self.pyttsx3_available = False
        self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 if available"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            self.pyttsx3_available = True
            print("✅ pyttsx3 TTS initialized as fallback")
        except Exception as e:
            print(f"⚠️ pyttsx3 not available: {e}")
            self.pyttsx3_available = False
    
    def say(self, text, output_file=None):
        """Speak text using available fallback method"""
        if self.pyttsx3_available:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"pyttsx3 failed: {e}")
                self._simple_beep()
        else:
            self._simple_beep()
    
    def _simple_beep(self):
        """Generate a simple beep sound"""
        duration = 0.3
        frequency = 800
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.2 * np.sin(2 * np.pi * frequency * t)
        sd.play(audio, sample_rate)
        sd.wait()

class HybridSpeaker:
    """
    Hybrid speaker that can use both Bark (high quality) and fallback (reliable)
    """
    def __init__(self, use_bark=True, voice_preset="v2/en_speaker_6"):
        self.use_bark = use_bark and BARK_AVAILABLE
        
        if self.use_bark:
            try:
                self.bark_speaker = BarkSpeaker(voice_preset)
                self.fallback_speaker = None
                print("🎤 Using Bark TTS for high-quality voice synthesis")
            except Exception as e:
                print(f"Bark TTS failed to initialize: {e}")
                self.use_bark = False
                self._init_fallback()
        else:
            self._init_fallback()
    
    def _init_fallback(self):
        """Initialize fallback speaker"""
        self.fallback_speaker = FallbackSpeaker()
        print("🎤 Using fallback TTS system")
    
    def say(self, text, output_file=None):
        """Speak text using available TTS method"""
        if self.use_bark and hasattr(self, 'bark_speaker'):
            try:
                self.bark_speaker.say(text, output_file)
            except Exception as e:
                print(f"Bark failed, falling back: {e}")
                self._fallback_say(text)
        else:
            self._fallback_say(text)
    
    def _fallback_say(self, text):
        """Use fallback TTS method"""
        if self.fallback_speaker:
            self.fallback_speaker.say(text)
        else:
            print(f"TTS not available. Text: {text}")
    
    def toggle_bark(self):
        """Toggle between Bark and fallback TTS"""
        if BARK_AVAILABLE:
            self.use_bark = not self.use_bark
            if self.use_bark:
                try:
                    self.bark_speaker = BarkSpeaker()
                    print("✅ Bark TTS enabled")
                except Exception as e:
                    print(f"Failed to enable Bark: {e}")
                    self.use_bark = False
            else:
                print("📝 Bark TTS disabled, using fallback")
        else:
            print("⚠️ Bark TTS is not available")

# Global speaker instance - defaults to Bark if available
try:
    if BARK_AVAILABLE:
        _speaker = HybridSpeaker(use_bark=True)
    else:
        _speaker = HybridSpeaker(use_bark=False)
except Exception as e:
    print(f"Using fallback TTS: {e}")
    _speaker = HybridSpeaker(use_bark=False)

def speak(text: str, output_file=None):
    """Global helper function to speak text"""
    _speaker.say(text, output_file)

def change_voice(voice_preset: str):
    """Change the voice preset for Bark TTS"""
    if hasattr(_speaker, 'bark_speaker') and _speaker.bark_speaker:
        _speaker.bark_speaker.change_voice(voice_preset)
    else:
        print("Voice changing not available with fallback TTS")

def toggle_bark():
    """Toggle between Bark and fallback TTS"""
    _speaker.toggle_bark()

def get_available_voices():
    """Get list of available voice presets"""
    if BARK_AVAILABLE:
        return [
            "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2",
            "v2/en_speaker_3", "v2/en_speaker_4", "v2/en_speaker_5",
            "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", "v2/en_speaker_9"
        ]
    else:
        return ["fallback_only"]
