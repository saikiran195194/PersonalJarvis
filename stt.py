import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import webrtcvad
import threading
import queue
import time

# Load Whisper once
stt_model = WhisperModel("large-v3", device="cpu")
FS = 16000  # Sampling rate

class EnhancedListener:
    """
    Enhanced audio listener with real-time processing and better silence detection
    """
    def __init__(self, sample_rate=16000, chunk_duration=0.1):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration)
        
        # Initialize VAD for better speech detection
        try:
            self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        except Exception as e:
            print(f"VAD initialization failed: {e}")
            self.vad = None
        
        # Audio processing queues
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for real-time audio processing"""
        if status:
            print(f"Audio callback status: {status}")
        
        # Convert to 16-bit PCM for VAD
        audio_chunk = (indata[:, 0] * 32767).astype(np.int16)
        self.audio_queue.put(audio_chunk)
    
    def _is_speech(self, audio_chunk):
        """Detect if audio chunk contains speech using VAD"""
        if self.vad is None:
            # Fallback to RMS-based detection
            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32)**2))
            return rms > 0.01
        
        try:
            # VAD expects 16-bit PCM at 16kHz
            if len(audio_chunk) >= 160:  # Minimum frame size for VAD
                return self.vad.is_speech(audio_chunk.tobytes(), self.sample_rate)
        except Exception:
            pass
        
        return True  # Default to speech if VAD fails
    
    def listen_continuous(self, duration=20, silence_threshold=0.8):
        """
        Listen continuously with real-time speech detection.
        Returns transcribed text when silence is detected.
        """
        audio_buffer = []
        last_speech_time = time.time()
        start_time = time.time()
        
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=self.chunk_size,
            callback=self._audio_callback
        ) as stream:
            self.is_listening = True
            
            while True:
                try:
                    # Get audio chunk from queue
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    
                    # Check if it's speech
                    if self._is_speech(audio_chunk):
                        last_speech_time = time.time()
                        audio_buffer.append(audio_chunk.astype(np.float32) / 32767)
                    
                    # Check for silence
                    current_time = time.time()
                    if (current_time - last_speech_time) > silence_threshold:
                        break
                    
                    # Hard time limit
                    if (current_time - start_time) > duration:
                        break
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Audio processing error: {e}")
                    break
            
            self.is_listening = False
        
        if audio_buffer:
            # Concatenate all audio chunks
            full_audio = np.concatenate(audio_buffer)
            return transcribe(full_audio)  # Use the global transcribe function
        else:
            return ""

def record_audio(duration=20, silence_threshold=0.01, end_silence=0.8):
    """
    Records audio from the default mic until user stops speaking.
    Returns numpy array.
    """
    print(f"🎤 Starting audio recording for {duration} seconds...")
    audio_buffer = []
    start_time = 0
    last_speech_time = None
    
    # Show audio levels during recording
    print("📊 Audio levels (speak now): ", end="", flush=True)

    with sd.InputStream(samplerate=FS, channels=1, dtype="float32") as stream:
        while True:
            chunk, _ = stream.read(int(0.1 * FS))  # 100ms chunks
            chunk = np.squeeze(chunk)
            audio_buffer.append(chunk)

            # Calculate and display audio level
            rms = np.sqrt(np.mean(chunk**2))
            level_bars = int(rms * 50)  # Scale RMS to visual bars
            level_display = "█" * level_bars + "░" * (10 - level_bars)
            print(f"\r📊 Audio levels: [{level_display}] RMS: {rms:.4f}", end="", flush=True)

            now = start_time + len(audio_buffer)*0.1
            
            if rms > silence_threshold:
                last_speech_time = now

            # Stop after silence
            if last_speech_time and (now - last_speech_time) > end_silence:
                break

            # Hard limit
            if (len(audio_buffer) * 0.1) > duration:
                break
    
    print(f"\n✅ Recording complete. Captured {len(audio_buffer) * 0.1:.1f} seconds of audio.")
    return np.concatenate(audio_buffer)

def transcribe(audio):
    """
    Transcribe numpy audio array with Whisper.
    Returns lowercase string.
    """
    try:
        print("🔄 Transcribing audio...")
        segments, _ = stt_model.transcribe(audio)
        text = "".join([s.text for s in segments]).strip()
        print(f"✅ Transcription complete: '{text}'")
        return text
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return ""

# Optional helper to keep main.py unchanged
def listen(duration=20):
    print(f"🎧 Listening for {duration} seconds...")
    audio = record_audio(duration=duration)
    if audio.size == 0:
        print("⚠️ No audio captured!")
        return ""
    return transcribe(audio)

def listen_enhanced(duration=20, silence_threshold=0.8):
    """
    Enhanced listening with better speech detection and real-time processing
    """
    listener = EnhancedListener()
    return listener.listen_continuous(duration, silence_threshold)

def get_available_whisper_models():
    """Get list of available Whisper models"""
    return [
        "tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"
    ]

def change_whisper_model(model_name):
    """Change the Whisper model being used"""
    global stt_model
    try:
        stt_model = WhisperModel(model_name, device="cpu")
        print(f"Whisper model changed to: {model_name}")
    except Exception as e:
        print(f"Failed to change Whisper model: {e}")

def test_microphone():
    """Test microphone input to verify audio is being received"""
    print("🎤 Testing microphone input...")
    print("Please speak something for 3 seconds...")
    
    try:
        with sd.InputStream(samplerate=FS, channels=1, dtype="float32") as stream:
            audio_buffer = []
            start_time = time.time()
            
            while time.time() - start_time < 3:
                chunk, _ = stream.read(int(0.1 * FS))
                chunk = np.squeeze(chunk)
                audio_buffer.append(chunk)
                
                # Show real-time audio levels
                rms = np.sqrt(np.mean(chunk**2))
                level_bars = int(rms * 50)
                level_display = "█" * level_bars + "░" * (10 - level_bars)
                print(f"\r📊 Audio: [{level_display}] RMS: {rms:.4f}", end="", flush=True)
                
                time.sleep(0.1)
            
            print(f"\n✅ Microphone test complete. Captured {len(audio_buffer) * 0.1:.1f} seconds.")
            
            if audio_buffer:
                full_audio = np.concatenate(audio_buffer)
                max_level = np.max(np.abs(full_audio))
                avg_level = np.mean(np.abs(full_audio))
                print(f"📊 Audio stats - Max: {max_level:.4f}, Avg: {avg_level:.4f}")
                
                if max_level < 0.01:
                    print("⚠️ Audio levels are very low. Check microphone settings.")
                elif max_level > 0.9:
                    print("⚠️ Audio levels are very high. Check microphone settings.")
                else:
                    print("✅ Audio levels look good!")
                
                return True
            else:
                print("❌ No audio captured!")
                return False
                
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False
