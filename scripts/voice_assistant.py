# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:42:36 2021

@author: Sam
"""

# for voice chat
import speech_recognition as sr
import pyttsx3

import webbrowser
import operator  # used for math operations
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory
from datetime import date, timedelta, datetime

# Wake word in Listen Function
WAKE = "Karen"

# Used to store user commands for analysis
CONVERSATION_LOG = "Conversation_Log.txt"


# Speech Recognition Constants
recognizer = sr.Recognizer()
microphone = sr.Microphone()
# Python Text-to-Speech (pyttsx3) Constants
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('voice', 'english_rp+f3')

# Initial analysis of words that would typically require a Google search
SEARCH_WORDS = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}

class Karen:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.WAKE = 'Karen'
        self.CONVERSATION_LOG = "Conversation_Log.txt"

    # Used to hear the commands after the wake word has been said
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # May reduce the time out in the future
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                s.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to speak to the user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Used to track the date of the conversation, may need to add the time in the future
    def start_conversation_log(self):
        today = str(date.today())
        today = today
        with open(CONVERSATION_LOG, "a") as f:
            f.write("Conversation started on: " + today + "\n")

    def search_youtube(self, command):
        search_term = command.replace('search youtube for ', '')
        s.speak(f'searching youtube for {search_term}')
        query = search_term.replace(' ', '+')
        webbrowser.open(f'https://www.youtube.com/results?search_query={str(query)}')
        pass

    # Writes each command from the user to the conversation log
    def remember(self, command):
        with open(CONVERSATION_LOG, "a") as f:
            f.write("User: " + command + "\n")

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        if "today" in command:
            s.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif command == "what time is it":
            s.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

        elif "yesterday" in command:
            date_intent = today - timedelta(days=1)
            return date_intent

        elif "this time last year" in command:
            current_year = today.year

            if current_year % 4 == 0:
                days_in_current_year = 366

            else:
                days_in_current_year = 365
            date_intent = today - timedelta(days=days_in_current_year)
            return date_intent

        elif "last week" in command:
            date_intent = today - timedelta(days=7)
            return date_intent
        else:
            pass


    def light_switch(self, command):
        ips = []
        lights = []
        if 'bedroom light' in command:
            ips.append(bedroom_light_ip)
            lights.append('bedroom light')
        if 'bedroom lamp' in command:
            ips.append(bedroom_lamp_ip)
            lights.append('bedroom lamp')
        if 'office light' in command:
            ips.append(office_light_ip)
            lights.append('office light')

        s.speak(f'switching {[light for light in lights]}')

        if len(ips) > 0:
            if 'on' in command:
                for ip in ips:
                    bulb = yeelight.Bulb(ip)
                    bulb.turn_on()
            elif 'off' in command:
                for ip in ips:
                    bulb = yeelight.Bulb(ip)
                    bulb.turn_off()
        else:
            s.speak('Sorry, I could not find the light you were looking for')
            return None

    def light_brightness(self, command):
        ips = []
        lights = []
        if 'bedroom light' in command:
            ips.append(bedroom_light_ip)
            lights.append('bedroom light')
        if 'bedroom lamp' in command:
            ips.append(bedroom_lamp_ip)
            lights.append('bedroom lamp')
        if 'office light' in command:
            ips.append(office_light_ip)
            lights.append('office light')

        value = [int(s) for s in command.split() if s.isdigit()][0]

        s.speak(f'Setting Brightness to {value} for {[light for light in lights]}')

        if len(ips) > 0:
            for ip in ips:
                bulb = yeelight.Bulb(ip)
                try:
                    bulb.turn_on()
                finally:
                    bulb.set_brightness(value)
        else:
            s.speak('Sorry, I could not find the light you were looking for')
            return None

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            'divided': operator.__truediv__,
            'over': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
            '^': operator.xor,
        }[op]

    # We'll need a list to perform the math
    def do_math(self, li):
        # passes the second item in our list to get the built-in function operand
        op = self.get_operator(li[1])
        # changes the strings in the list to integers
        int1, int2 = int(li[0]), int(li[2])
        # this uses the operand from the get_operator function against the two intengers
        result = op(int1, int2)
        s.speak(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))

    # Checks "what is" to see if we're doing math
    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        # First, we'll make a list a out of the string
        li = list(command.split(" "))
        # Then we'll delete the "what" and "is" from the list
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "what is the date today" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        s.speak("Here is what I found.")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, command, WAKE):
        try:

            if command == "introduce yourself":
                s.speak(f"I am {WAKE}. I'm a digital assistant.")

            elif command == "what time is it":
                self.understand_time(command)

            elif command == "how are you":
                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]
                greeting = random.choice(current_feelings)
                s.speak(greeting)

            elif ('light' in command or 'lamp' in command) and ('on ' in command or 'off ' in command):
                self.light_switch(command)

            elif ('light' in command or 'lamp' in command) and ('brightness' in command):
                self.light_brightness(command)

            elif "weather" in command:
                self.get_weather(command)

            elif "what is" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            elif 'search youtube for' in command:
                self.search_youtube(command)

            else:
                s.speak("I don't know how to do that yet.")

        
        except TypeError as e:
            print("Warning: You're getting a TypeError somewhere.", e)
            pass
        except AttributeError as e:
            print("Warning: You're getting an Attribute Error somewhere.", e)
            pass

    # Used to listen for the wake word
    def listen(self, recognizer, microphone, WAKE):
        while True:
            try:
                with microphone as source:
                    print("Listening.")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=5.0)
                    response = recognizer.recognize_google(audio)

                    if WAKE in response:
                        s.speak(random.choice(['Hi!', 'Hello!', 'Hi Sam', 'Hello Sam', 'Yes Sam?', 'Yes?']))
                        return response.lower()
                    else:
                        pass

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")


previous_response = ""


def run_va(previous_response):
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)

    if command != previous_response:
        s.analyze(command)
        previous_response = command
    else:
        s.speak("You already asked that. Ask again if you want to do that again.")
        previous_command = ""
        response = s.listen(recognizer, microphone)
        command = s.hear(recognizer, microphone, response)

    return previous_response

if __name__ == '__main__':
    s = Karen()
    s.start_conversation_log()
    previous_response = ""
    while True:
        previous_response = run_va(previous_response)


