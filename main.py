import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import re
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print("You said:", command)
            return command
    except Exception as e:
        print("Error:", e)
        return ""

def guess_number_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    talk("sure boss Let's play a number guessing game I'm thinking of a number between 1 and 100  Try to guess it.")
    while True:
        try:
            guess = take_command()
            attempts += 1
            if "jarvis shut up" in guess:
                talk('Alright, exiting the game.')
                break
            guess = int(guess)
            if guess < number_to_guess:
                talk("Too low. Try again.")
            elif guess > number_to_guess:
                talk("Too high. Try again.")
            else:
                talk(f"Congratulations boss! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break
        except ValueError:
            talk("Please say a number.")

def run_jarvis():
    while True:
        command = take_command()

        if "jarvis shut up" in command:
            talk('Alright, shutting down.')
            break  

        if "weather" in command:
            city = command.replace("weather", "")
            if city != "":
                url = f"https://www.google.com/search?q=weather+{city}"
                webbrowser.open(url)
                talk(f"Retrieving weather for {city}")
            else:
                talk("Please specify a city for weather information.")

        elif "open website" in command:
            website = command.replace("open website", "")
            if website != "":
                url = website.replace(" ", "")
                webbrowser.open(url)
                talk(f"Opening {website}")
            else:
                talk("Please specify the website URL to open.")

        elif "set reminder" in command:
            try:
                time = ""
                content = ""
                time_re = r"\d+(?:( minute| hour| day)(?:s)?)"
                time_match = re.findall(time_re, command)
                for match in time_match:
                    time += match.lower() + " "
                content = command.replace(time, "").replace("set reminder", "")
                pywhatkit.sendwhatmsg_instantly("+91xxxxxxxxxx", content, time)  # Replace with your number
                talk(f"Reminder set for {time} with content: {content}")
            except Exception as e:
                print("Error:", e)
                talk("Sorry boss, I couldn't understand your reminder request. Please try phrasing it differently.")

        elif "cancel reminder" in command:
            try:
                content = command.replace("cancel reminder", "")
                pywhatkit.cancel_reminder("all")
                talk(f"Your reminder '{content}' has been canceled.")
            except Exception as e:
                print("Error:", e)
                talk("Sorry, I couldn't find any reminders to cancel.")

        elif "play a game" in command:
            talk("Sure boss, let's play a game.please say 'number guessing game' to ignite ")
            game_choice = take_command()
            if "number guessing game" in game_choice:
                guess_number_game()
            else:
                talk("I'm sorry boss, I didn't understand which game you want to play.")

        else:
            if 'play' in command:
                song = command.replace('play', '')
                talk('playing' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('The time is ' + time)
            elif 'who is' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            elif 'sing me a song' in command:
                talk('Sorry boss, my voice is not good today. But if you want, I can try to sing you a lullaby.')
            elif 'i am bored' in command:
                talk('Boss, why dont you massage my back for some time?')

def tell_joke():
    jokes = [
        "What do you call a fish with no eyes? Fsh!",
        "What do you call a deer with no eyes? No idea!",
        "What do you call a cow with no legs? Ground beef!"
    ]
    joke = random.choice(jokes)
    talk(joke)

run_jarvis()
