import pyttsx3
import speech_recognition as sr
import eel
import time

# ------------------ SPEAK FUNCTION ------------------
def speak(text: str):
    """Convert text to speech and send message to frontend via Eel"""
    # Import settings here to avoid circular import
    try:
        from Backend.settings import get_tts_engine, is_tts_enabled
        
        # Check if TTS is enabled
        if not is_tts_enabled():
            # Still send to frontend but don't speak
            try:
                eel.DisplayMessage(text)
                eel.receiverText(text)
            except Exception:
                pass
            return
        
        # Use configured TTS engine
        Backend = get_tts_engine()
    except ImportError:
        # Fallback to default settings if settings module not available
        Backend = pyttsx3.init('sapi5')
        voices = Backend.getProperty('voices')
        if len(voices) > 1:
            Backend.setProperty('voice', voices[1].id)
        else:
            Backend.setProperty('voice', voices[0].id)
        Backend.setProperty('rate', 174)

    # Send text to frontend safely
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
    except Exception:
        pass

    # Speak
    Backend.say(text)
    Backend.runAndWait()

# ------------------ LISTEN FUNCTION ------------------
@eel.expose
def takecommand():
    """Capture user voice input and return as text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            eel.DisplayMessage("Listening...")
        except Exception:
            pass

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except Exception as e:
            print(f"Microphone Error: {e}")
            speak("Microphone not available or busy.")
            return "COMMAND_NOT_RECOGNIZED"

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        time.sleep(1)
    except sr.WaitTimeoutError:
        print("Timeout error")
        speak("I didn't hear anything.")
        return "COMMAND_NOT_RECOGNIZED"
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("I didn't catch that. Could you say it again?")
        return "COMMAND_NOT_RECOGNIZED"
    except Exception as e:
        print(f"Recognition Error: {e}")
        speak("I encountered a recognition error.")
        return "COMMAND_NOT_RECOGNIZED"

    return query.lower()

# ------------------ COMMAND HANDLER ------------------
@eel.expose
def allCommands(message=1):
    """Process either voice command or text command"""
    if message == 1:
        query = takecommand()
        if query == "COMMAND_NOT_RECOGNIZED":
            eel.ShowHood()
            return
        print(query)
        eel.senderText(query)
    else:
        query = message
        print("Text command: ", query)
        eel.senderText(query)

    try:
        # ✅ Import feature functions here (lazy import) to avoid circular import
        from Backend import feature  

        # ----------- OPEN COMMANDS -----------
        if "open" in query:
            feature.openCommand(query)

        # ----------- YOUTUBE -----------
        elif "on youtube" in query:
            feature.PlayYoutube(query)

        # ----------- CONTACT-BASED COMMANDS -----------
        elif any(cmd in query for cmd in ["send message", "phone call", "video call"]):
            contact_no, name = feature.findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("What message to send")
                        message_content = takecommand()
                        if message_content != "COMMAND_NOT_RECOGNIZED":
                            feature.sendMessage(message_content, contact_no, name)
                        else:
                            speak("Message canceled.")

                    elif "phone call" in query:
                        feature.makeCall(name, contact_no)
                    else:
                        speak("Please try again")

                elif "whatsapp" in preferance:
                    message_type = 'video call'
                    whatsapp_message_content = ""

                    if "send message" in query:
                        message_type = 'message'
                        speak("What message to send")
                        whatsapp_message_content = takecommand()
                        if whatsapp_message_content == "COMMAND_NOT_RECOGNIZED":
                            speak("Message canceled.")
                            eel.ShowHood()
                            return

                    elif "phone call" in query:
                        message_type = 'call'

                    feature.whatsApp(contact_no, whatsapp_message_content, message_type, name)

                else:
                    speak("I didn't understand the mode. Please try the command again.")

        # ----------- DEFAULT CHATBOT -----------
        else:
            feature.chatBot(query)

    except Exception as e:
        print(f"Command Execution Error: {e}")
        speak("I encountered an error while processing your command.")

    eel.ShowHood()