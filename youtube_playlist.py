import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the credentials for the YouTube Data API

def insert_playlist(artist, video_ids):

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube'])
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/youtube'])
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create a YouTube Data API client
    youtube = build('youtube', 'v3', credentials=creds)

    # Create a new playlist
    playlist_title = artist + ' Similar Artists'
    playlist_description = "Similar artist to " + artist + " on Spotify"
    playlist = youtube.playlists().insert(
        part="snippet, status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": playlist_description,
                "defaultLanguage": "en",

            },
            "status": {
                "privacyStatus": "public"
            }
        }
    ).execute()

    # Add videos to the playlist
# Replace with the actual video IDs
    for video_id in video_ids:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist['id'],
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
