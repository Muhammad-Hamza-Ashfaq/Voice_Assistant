# CodexCue Python Internship -- Project-5__VOICE ASSISTANT (Golden-Project)
# Muhammad Hamza Ashfaq -- h.ashfaq16@gmail.com

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import random
from tkinter import *

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("500x400+400+100")
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) #female voice

        self.status_label = Label(root, text="Assistant: Ready", font=("Helvetica", 14), fg="green" )
        self.status_label.pack(pady=20)

        self.output_text = Text(root, height=10, width=50, font=("Helvetica", 12))
        self.output_text.pack(pady=10)

        button_frame = Frame(root)
        button_frame.pack(pady=10)

        self.listen_button = Button(button_frame, text="Start Listening", command=self.listen, bg="green", fg="white",font=("Helvetica", 12))
        self.listen_button.pack(side="left", padx=10)

        self.exit_btn = Button(button_frame, text="Exit", command=root.quit, bg="red", fg="white", font=("Helvetica", 12))
        self.exit_btn.pack(side="left", padx=10)


        self.speak("Hello, I'm your Python Voice Assistant. How can I help you Today?")


    def speak(self, text):
        self.output_text.insert(END, f"Assistant: {text}\n")
        self.output_text.see(END)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.status_label.config(text="Listening...", fg="blue")
            self.root.update()

            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            self.status_label.config(text="Processing...", fg='orange')
            self.root.update()

            try:
                command = recognizer.recognize_google(audio).lower()
                self.output_text.insert(END, f"You:{command}\n")
                self.output_text.see(END)
                self.process_command(command)
            
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that, Could you repeat please?")

            except sr.RequestError:
                self.speak("Sorry, my speech service is down. Please try again later.")

            except Exception as e:
                self.speak(f"An Error Occurred: {str(e)}")
            
            self.status_label.config(text="Ready", fg="green")

    def process_command(self, command):
        if 'hello' in command or 'hi' in command:
            responses = ["Hello there!", "Hi!", "Hey", "Greetings"]
            self.speak(random.choice(responses))

        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")

        
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today's date is {current_date}")

        elif "what are you doing" in command:
            self.speak("I am just talking to you!")
        
        elif 'search' in command or 'google' in command:
            self.speak("What would you like me to search for?")
            with sr.Microphone() as source:
                audio = sr.Recognizer().listen(source)
                try:
                    query = sr.Recognizer().recognize_google(audio)
                    url = f"https://google.com/search?q={query}"
                    webbrowser.open(url)
                    self.speak(f"Here are the search results for {query}")
                except:
                    self.speak("Sorry, I didn't catch that.")
            
        
        elif "wikipedia" in command:
            self.speak("What would you like me to search on Wikipedia?")
            with sr.Microphone() as source:
                audio = sr.Recognizer().listen(source)
                try:
                    query = sr.Recognizer().recognize_google(audio)
                    result = wikipedia.summary(query, sentences=2)

                    self.speak(f"According to Wikipedia...")
                    self.speak(result)
                except:
                    self.speak("Sorry, I couldn't find that on Wikipedia.")

        
        elif "open" in command:
            if 'youtube' in command:
                webbrowser.open("https://youtube.com")
                self.speak("Opening Youtube")
            
            elif "github" in command:
                webbrowser.open("https://github.com")
                self.speak("Opening Github")
            
            else:
                self.speak("I can open Youtube or Github, which one would you like?")

        elif "play music" in command:
            music_dir = os.path.expanduser('C:\\Users\\Hamza\\Downloads')
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, random.choice(songs)))
                    self.speak("Playing Music")

                else:
                    self.speak("No music files found in your music directory")
            else:
                self.speak("Music directory not found")

        elif "thank you" in command or "thanks" in command:
            self.speak("You're welcome!")

        elif 'exit' in command or 'bye' in command or 'quit' in command or 'good bye' in command:
            self.speak("Goodbye! Have a great day!")
            self.root.quit()

        else:
            self.speak("I'm not sure I understand. Can you try a different command?")                


if __name__ == '__main__':
    root = Tk()
    app = VoiceAssistant(root)
    root.mainloop()