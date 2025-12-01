#!/usr/bin/env python3
"""
Jarvis Setup Script
This script sets up the Jarvis AI Assistant by:
1. Installing required dependencies
2. Initializing the database
3. Checking system requirements
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")
    try:
        from Backend.db import initialize_database
        initialize_database()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def check_audio_files():
    """Check if required audio files exist"""
    audio_path = "Frontend/assets/audio/start_sound.mp3"
    if os.path.exists(audio_path):
        print("✅ Audio files found!")
        return True
    else:
        print(f"⚠️  Audio file not found: {audio_path}")
        print("The application will work but without startup sound.")
        return False

def main():
    """Main setup function"""
    print("🤖 Jarvis AI Assistant Setup")
    print("=" * 40)
    
    success = True
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Initialize database
    if not initialize_database():
        success = False
    
    # Check audio files
    check_audio_files()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nTo start Jarvis:")
        print("1. Run: python main.py (for single process)")
        print("2. Run: python run.py (for multi-process with hotword)")
    else:
        print("❌ Setup completed with errors. Please check the messages above.")
    
    print("\nNote: Make sure you have:")
    print("- A working microphone")
    print("- Internet connection for AI features")
    print("- Valid Google API key in Backend/config.py")

if __name__ == "__main__":
    main()
