#!/usr/bin/env python3
# run -> $ python3 songfer.py

import os
import sys

from auth import authenticate_spotify
from services import (
    search_album_art_menu,
    list_and_export_playlists,
    transfer_playlist_to_ytmusic,
    transfer_liked_songs_to_ytmusic,
)
from ui import (
    clear_screen,
    print_menu,
    print_not_valid_choice,
    display_user_header,
    display_devices,
    render_album_art,
    format_comma_separated_maps,
    color,
    choose_browser_menu,
)
import constants

def refresh():
    """Restarts the application."""
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    # Authenticate and obtain Spotify client
    spotify_object, username = authenticate_spotify()

    # MAIN APPLICATION LOOP
    while True:
        user = spotify_object.current_user()
        clear_screen()
        display_user_header(user)

        # Check currently playing track
        art = ""
        playback = spotify_object.current_playback()

        if playback is None:
            print()
            print(color.BOLD + constants.CURRENTLY_NOTHING_PLAYING + color.END)
        elif playback.get('currently_playing_type') == 'episode':
            print()
            print(color.BOLD + constants.PODCASTS_NO_SUPPORT + color.END)
        elif playback.get('currently_playing_type') == 'ad':
            print()
            print(color.BOLD + constants.AD_PLAYING + color.END)
        else:
            track = spotify_object.current_user_playing_track()
            if track and track.get('item'):
                images = track['item'].get('album', {}).get('images', [])
                art = images[0]['url'] if images else ""
                artist = format_comma_separated_maps(track['item'].get('artists', []))
                track_name = track['item'].get('name', 'Unknown')

                if artist != "":
                    print()
                    print(constants.CURRENTLY_PLAYING, flush=True)
                    print()
                    if art:
                        render_album_art(art)

                    print(f" {color.BOLD}🎸  {track_name} - {artist}{color.END}")
                    print()

            devices = spotify_object.devices()
            display_devices(devices)

        # Display Main Menu
        print()
        print(" ----- MAIN MENU -----")
        print()
        print_menu(constants.MENU)
        print()
        choice = input(" Your choice : ").strip()

        if choice == "1":
            search_album_art_menu(spotify_object, art)
        elif choice == "2":
            list_and_export_playlists(spotify_object)
        elif choice == "3":
            transfer_playlist_to_ytmusic(spotify_object, username)
        elif choice == "4":
            transfer_liked_songs_to_ytmusic(spotify_object)
        elif choice == "5":
            choose_browser_menu()
        elif choice == "6":
            refresh()
        elif choice == "7":
            print()
            break
        else:
            print_not_valid_choice()

if __name__ == "__main__":
    main()