import csv

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

from youtube import search_youtube
from youtube_playlist import insert_playlist

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id = data['spotify_client_id']
secret = data['spotify_secret']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=secret))


def search_spotify(name_artist):
    list_video_ids = []
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
                yt_url, yt_id = search_youtube(track['name']+' '+artist['name'])
                    # Write each line to the file
                writer.writerow([artist['name'], track['name'], yt_url])
                list_video_ids.append(yt_id)
    insert_playlist(name_artist, list_video_ids)




