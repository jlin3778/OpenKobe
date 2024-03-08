import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
import requests
import re
from colorama import Fore, Style, init
import datetime
import base64
from pydub import AudioSegment
from pydub.playback import play
from concurrent.futures import ThreadPoolExecutor
import time
import threading

# Importing custom modules
from chatgpt_module import chatgpt
from greeting_module import first_time_greeting, self_introduction
from text_speech_module import text_to_speech
from audio_module import record_and_transcribe


# Global shared state to control music playback
playback_state = {"playing": False}


# Initialize colorama for colored text output
init()

# Global flag to check if it's the first run of the script
is_first_run = True

    
# Function to open and read a file
def open_file(filepath):
    """Open and return the content of a file given its filepath."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Load API keys and voice ID from files
api_key = open_file('api-keys/openaiapikey2.txt')
elapikey = open_file('api-keys/elabapikey.txt')
voice_id1 = 'rDtLxTyLozy3kzwxszee'


# Initialize conversation history and load chatbot personality
conversation1 = []  
chatbot1 = open_file('personalities/Activated.txt')

# Function to print text in colored format
def print_colored(agent, text):
    """Print the text in a color based on the agent speaking."""
    agent_colors = {"Openhome:": Fore.YELLOW}
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")
    
    

# Check if this is the first run of the script
if is_first_run:
    # self intro
    immediate_response = "Ready to work? Great things come from hard work and perseverance. No excuses. I know you aren't trying to be lazy today."
    text_to_speech(immediate_response, voice_id1, elapikey)
    self_introduction(api_key)
    
   
    # Perform first time greeting using the greeting module
    first_time_greeting(api_key, elapikey, chatbot1, conversation1, voice_id1)
    
    
    is_first_run = False


# Main loop
while True:

    # Record user's voice and transcribe it
    user_message = record_and_transcribe(api_key)

    # Check for a goodbye message to exit the loop
    if "lazy" in user_message.lower() in user_message.lower():
        immediate_response = "I can’t relate to lazy people. We don’t speak the same language. I don’t understand you. I don’t want to understand you. You gotta change that!"
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue

     # Check for a goodbye message to exit the loop
    if "easy" in user_message.lower() in user_message.lower():
        immediate_response = "I knew it'd be too easy for you. That was light work for me back in the day."
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue

     # Check for a goodbye message to exit the loop
    if "difficult" in user_message.lower() in user_message.lower():
        immediate_response = "Okay I see. On a scale of it didn't hurt enough to it should hurt more, what would you rate that workout so I could adjust it for you."
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue

      # Check for a goodbye message to exit the loop
    if "it didn't hurt enough" in user_message.lower() in user_message.lower():
        immediate_response = "Okay I see. We need to be hurting at all times then. Increase the reps on the last workout by 20-25 percent on average. Then we'll see what you are made of."
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue

     # Check for a goodbye message to exit the loop
    if "fear" in user_message.lower() in user_message.lower():
        immediate_response = "Fear? Fear is a good thing. You gotta look fear in the eyes and beat it. That's how you will become stronger."
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue

     # Check for a goodbye message to exit the loop
    if "challenge" in user_message.lower() in user_message.lower():
        immediate_response = "Mamba mentality. Mamba mentality. Mamba mentality."
        text_to_speech(immediate_response, voice_id1, elapikey)
        continue
    
     # Check for a goodbye message to exit the loop
    if "goodbye" in user_message.lower() or "good bye" in user_message.lower():
        immediate_response = "That's what's up. If you do not believe in yourself, no one will do it for you. Mamba out."
        text_to_speech(immediate_response, voice_id1, elapikey)
        break  # This exits the while loop
 
    

        
    # Generate a response using the ChatGPT module
    response = chatgpt(api_key, conversation1, chatbot1, user_message)

    # Print the response in a colored format
    print_colored("Openhome:", f"{response}\n\n")

 
    # Remove any image generation commands from the response
    user_message_without_generate_image = re.sub(r'(Response:|Narration:|Image: generate_image:.*|)', '', response).strip()

    # Convert the response to speech and play it
    text_to_speech(user_message_without_generate_image, voice_id1, elapikey)