# Spotify Tools
This project includes scripts for managing Spotify Playlists.
1.  Spotify Playlist Randomizer - It creates a temporary randomized playlist, replaces the contents of the original playlist with the randomized tracks, and then deletes the temporary playlist, assuring no 2 songs from 1 singer goes one after another.

---

## Features

- Randomizes the order of tracks in a Spotify playlist.
- Ensures the original playlist is updated with the new randomized order.
- Creates a temporary playlist during the randomization process and deletes it after completion.

---

## Prerequisites

Before you start, make sure you have:

1. **Python 3.7+** installed on your system.
2. `pip` installed for package management.
3. A **Spotify Developer Account** to create and manage a new app:
   - Register your app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Obtain your **Client ID** and **Client Secret**.
4. Access to the playlist you want to randomize.

---

## Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/dumitrub98/spotifytools
cd spotifytools
```

### Step 2: Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install spotipy tqdm
```

### Step 3: Set up environment variables

You need to configure the following environment variables for authentication:
- SPOTIFY_CLIENT_ID: Your Spotify application’s Client ID.
- SPOTIFY_CLIENT_SECRET: Your Spotify application’s Client Secret.
- SPOTIFY_REDIRECT_URI: The redirect URI you set in your Spotify app’s settings (e.g., http://localhost:8888/callback/).

To set these variables:
```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback/"
```


## Usage

### Command Syntax:
```bash
python3 spotify_randomizer.py <spotify_playlist_url>
```
- 	<spotify_playlist_url>: The full URL of the Spotify playlist you want to randomize (e.g., https://open.spotify.com/playlist/dasdasdasdsad?si=dasdasdsad).

### Output:
```bash
Fetching playlist tracks...
Fetched 500 tracks.
Created new playlist: MyPlaylist_rnd.
Added 500 randomized tracks to the new playlist.
Original playlist cleared.
Original playlist updated with randomized tracks.
Deleted temporary randomized playlist.
Playlist randomized successfully!
```

---

## Notes
- The script does not work with playlists you do not own or have edit permissions for.
- Be mindful of Spotify API rate limits. Avoid running the script repeatedly on very large playlists.
- The script requires the Spotify API to be reachable. If you encounter timeout issues, check your internet connection or retry after some time.

---

## Troubleshooting

- **Rate limit errors**:
If you see messages like Your application has reached a rate/request limit, it means Spotify has temporarily blocked further requests. You need to wait for the limit to reset (typically a few minutes to hours).
- **Authentication errors**:
Ensure your SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REDIRECT_URI are set correctly. If you’re still having trouble, delete the .cache file in your project directory and re-authenticate.

---

## Contributing

Feel free to submit issues or contribute improvements to this project by opening a pull request.

---
## Acknowledgements

Special thanks to the Spotipy library for providing an excellent Python wrapper for the Spotify Web API.
