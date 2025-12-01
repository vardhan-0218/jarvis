#!/usr/bin/env python3
"""
Jarvis Verification and Startup Script
Performs quick checks before starting Jarvis to ensure smooth operation
"""

import os
import sys

def quick_verification():
    """Perform quick verification checks"""
    print("🔍 Quick Verification Checks...")
    
    issues = []
    
    # Check critical files
    critical_files = [
        "Backend/command.py",
        "Backend/feature.py", 
        "Backend/config.py",
        "Frontend/index.html",
        "Frontend/controller.js"
    ]
    
    for file_path in critical_files:
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_path}")
    
    # Check database
    try:
        from Backend.db import initialize_database
        initialize_database()
        print("✅ Database ready")
    except Exception as e:
        issues.append(f"Database issue: {e}")
    
    # Check key imports
    try:
        import eel
        print("✅ Eel imported")
    except ImportError:
        issues.append("Eel not installed - run: pip install eel")
    
    try:
        import pyttsx3
        print("✅ Text-to-speech ready")
    except ImportError:
        issues.append("pyttsx3 not installed - run: pip install pyttsx3")
    
    try:
        import speech_recognition
        print("✅ Speech recognition ready")
    except ImportError:
        issues.append("SpeechRecognition not installed - run: pip install SpeechRecognition")
    
    return issues

def start_jarvis():
    """Start Jarvis application"""
    print("\n🚀 Starting Jarvis AI Assistant...")
    print("=" * 40)
    
    try:
        from main import start
        start()
    except KeyboardInterrupt:
        print("\n👋 Jarvis stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting Jarvis: {e}")
        print("\nTroubleshooting:")
        print("1. Run: python test_complete.py")
        print("2. Check your API key in Backend/config.py")
        print("3. Ensure all dependencies are installed")

def main():
    """Main function"""
    print("🤖 Jarvis AI Assistant - Startup Verification")
    print("=" * 50)
    
    # Quick verification
    issues = quick_verification()
    
    if issues:
        print("\n⚠️  Issues detected:")
        for issue in issues:
            print(f"   - {issue}")
        
        print("\n🔧 Please fix these issues before starting Jarvis")
        print("Run: python test_complete.py for detailed diagnostics")
        return
    
    print("\n✅ All checks passed!")
    
    # Ask user if they want to start
    response = input("\nStart Jarvis now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        start_jarvis()
    else:
        print("👋 Startup cancelled. Run this script again when ready.")

if __name__ == "__main__":
    main()
