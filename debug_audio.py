#!/usr/bin/env python3
"""
Debug script to test microphone input and audio processing
Run this to verify your microphone is working before running Jarvis
"""

import time
from stt import test_microphone, listen, transcribe
import numpy as np

def test_basic_audio():
    """Test basic audio recording"""
    print("🎤 Basic Audio Test")
    print("=" * 40)
    
    print("This test will record 3 seconds of audio and show you the levels.")
    print("Please speak something when prompted...")
    input("Press Enter when ready...")
    
    success = test_microphone()
    
    if success:
        print("✅ Basic audio test passed!")
    else:
        print("❌ Basic audio test failed!")
    
    return success

def test_short_listening():
    """Test short listening with transcription"""
    print("\n🎧 Short Listening Test")
    print("=" * 40)
    
    print("This test will listen for 3 seconds and transcribe what you say.")
    print("Please say 'Hey Jarvis' or any other phrase...")
    input("Press Enter when ready...")
    
    try:
        text = listen(duration=3)
        if text.strip():
            print(f"✅ Transcription successful: '{text}'")
            return True
        else:
            print("❌ No transcription received")
            return False
    except Exception as e:
        print(f"❌ Listening test failed: {e}")
        return False

def test_wake_word_detection():
    """Test wake word detection specifically"""
    print("\n🎯 Wake Word Detection Test")
    print("=" * 40)
    
    wake_word = "hey jarvis"
    print(f"Testing wake word detection for: '{wake_word}'")
    print("Please say the wake word clearly...")
    input("Press Enter when ready...")
    
    try:
        text = listen(duration=3)
        if text.strip():
            print(f"📝 You said: '{text}'")
            text_lower = text.lower()
            if wake_word in text_lower:
                print("✅ Wake word detected successfully!")
                return True
            else:
                print(f"❌ Wake word not found in: '{text_lower}'")
                print(f"Looking for: '{wake_word}'")
                return False
        else:
            print("❌ No audio captured")
            return False
    except Exception as e:
        print(f"❌ Wake word test failed: {e}")
        return False

def main():
    """Run all audio tests"""
    print("🔍 Audio Debugging Suite")
    print("=" * 50)
    print("This will help identify any audio input issues.")
    print()
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Basic audio
    if test_basic_audio():
        tests_passed += 1
    
    # Test 2: Short listening
    if test_short_listening():
        tests_passed += 1
    
    # Test 3: Wake word detection
    if test_wake_word_detection():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your audio system is working correctly.")
        print("You can now run: python main.py")
    elif tests_passed > 0:
        print("⚠️ Some tests passed. Check the failed tests above.")
        print("Common issues:")
        print("- Microphone not selected as default input device")
        print("- Microphone permissions not granted")
        print("- Audio levels too low or too high")
    else:
        print("❌ All tests failed. Check your microphone setup:")
        print("- Verify microphone is connected and working")
        print("- Check Windows sound settings")
        print("- Try a different microphone if available")

if __name__ == "__main__":
    main()
