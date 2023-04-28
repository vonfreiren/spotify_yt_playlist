import csv

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

from youtube import search_youtube
from youtube_playlist import insert_playlist

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']
user_id = data['spotify_user_id']


os.environ["SPOTIPY_REDIRECT_URI"] = "https://example.com/callback"

scope = "user-library-read user-library-modify playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=secret,
                                               scope=scope))

def search_spotify_artist(name_artist, song=None, include_youtube=False):
    lists_uris_spotify = []
    list_video_ids = []
    if song is not None:
        results = sp.search(q=name_artist + song, limit=1)
    else:
        results = sp.search(q=name_artist, limit=1)
    artist_id = results['tracks']['items'][0]['artists'][0]['id']
    related_artists = sp.artist_related_artists(artist_id)['artists']
    with open('songs.csv', 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Artist", "Title", "URL"])
        for artist in related_artists:
            top_tracks = sp.artist_top_tracks(artist['id'])
            for idx, track in enumerate(top_tracks['tracks']):
                lists_uris_spotify.append(track['uri'])
                if include_youtube:
                    yt_url, yt_id = search_youtube(track['name']+' '+artist['name'])
                    # Write each line to the file
                    writer.writerow([artist['name'], track['name'], yt_url])
                    list_video_ids.append(yt_id)
    add_playlist_spotify(name_artist, lists_uris_spotify)
    #insert_playlist(name_artist, list_video_ids)



def add_playlist_spotify(name_artist,lists_uris_spotify ):
    playlist_name = name_artist +' Similar Songs'

    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)

    # Replace the list of track URIs with the URIs of the tracks you want to add
    sp.playlist_add_items(playlist_id=new_playlist['id'], items=lists_uris_spotify[:99])

def add_playlist(artist_name):
    # Replace the playlist name and description with your own values
    playlist_name = 'Similar artists to ' + artist_name + ' on Spotify'
    playlist_description = 'Tracks from Similar artists to ' + artist_name + ' on Spotify'

    # Create the new playlist
    playlist = sp.user_playlist_create(user='javfreire@protonmail.com', name=playlist_name, public=True, description=playlist_description)

    # Print the playlist ID
    print(f'Playlist created! ID: {playlist["id"]}')


artist = 'Kygo'
song = 'Firestone'
search_spotify_artist('Kygo', song=song)
