import os
import sys
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify environment variables
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback/")

# Creează clientul Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope="playlist-modify-private playlist-modify-public playlist-read-private"))

def get_spotify_tracks(playlist_url):
    """Fetch tracks from Spotify playlist."""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    tracks = []
    results = sp.playlist_items(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            tracks.append(track['id'])  # Stocăm doar ID-ul piesei
        
        if results['next']:
            results = sp.next(results)
        else:
            break

    print(f"Fetched {len(tracks)} tracks.")
    return tracks, playlist_id

def create_randomized_playlist(original_playlist_id, tracks):
    """Creează un playlist randomizat și returnează ID-ul acestuia."""
    random.shuffle(tracks)
    original_playlist = sp.playlist(original_playlist_id)
    new_playlist_name = f"{original_playlist['name']}_rnd"

    # Creează un playlist nou
    new_playlist = sp.user_playlist_create(user=original_playlist['owner']['id'],
                                           name=new_playlist_name,
                                           public=False,
                                           description="Randomized playlist")
    new_playlist_id = new_playlist['id']
    print(f"Created new playlist: {new_playlist_name}.")

    # Adaugă piesele randomizate în noul playlist
    for i in range(0, len(tracks), 100):  # Spotify API permite max 100 piese/adăugare
        sp.playlist_add_items(new_playlist_id, tracks[i:i + 100])
    
    print(f"Added {len(tracks)} randomized tracks to the new playlist.")
    return new_playlist_id

def replace_original_playlist(original_playlist_id, randomized_playlist_id):
    """Înlocuiește conținutul playlistului original cu cel din playlistul randomizat."""
    # Șterge toate piesele din playlistul original
    original_tracks, _ = get_spotify_tracks(f"https://open.spotify.com/playlist/{original_playlist_id}")
    if original_tracks:
        sp.playlist_replace_items(original_playlist_id, [])  # Golește playlistul original
        print("Original playlist cleared.")

    # Adaugă piesele din playlistul randomizat în cel original
    randomized_tracks, _ = get_spotify_tracks(f"https://open.spotify.com/playlist/{randomized_playlist_id}")
    for i in range(0, len(randomized_tracks), 100):
        sp.playlist_add_items(original_playlist_id, randomized_tracks[i:i + 100])
    
    print("Original playlist updated with randomized tracks.")

    # Șterge playlistul temporar randomizat
    sp.current_user_unfollow_playlist(randomized_playlist_id)
    print("Deleted temporary randomized playlist.")

def randomize_playlist(playlist_url):
    """Randomizează conținutul unui playlist."""
    tracks, playlist_id = get_spotify_tracks(playlist_url)
    if not tracks:
        print("No tracks found in the playlist.")
        return

    randomized_playlist_id = create_randomized_playlist(playlist_id, tracks)
    replace_original_playlist(playlist_id, randomized_playlist_id)
    print("Playlist randomized successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python spotify_randomizer.py <spotify_playlist_url>")
        sys.exit(1)

    spotify_playlist_url = sys.argv[1]
    randomize_playlist(spotify_playlist_url)