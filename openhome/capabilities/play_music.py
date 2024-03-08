import spotipy
from spotipy.oauth2 import SpotifyOAuth
from chatgpt_module import chatgpt
import re

def open_file(filepath):
    """Open and return the content of a file given its filepath."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read().strip()
        
def execute(user_message):

    api_key = open_file('api-keys/openaiapikey2.txt')

    conversation1 = []  
    chatbot1 = "You are a smart speaker. Tell me what music to play based on the following description:"  
    
    # Query GPT for song recommendations
    response_note = "I've processed a command. The message to you follows:"
    response = chatgpt(api_key, conversation1, chatbot1, response_note + user_message)

    user_message_without_generate_image = re.sub(r'(Response:|Narration:|Image: generate_image:.*|)', '', response).strip()

    # Spotify setup

    #spotify id
    client_id = '77d4a0318c9f4cc888f04bca34dfe80c'
    client_secret = '9de3e8030a0c41668e825c56d573f244'
    redirect_uri = 'http://localhost:8888/callback'
    scope = "user-modify-playback-state user-read-playback-state"
    
    auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri,
                                scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Search and play the song on Spotify
    results = sp.search(q=user_message_without_generate_image, limit=1, type='track')
    tracks = results['tracks']['items']
    if tracks:
        track_uri = tracks[0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing: {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")
    else:
        print("No tracks found for:", user_message_without_generate_image)