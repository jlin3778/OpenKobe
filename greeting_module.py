# Import necessary modules
from chatgpt_module import chatgpt
from file_management import open_file
from text_speech_module import text_to_speech
from openai import OpenAI
import os
from audio_module import record_and_transcribe
import sounddevice as sd
import soundfile as sf
import json



def analyze_and_extract_info(api_key, user_transcription):
    client = OpenAI(api_key=api_key)
    
    # Assuming 'user_transcription' contains the transcribed self-introduction
    # Adapt the conversation structure for personal introduction analysis
    conversation = [
        {"role": "system", "content": "Extract key personal details such as name, interests from the following introduction."},
        {"role": "user", "content": user_transcription}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4",  # Ensure you're using the correct and latest model
        messages=conversation,
        temperature=0.7,  # Adjust based on how creative or straightforward you want the response to be
        max_tokens=1024,  # Adjust as needed
        n=1,  # Number of completions to generate
    )
    
    # Extract the structured information from the completion response
    structured_info = completion.choices[0].message.content.strip()
    
    # Here you would parse 'structured_info' to extract and structure the user information
    # The parsing logic depends on the expected format of the GPT response
    
    return structured_info  # Or return a parsed dictionary of user details

    
def save_user_info(user_info, filepath='history-files/user.txt'):
    with open(filepath, 'w') as file:
        for key, value in user_info.items():
            file.write(f"{key}: {value}\n")


def self_introduction(api_key):
    # ask for user information, take user vocal input and transcribe it into a paragraph and send to the gpt and let create a dictionary that classified user info
    
    transcription = record_and_transcribe(api_key)
    extracted_info = analyze_and_extract_info(api_key, transcription)
    print(extracted_info)
    
    # Assuming `extracted_info` is a string of key:value pairs, convert it to a dict
    user_info = dict(item.split(':') for item in extracted_info.split('\n') if item)
    save_user_info(user_info)
    print("saved")
    
    # then save this file to 'history-files/user.txt'


def first_time_greeting(api_key, elapikey, chatbot1, conversation1, voice_id1):
    
    # Read user information
    user_info = open_file('history-files/user.txt')

    # Initial greeting message
    greeting_message = "Hi Shannon. I'm excited to meet you. I'm the OpenHome onboarding assistant. Let me summarize what I know about you."

    # Pass user info to the chatbot
    chat_response = chatgpt(api_key, conversation1, chatbot1, user_info, temperature=0.5)

    # Convert chatbot's response to speech
    text_to_speech(chat_response, voice_id1, elapikey)


#api_key= "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"
#
#self_introduction(api_key)
