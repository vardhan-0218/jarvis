import speech_recognition as sr
import pyaudio  # Import PyAudio explicitly to test the driver connection

def test_mic_hardware():
    print("--- Running Microphone Hardware Test ---")
    
    try:
        # Check PyAudio installation first
        p = pyaudio.PyAudio()
        print(f"PyAudio version: {pyaudio.__version__}")
        print(f"Found {p.get_device_count()} audio devices.")
        
        # List devices for clarity
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"  Device {i}: {info['name']} (Inputs: {info['maxInputChannels']}, Outputs: {info['maxOutputChannels']})")
        
        p.terminate()

    except Exception as e:
        print("\n❌ CRITICAL FAILURE: PyAudio/Driver Error.")
        print("Error details:", e)
        print("Resolution: Uninstall PyAudio and reinstall the correct wheel (.whl) file.")
        return

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("\n✅ Hardware Check Passed. Now testing recognition.")
        print("Listening for 5 seconds... SAY SOMETHING NOW.")
        
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print("\n🎉 SUCCESS: Recognized text:", text)
        except sr.WaitTimeoutError:
            print("\n⚠️ TIMEOUT: Heard nothing within 5 seconds.")
        except sr.UnknownValueError:
            print("\n❌ FAILURE: Could not understand audio (too quiet or too loud).")
        except Exception as e:
            print(f"\n❌ UNEXPECTED RECOGNITION ERROR: {e}")

if __name__ == '__main__':
    test_mic_hardware()
