import requests
import base64
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify token URL
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_spotify_token():
    # Encode client credentials
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    # Request headers
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Request body
    data = {"grant_type": "client_credentials"}
    
    # Make request
    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        print(token_info)
        access_token = token_info["access_token"]
        return access_token
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def api_call(url, access_token):
    """Makes an API call to the given URL with the provided access token."""
    headers = {'Authorization': f'Bearer {access_token}'}  # Correct format
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Call Failed: {response.status_code}, {response.text}")

if __name__ == "__main__":
    try:
        # Get the access token once and reuse it
        access_token = get_spotify_token()
        print(f"Access Token: {access_token[:15]}...")  # Print partial token for security
        
        # Example API call: Get Spotify new releases
        url = "https://api.spotify.com/v1/playlists/0vvXsWCC9xrXsKd4FyS8kM?offset=0&limit=5"
        data = api_call(url, access_token)
        valid_json = json.dumps(data, indent=4)
        with open("output.json", "w") as file:
            json.dump(data, file, indent=4)
        
    except Exception as e:
        print(e)
