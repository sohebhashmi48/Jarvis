# Import necessary libraries
import speech_recognition as sr  #pip install speech recognition
import pyttsx3 #pip install pyttsx3
import random
import pyautogui
import datetime
import time
import webbrowser
import openai #pip install openai

# Define your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key


# Function for speech recognition and query processing
def Listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)  # Listening Mode.....

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en")

    except:
        return ""

    query = str(query).lower()
    print(query)
    return query


# Function for text-to-speech
def Speak(Text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[1].id)
    engine.setProperty('rate', 190)
    print("")
    print(f"You : {Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()


# Function to detect a wake-up command
def WakeupDetected():
    while True:
        queery = Listen().lower()
        if "wake up" in queery:
            Speak("Yes, I'm awake. How can I assist you?")
            return
        else:
            pass


# Function to exit the assistant
def exit_jarvis():
    farewell_phrases = [
        "Goodbye! Have a great day!",
        "Farewell! Remember, I'm just a command away.",
        "Until next time! Stay productive.",
        # Add more farewell phrases as needed
    ]

    chosen_farewell = random.choice(farewell_phrases)
    Speak(chosen_farewell)
    time.sleep(1)
    pyautogui.hotkey("ALT", "F4")


# Function to tell the current time
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time_message = 'Current time is ' + current_time
    return time_message


# Function to greet the user based on the time of day
def greet():
    greeting_responses = [
        "Hello! How can I assist you today?",
        "Boss! What can I do for you?",
        "Hi there! How may I be of service?",
        # Add more greeting responses as needed
    ]

    random_response = random.choice(greeting_responses)
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 5 <= hour < 12:
        return "Good morning! " + random_response
    elif 12 <= hour < 18:
        return "Good afternoon! " + random_response
    else:
        return "Good evening! " + random_response


# Function to open an application
def open_application():
    Speak("What app would you like me to open?....")
    print("Note: say open + app name only!")
    query = Listen()
    query_length = len(query)

    if query_length >= 6:
        while True:
            app_name = query.replace("open", "")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write(app_name)
            time.sleep(3)
            pyautogui.press('Enter')
            break
    else:
        pass


# Function to search and play a video on YouTube
def youtube_search():
    Speak("What video would you like me to play?")
    video = Listen()

    video_search = video.replace("play", "").strip()
    video_length = len(video_search)

    if video_length >= 3:
        webbrowser.open("https://www.youtube.com")
        time.sleep(4)
        pyautogui.click(x=824, y=127)
        pyautogui.write(video_search)
        while True:
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(3)
            pyautogui.click(x=661, y=338)
            break
    else:
        error = "Video not found!"
        return error


# Function to interact with OpenAI GPT-3.5 Turbo
def brain(query):
    prompt = f"Jarvis, could you please {query}?"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant, who is acting like Jarvis from the Iron Man movie, and your reply should be less than 75 words"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']


# Main function
if __name__ == "__main__":
    Speak("Please say 'wake up' to activate Jarvis.")
    WakeupDetected()

    while True:
        command = Listen()

        if "exit" in command:
            exit_jarvis()
            break
        elif "time" in command:
            current_time = tell_time()
            Speak(current_time)
        elif "hello" in command:
            greeting = greet()
            Speak(greeting)
        elif "open" in command:
            open_application()
        elif "play" in command:
            youtube_search()
        else:
            response = brain(command)
            Speak(response)
