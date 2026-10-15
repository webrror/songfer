import os
import sys
from json.decoder import JSONDecodeError
import spotipy
import spotipy.util as util
import constants
from ui.terminal import print_instructions

class CustomSpotifyOAuth(spotipy.SpotifyOAuth):
    def _open_auth_url(self):
        auth_url = self.get_authorize_url()
        print()
        print(" Open this URL in your browser if it doesn't open automatically:")
        print()
        print(f" {auth_url}")
        print()
        # super()._open_auth_url()

def get_credentials():
    """
    Reads Spotify developer credentials from user.yml.
    If the file does not exist or is empty, instructions are shown
    and the user is prompted to enter them.
    """
    if os.path.exists(constants.USER_YML) and os.path.getsize(constants.USER_YML) > 0:
        user_dict = {}
        with open(constants.USER_YML, "r") as f:
            for line in f:
                line = line.strip()
                name, var = line.partition(":")[::2]
                user_dict[name.strip()] = str(var)
        return user_dict.get('USERNAME'), user_dict.get('CLIENT'), user_dict.get('SECRET')
    else:
        print()
        print(" ----- INSTRUCTIONS -----")
        print()
        print_instructions()

        print()
        client_id = input("Enter your Client ID : ").strip()
        secret_client_id = input("Enter your Client Secret : ").strip()
        username = input("Enter your Username : ").strip()

        if client_id and secret_client_id and username:
            with open(constants.USER_YML, "w") as f:
                f.write("CLIENT:" + client_id + "\n")
                f.write("SECRET:" + secret_client_id + "\n")
                f.write("USERNAME:" + username + "\n")
                f.write("PORT:" + constants.PORT + "\n")
        else:
            print()
            print(" Required details not entered. Exiting...")
            sys.exit(1)

        return username, client_id, secret_client_id

def authenticate_spotify():
    """
    Sets up environment variables, handles OAuth authentication,
    and returns an authenticated spotipy.Spotify instance and username.
    """
    username, client_id, client_secret = get_credentials()

    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    os.environ["SPOTIPY_REDIRECT_URI"] = constants.SPOTIPY_REDIRECT_URI

    sp_oauth = CustomSpotifyOAuth(scope=constants.SCOPES, username=username)

    try:
        token = util.prompt_for_user_token(username, constants.SCOPES, oauth_manager=sp_oauth)
    except (AttributeError, JSONDecodeError, spotipy.oauth2.SpotifyOauthError):
        cache_file = f".cache-{username}"
        if os.path.exists(cache_file):
            os.remove(cache_file)
        token = util.prompt_for_user_token(username, constants.SCOPES, oauth_manager=sp_oauth)

    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object, username
