# Assuming this is in your main_eel.py or a similar launcher file

import os
import eel
import subprocess
import time

# Ensure imports are correct based on your file structure
from Backend.feature import playAssistantSound
from Backend.command import speak
from Backend.db import initialize_database
from Backend.settings import load_settings

# Initialize database and settings on startup
try:
    initialize_database()
    load_settings()
    print("✅ Database and settings initialized")
except Exception as e:
    print(f"Initialization error: {e}")

# Authentication import (commented out for now to avoid errors)
# from Backend.auth.recoganize import AuthenticateFace 

def start():
    # Initialize frontend folder
    eel.init("Frontend")

    # Play startup sound (Must match the exposed name: playAssistantSound)
    # NOTE: The original code calls this outside the exposed function, 
    # which is fine, but may run before the browser is ready.
    playAssistantSound()

    # CRITICAL FIX: The init function should be called by the browser's JS,
    # and its logic needs to be updated to use the modern JS functions.
    @eel.expose
    def init():
        try:
            # 1. Start device.bat (ADB setup) - Optional, skip if fails
            try:
                result = subprocess.run([r'device.bat'], timeout=10, capture_output=True, text=True)
                if result.returncode != 0:
                    print("ADB setup completed with warnings (Android features may be limited)")
            except Exception as e:
                print(f"ADB setup skipped: {e}")
            
            # 2. Skip Authentication - Show Welcome Animation
            eel.hideLoader()()
            
            # Show welcome animation while speaking
            eel.showWelcomeAnimation()()
            speak("Hello, Welcome Sir")
            time.sleep(1)
            
            # Show system ready animation
            eel.showSystemReady()()
            speak("How can I Help You")
            time.sleep(1.5)
            
            # Hide animations and go to main UI
            eel.hideWelcomeAnimations()()
            eel.show_main_ui()()         # Hides the starting section (#Start), shows the main UI (#Oval)
            
            playAssistantSound()         # Optional: Plays a final ready sound
            
            return {"status": "ok", "authenticated": True}
            
            # ========== FACE AUTHENTICATION (COMMENTED OUT) ==========
            # Uncomment the section below to enable face authentication
            """
            # 2. Hide Loader and Start Auth
            eel.hideLoader()()
            speak("Ready for Face Authentication")
            
            # CRITICAL: Authentication call (assuming it returns 1 for success)
            # from Backend.auth.recoganize import AuthenticateFace
            # flag = AuthenticateFace() 
            flag = 1 # Using mock success for demonstration
            
            if flag == 1:
                # Auth Success Sequence
                eel.hideFaceAuth()()         # Hides FaceAuth, shows FaceAuthSuccess
                speak("Face Authentication Successful")
                time.sleep(1)
                
                eel.hideFaceAuthSuccess()()  # Hides FaceAuthSuccess, shows HelloGreet
                time.sleep(1)

                speak("Hello, Welcome Sir, How can I Help You")
                
                # CRITICAL FIX: Call the correct consolidated JS function
                eel.show_main_ui()()         # Hides the starting section (#Start), shows the main UI (#Oval)
                
                playAssistantSound()         # Optional: Plays a final ready sound
                
                return {"status": "ok", "authenticated": True}
            else:
                speak("Face Authentication Fail")
                # Optional: Add eel.hideStart()() to reset the screen back to the main UI flow
                return {"status": "ok", "authenticated": False}
            """

        except Exception as e:
            print("Error in init():", e)
            speak("Authentication system error.")
            return {"status": "error", "message": str(e)}

    # Open the web app (NOTE: Running this before eel.start can cause issues)
    os.system('start msedge.exe --app="http://localhost:9000/index.html"')

    # Start the Eel server
    # NOTE: We set the initial page and let JavaScript call init() when it loads.
    eel.start("index.html", mode=None, host='localhost', port=9000, block=True)

# Start the application
if __name__ == "__main__":
    start()