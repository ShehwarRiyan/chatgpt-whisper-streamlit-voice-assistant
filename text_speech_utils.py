import openai
import sounddevice as sd
import audiofile as af
from scipy.io.wavfile import write
from gtts import gTTS

import multiprocessing
import pyttsx3
import keyboard

def say(text):
		p = multiprocessing.Process(target=pyttsx3.speak, args=(text,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('enter'):
				p.terminate()
			else:
				continue
		p.join()


def record_audio(filename, sec, sr = 44100):
    audio = sd.rec(int(sec * sr), samplerate=sr, channels=2, blocking=False)
    sd.wait()
    write(filename, sr, audio)

#def record_audio_manual(filename, sr = 44100):
    #input("  ** Press enter to start recording **")
    #audio = sd.rec(int(10 * sr), samplerate=sr, channels=2)
    i#nput("  ** Press enter to stop recording **")
    #sd.stop()
    #write(filename, sr, audio) 

def record_audio_manual(filename, sr=44100):
    """Records audio manually after user prompt."""

    # List available audio devices
    print("Available audio devices:")
    for i, device in enumerate(sd.query_devices()):
        print(f"{i}: {device['name']}")

    # Get user input for device selection
    selected_device = int(input("Enter the device index to use: "))

    input("  ** Press enter to start recording **")
    try:
        # Record audio using the selected device
        audio = sd.rec(int(10 * sr), samplerate=sr, channels=2, device=selected_device)  # Specify device
        input("  ** Press enter to stop recording **")
        sd.stop()
        # ... (rest of your function)

    except sd.PortAudioError as e:
        print(f"Error recording audio: {e}")
        # Handle the error appropriately (e.g., exit, retry, etc.)

def play_audio(filename):
    signal, sr = af.read(filename)
    sd.play(signal, sr)

def transcribe_audio(filename):
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    return transcript

def translate_audio(filename):
    audio_file= open(filename, "rb")
    translation = openai.Audio.translate("whisper-1", audio_file)
    audio_file.close()
    return translation

def save_text_as_audio(text, audio_filename):
    myobj = gTTS(text=text, lang='en', slow=False)  
    myobj.save(audio_filename)



