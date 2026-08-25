# pip install pyaudio

import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import subprocess

# `sapi5` is the Windows speech driver. `nsss` is the equivalent on macOS.
engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    sender = os.environ.get('GMAIL_ADDRESS')
    app_password = os.environ.get('GMAIL_APP_PASSWORD')
    if not sender or not app_password:
        raise RuntimeError(
            'Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD before using email commands.'
        )

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, app_password)
    server.sendmail(sender, to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            # Change this to the folder where you keep your music on this Mac.
            music_dir = os.path.expanduser('~/Music')
            songs = os.listdir(music_dir)
            print(songs)    
            if songs:
                subprocess.run(['open', os.path.join(music_dir, songs[0])], check=False)
            else:
                speak("I could not find any music files.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            subprocess.run(['open', '-a', 'Visual Studio Code'], check=False)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = os.environ.get('GMAIL_RECIPIENT')
                if not to:
                    raise RuntimeError('Set GMAIL_RECIPIENT before using this command.')
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")    
        else:
            print("No query matched")
