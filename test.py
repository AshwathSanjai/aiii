import speech_recognition as sr
import os
import threading  
import time
import openai
from datetime import datetime
import pyttsx3

openai.api_key = "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"  

engine = pyttsx3.init()
WAKE_WORD = "bps"   

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                if text.lower().count(WAKE_WORD) > 0:
                    return True

            except:
                pass
                
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio_data)  
            if query:
                print("You said:", query)
                return query.lower()

        except:
            print("Waiting...")
            pass

def respond_to_command(command):

    if "what is the time" in command:
        current_time = datetime.now().strftime("%H:%M") 
        response = f"The current time is {current_time}"
    elif "who are you" in command:
        response = "I am BPS AI, the short form of Bridge Woods Public School Artificial Intelligence."
    elif "who created" in command:
        response = "I was created by Ashwath Sanjai for his gallery walk project in his 8th grade"
    elif "who really created you" in command:
        response = "ashwath sanjai"
    else:
        # Generate OpenAI response
        prompt = f"Command: {command}. Provide helpful response:"  
        openai_response = generate_openai_response(prompt) 
        response = openai_response

    print(response)        
    speak_response(response)

def generate_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error processing OpenAI response: {e}")
        return "I'm sorry, there was an issue processing your request."

def speak_response(text):
    engine.say(text)
    engine.runAndWait() 

if __name__ == "__main__":
    
    wake_word_thread = threading.Thread(target=listen_for_wake_word)  
    wake_word_thread.start()
    
    while True:
        wake_word_thread.join()
        command = listen_for_command()
        if command:
            respond_to_command(command)