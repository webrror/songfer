SCOPES = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-library-read'
USER_YML = 'user.yml'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'
PORT = '8888'

INSTRUCTIONS = [
    "Go to the Spotify dashboard - https://developer.spotify.com/dashboard/applications",
    "Click create an app and note the Client ID and Client Secret",
    "Now click `Edit Settings`",
    "Add `http://localhost:"+PORT+"/callback` to the Redirect URIs",
    "Note your username from account page - https://www.spotify.com/account/overview/ ",
    "You are now ready to authenticate with Spotify!",
]

FREE = "Free"
CURRENTLY_NOTHING_PLAYING = " Currently nothing playing."
PODCASTS_NO_SUPPORT = " Podcast playing."
AD_PLAYING = " Ad playing."
CURRENTLY_PLAYING = " Currently playing : "

MENU = [
    "Get album art",
    "List your songs in a playlist from Spotify",
    "Transfer songs",
    "Exit"
]

SELECT_SOURCE = "SELECT A SOURCE"

ALBUM_ART_SUB_MENU = [
    "Current playing song",
    "Search using song name, artist, album, .....",
    "Search using artist name (legacy)",
    "Exit to main menu"
] 