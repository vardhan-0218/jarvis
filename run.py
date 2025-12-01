import multiprocessing
import subprocess
import sys

# To run Jarvis
def startJarvis():
    try:
        print("Jarvis process is running.")
        from main import start
        start()
    except Exception as e:
        print("Error in Jarvis process:", e)
        sys.exit(1)

# To run hotword listener
def listenHotword():
    try:
        print("Hotword process is running.")
        from Backend.feature import hotword
        hotword()
    except Exception as e:
        print("Error in Hotword process:", e)
        sys.exit(1)

if __name__ == '__main__':
    # Start both processes
    p1 = multiprocessing.Process(target=startJarvis, name="JarvisProcess")
    p2 = multiprocessing.Process(target=listenHotword, name="HotwordProcess")

    p1.start()
    p2.start()

    try:
        p1.join()  # Wait for Jarvis to finish
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Terminating processes...")

    # Ensure hotword process stops if still alive
    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stopped.")    
