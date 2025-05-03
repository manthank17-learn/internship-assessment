import os
import requests
import json
from dotenv import load_dotenv
import wave
import contextlib


load_dotenv()

def get_audio_duration(file_path):
    """
    Get the duration of an audio file in seconds
    """
    try:
        with contextlib.closing(wave.open(file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except:
        
        print("Warning: Could not determine audio duration. Assuming it's valid.")
        return 0  

def display_language_options():
    """Display the numbered language options"""
    print("\nAvailable languages:")
    print("1. English")
    print("2. Luganda")
    print("3. Runyankole")
    print("4. Ateso")
    print("5. Lugbara")
    print("6. Acholi")

def get_language_choice(prompt):
    """Get and validate language choice from user"""
    languages = ["English", "Luganda", "Runyankole", "Ateso", "Lugbara", "Acholi"]
    language_codes = ["eng", "lug", "nyn", "teo", "lgg", "ach"]
    
    while True:
        display_language_options()
        print(prompt)
        try:
            choice = int(input())
            if choice < 1 or choice > 6:
                print("Please enter a number between 1 and 6.")
                continue
                
            
            selected_index = choice - 1
            selected_language = languages[selected_index]
            selected_code = language_codes[selected_index]
            
            return selected_language, selected_code
        except ValueError:
            print("Please enter a valid number.")

def transcribe_audio(file_path, language_code, api_token):
    """
    Transcribe an audio file using the Sunbird AI API
    """
    url = "https://api.sunbird.ai/tasks/stt"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    
    file_name = os.path.basename(file_path)
    
    files = {
        "audio": (
            file_name,
            open(file_path, "rb"),
            "audio/mpeg"
        )
    }
    
    data = {
        "language": language_code,
        "adapter": language_code,
        "whisper": True
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            
            
            if "text" in result:
                return result["text"]
            elif "transcription" in result:
                return result["transcription"]
            elif isinstance(result, dict) and len(result) > 0:
                
                return str(result)
            else:
                return f"Transcription received but in unexpected format: {result}"
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    
    api_token = os.getenv("AUTH_TOKEN")
    
    
    if not api_token:
        api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXRyaWNrY21kIiwiYWNjb3VudF90eXBlIjoiRnJlZSIsImV4cCI6NDg2OTE4NjUzOX0.wcFG_GjBSNVZCpP4NPC2xk6Dio8Jdd8vMb8e_rzXOFc"
        print("No AUTH_TOKEN found in environment, using default token")
    
    print("Welcome to the Ugandan Language Audio Transcriber")
    print("-------------------------------------------------")
    
    while True:
        
        print("\nPlease enter the path to the audio file:")
        file_path = input().strip()
        
        
        if not os.path.isfile(file_path):
            print(f"Error: File {file_path} does not exist.")
            continue
        
     
        duration = get_audio_duration(file_path)
        if duration > 300:  # 5 minutes = 300 seconds
            print("Error: Audio file is longer than 5 minutes. Please use a shorter audio file.")
            continue
        
       
        language, language_code = get_language_choice("Please enter the number for the language of the audio:")
        print(f"Language selected: {language}")
        
       
        print("\nTranscribing audio...")
        transcription = transcribe_audio(file_path, language_code, api_token)
        
        print("\nTranscription result:")
        print(transcription)
        
        
        print("\nWould you like to transcribe another audio file? (y/n)")
        continue_choice = input().lower()
        if continue_choice != 'y':
            print("Thank you for using the Ugandan Language Audio Transcriber!")
            break

if __name__ == "__main__":
    main()