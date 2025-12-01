#!/usr/bin/env python3
"""
Settings management for Jarvis AI Assistant
Handles user preferences and configuration
"""

import json
import os
import eel
import pyttsx3
from Backend.config import ASSISTANT_NAME

# Settings file path
SETTINGS_FILE = "jarvis_settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "voiceGender": "female",
    "speechRate": 174,
    "voiceVolume": 90,
    "enableTTS": True,
    "aiModel": "gemini-1.5-pro",
    "responseLength": "medium",
    "enableAnimations": True,
    "enableSounds": True,
    "theme": "default",
    "enableHotword": True,
    "hotwordSensitivity": 0.5
}

# Global settings variable
current_settings = DEFAULT_SETTINGS.copy()

def load_settings():
    """Load settings from file or create default"""
    global current_settings
    
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                saved_settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                current_settings = {**DEFAULT_SETTINGS, **saved_settings}
        else:
            current_settings = DEFAULT_SETTINGS.copy()
            save_settings()
    except Exception as e:
        print(f"Error loading settings: {e}")
        current_settings = DEFAULT_SETTINGS.copy()
    
    return current_settings

def save_settings():
    """Save current settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(current_settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")

@eel.expose
def updateSettings(settings):
    """Update settings from frontend"""
    global current_settings
    
    try:
        # Update current settings
        current_settings.update(settings)
        
        # Save to file
        save_settings()
        
        # Apply TTS settings immediately
        apply_tts_settings()
        
        print("Settings updated successfully")
        return {"status": "success", "message": "Settings updated"}
    
    except Exception as e:
        print(f"Error updating settings: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def getSettings():
    """Get current settings"""
    return current_settings

def apply_tts_settings():
    """Apply text-to-speech settings"""
    try:
        # This will be used by the speak function
        pass
    except Exception as e:
        print(f"Error applying TTS settings: {e}")

def get_tts_engine():
    """Get configured TTS engine based on settings"""
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        
        # Apply voice gender setting
        if current_settings.get("voiceGender") == "male" and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        elif len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        elif len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        
        # Apply speech rate
        rate = current_settings.get("speechRate", 174)
        engine.setProperty('rate', rate)
        
        # Apply volume (convert from 0-100 to 0-1)
        volume = current_settings.get("voiceVolume", 90) / 100.0
        engine.setProperty('volume', volume)
        
        return engine
    
    except Exception as e:
        print(f"Error configuring TTS engine: {e}")
        return pyttsx3.init()

def get_ai_model():
    """Get current AI model setting"""
    return current_settings.get("aiModel", "gemini-1.5-pro")

def get_response_length():
    """Get response length preference"""
    return current_settings.get("responseLength", "medium")

def is_tts_enabled():
    """Check if TTS is enabled"""
    return current_settings.get("enableTTS", True)

def is_hotword_enabled():
    """Check if hotword detection is enabled"""
    return current_settings.get("enableHotword", True)

def get_hotword_sensitivity():
    """Get hotword sensitivity setting"""
    return current_settings.get("hotwordSensitivity", 0.5)

def is_sounds_enabled():
    """Check if sounds are enabled"""
    return current_settings.get("enableSounds", True)

def get_response_prefix():
    """Get response prefix based on length setting"""
    length = get_response_length()
    
    if length == "short":
        return "Give a brief answer: "
    elif length == "long":
        return "Give a detailed explanation: "
    else:
        return ""

# Initialize settings on import
load_settings()

if __name__ == "__main__":
    # Test settings functionality
    print("Current settings:", current_settings)
    
    # Test updating settings
    test_settings = {
        "voiceGender": "male",
        "speechRate": 200,
        "aiModel": "gemini-1.5-flash"
    }
    
    result = updateSettings(test_settings)
    print("Update result:", result)
    print("Updated settings:", current_settings)
