import csv
import constants
from ui.theme import color
from ui.terminal import (
    print_menu,
    print_not_valid_choice,
    print_to_go_back,
    format_comma_separated_maps,
    format_comma_separated_list,
)
from ui.browser import (
    open_in_browser,
    get_preferred_browser_display_name,
    choose_browser_menu,
)

def search_album_art_menu(sp, current_art_url: str):
    """Handles the 'Get album art' submenu and searches."""
    while True:
        print()
        print(" ---- " + constants.SELECT_SOURCE + " ---- ")
        print()
        print_menu(constants.ALBUM_ART_SUB_MENU)
        print()
        choice = input(" Your choice : ").strip()

        if choice == "1":
            if not current_art_url:
                print()
                print(color.BOLD + constants.CURRENTLY_NOTHING_PLAYING + color.END)
            else:
                print()
                print(f" ✅ Album art opened in {get_preferred_browser_display_name()}.")
                print()
                open_in_browser(current_art_url)

        elif choice == "2":
            print()
            search_query = input(" Enter song name, artist or album : ").strip()
            print()
            search_results = sp.search(search_query, limit=4, type="album,track")
            tracks_array = search_results['tracks']['items']
            albums_array = search_results['albums']['items']
            results_array = tracks_array + albums_array

            print(f" {len(results_array)} Results : ")
            while True:
                print()
                result_count = 0
                for result in results_array:
                    artist_names = format_comma_separated_maps(result.get('artists', []))
                    if result.get('type') == "track":
                        print(f" {result_count} - 🎸 {result['name']} - {artist_names}")
                    elif result.get('type') == "album":
                        print(f" {result_count} - 💿 {result['name']} - {artist_names}")
                    result_count += 1

                print_to_go_back("e")
                sub_choice = input(" Your choice : ").strip()
                if sub_choice == "e":
                    break

                try:
                    selected_idx = int(sub_choice)
                    if selected_idx < 0 or selected_idx >= len(results_array):
                        print_not_valid_choice()
                        continue

                    print()
                    print(f" ✅ Album art opened in {get_preferred_browser_display_name()}.")
                    selected_item = results_array[selected_idx]
                    if selected_item.get('type') == "track":
                        open_in_browser(selected_item['album']['images'][0]['url'])
                    elif selected_item.get('type') == "album":
                        open_in_browser(selected_item['images'][0]['url'])
                except (ValueError, IndexError, KeyError):
                    print_not_valid_choice()

        elif choice == "3":
            def get_popularity(item):
                return 0 if item.get('popularity') is None else item['popularity']

            print()
            artist_name = input(" What's the artist name? : ").strip()
            print()
            search_results = sp.search(artist_name, limit=5, type="artist")
            artists_list = search_results['artists']['items']
            artists_list.sort(reverse=True, key=get_popularity)

            print(f" {len(artists_list)} Results : ")
            print()
            for idx, artist in enumerate(artists_list):
                genres = artist.get('genres')
                genre = "NA" if not genres else genres[0]
                followers = artist.get('followers', {}).get('total', 0)
                pop = artist.get('popularity', 0)
                print(f" {idx} - 🎨 {artist['name']} - {genre} - {followers} followers - 🔥{pop}")

            print_to_go_back("e")
            sub_choice = input(" Your choice : ").strip()
            if sub_choice != "e":
                try:
                    artist_idx = int(sub_choice)
                    artist = artists_list[artist_idx]
                    genres_str = format_comma_separated_list(artist.get('genres', []))

                    print()
                    print(f" 🎨 Artist Name - {artist['name']}")
                    print(f" 👥 Followers - {artist.get('followers', {}).get('total', 0)} followers")
                    print(f" 🎶 Genres - {genres_str}")

                    artist_id = artist['id']
                    album_results = sp.artist_albums(artist_id, limit=50)
                    filtered_albums = [
                        alb for alb in album_results.get('items', [])
                        if alb.get('album_type') in ('album', 'single')
                    ]

                    print()
                    print(f" {len(filtered_albums)} albums :")
                    for alb_idx, alb in enumerate(filtered_albums):
                        print(f"\n {alb_idx} - 💿 {alb['name']}")
                        track_results = sp.album_tracks(alb['id'])
                        songs = [s['name'] for s in track_results.get('items', [])]
                        print()
                        print(", ".join(songs))
                        print()

                    print_to_go_back("e")
                    alb_choice = input(" Your choice : ").strip()
                    if alb_choice != "e":
                        selected_alb = filtered_albums[int(alb_choice)]
                        print()
                        print(f" ✅ Album art opened in {get_preferred_browser_display_name()}.")
                        if selected_alb.get('type') == "track":
                            open_in_browser(selected_alb['album']['images'][0]['url'])
                        elif selected_alb.get('type') == "album":
                            open_in_browser(selected_alb['images'][0]['url'])
                except (ValueError, IndexError, KeyError):
                    print_not_valid_choice()

        elif choice == "4":
            choose_browser_menu()

        elif choice == "5":
            print()
            break
        else:
            print_not_valid_choice()

def list_and_export_playlists(sp):
    """Lists the user's Spotify playlists and exports tracks from the selected playlist to CSV."""
    playlist_uris = []
    playlist_names = []
    print()
    print(" Your Spotify playlists : ")
    print()

    playlists = sp.current_user_playlists()
    total_playlists = playlists.get('total', 0)
    items = playlists.get('items', [])

    counter = 0
    while counter < total_playlists:
        offset = counter % 50
        if offset == 0 and counter > 0:
            playlists = sp.next(playlists)
            items = playlists.get('items', [])

        if offset < len(items):
            p_name = items[offset]['name']
            p_uri = items[offset]['uri']
            print(f" {counter}: {p_name}")
            playlist_uris.append(p_uri)
            playlist_names.append(p_name)
        counter += 1

    print()

    while True:
        playlist_selection = input(" Enter the index number of a playlist to see all songs in it or e to exit : ").strip()
        if playlist_selection == "e":
            break

        try:
            selected_idx = int(playlist_selection)
            playlist_uri = playlist_uris[selected_idx]
            results = sp.playlist(playlist_uri)
            total_tracks = results["tracks"]["total"]

            song_list = []
            album_list = []
            artist_list = []
            release_date_list = []

            tracks = results["tracks"]
            items = tracks.get("items", [])
            print()
            print(" Songs in the playlist :")
            print()

            track_idx = 0
            while track_idx < total_tracks:
                offset = track_idx % 100
                if offset == 0 and track_idx > 0:
                    tracks = sp.next(tracks)
                    if tracks is None:
                        break
                    items = tracks.get("items", [])

                if offset < len(items) and items[offset].get("track"):
                    trk = items[offset]["track"]
                    song = trk.get("name", "Unknown")
                    album = trk.get("album", {}).get("name", "Unknown")
                    release_date = trk.get("album", {}).get("release_date", "Unknown")
                    artists = ", ".join(k.get("name", "") for k in trk.get("artists", []))

                    print(f" {track_idx} : {song} - {artists}")
                    song_list.append(song)
                    album_list.append(album)
                    release_date_list.append(release_date)
                    artist_list.append(artists)

                track_idx += 1

            # Save details to songlist.csv
            final_data = list(zip(song_list, artist_list, album_list, release_date_list))
            headers = ["Name", "Artists", "Album", "Release Date"]
            with open("songlist.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(final_data)

            print()
            print(" ✅ Details saved in 'songlist.csv' file.")
            break
        except (ValueError, IndexError) as err:
            print_not_valid_choice()
