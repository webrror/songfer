import os
import time
import datetime
from ytmusicapi import YTMusic
from ui.terminal import print_not_valid_choice

def get_ytmusic_client():
    """Initializes and returns the YTMusic client using headers_auth.json."""
    auth_file = "headers_auth.json"
    if not os.path.exists(auth_file):
        print()
        print(" 🚫 'headers_auth.json' not found. Please set up YTMusic credentials first.")
        return None
    try:
        return YTMusic(auth_file)
    except Exception as e:
        print(f" 🚫 Error initializing YTMusic: {e}")
        return None

def transfer_playlist_to_ytmusic(sp, username: str):
    """Transfers a selected Spotify playlist to YouTube Music."""
    ytmusic = get_ytmusic_client()
    if not ytmusic:
        return

    playlist_uris = []
    playlist_names = []
    print()
    print(" Your Spotify playlists : ")
    print()

    playlists = sp.user_playlists(username)
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
        playlist_selection = input(" Enter a playlist number to transfer songs from or e to exit : ").strip()
        if playlist_selection == "e":
            break

        try:
            sel_idx = int(playlist_selection)
            if sel_idx < 0 or sel_idx >= len(playlist_uris):
                print_not_valid_choice()
                continue

            playlist_uri = playlist_uris[sel_idx]
            playlist_name = playlist_names[sel_idx]

            results = sp.playlist(playlist_uri)
            total_tracks = results["tracks"]["total"]
            search_query_list = []

            tracks = results["tracks"]
            items = tracks.get("items", [])
            print()
            print(" Collecting songs from Spotify.......")
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
                    song = trk.get("name", "")
                    artists = ", ".join(k.get("name", "") for k in trk.get("artists", []))
                    search_query_list.append(f"{song} {artists}")

                track_idx += 1

            print(f" Creating playlist '{playlist_name}' on YT Music.....")
            print()
            playlist_id = ytmusic.create_playlist(playlist_name, "Playlist made by Songfer", "PRIVATE")

            print(" Matching songs on YT Music.....")
            print()
            video_ids = []
            for query in search_query_list:
                try:
                    search_results = ytmusic.search(query, 'songs')
                    if search_results and 'videoId' in search_results[0]:
                        video_ids.append(search_results[0]['videoId'])
                except Exception:
                    pass

            print(" Songs being transferred......")
            print()
            status = ytmusic.add_playlist_items(playlist_id, video_ids, '', 'False')
            if status.get('status') == "STATUS_SUCCEEDED":
                print(f" ✅ Playlist : {playlist_name} successfully transferred to YT Music.")
            else:
                print(" 🚫 Something went wrong.")
            break

        except (ValueError, IndexError):
            print_not_valid_choice()

def transfer_liked_songs_to_ytmusic(sp):
    """Transfers all Spotify liked songs to a YouTube Music playlist."""
    ytmusic = get_ytmusic_client()
    if not ytmusic:
        return

    print()
    print(" Collecting Liked Songs from Spotify.......")
    print()

    liked_songs = sp.current_user_saved_tracks(limit=50)
    items = liked_songs.get("items", [])
    while liked_songs.get("next"):
        liked_songs = sp.next(liked_songs)
        items.extend(liked_songs.get("items", []))

    search_query_list = []
    for item in items:
        if item.get("track"):
            song = item["track"].get("name", "")
            artists = ", ".join(k.get("name", "") for k in item["track"].get("artists", []))
            search_query_list.append(f"{song} {artists}")

    print(f" Found {len(search_query_list)} liked songs.")
    print(" Creating playlist 'Spotify Liked Songs' on YT Music.....")
    print()
    playlist_id = ytmusic.create_playlist("Spotify Liked Songs", "Playlist made by Songfer", "PRIVATE")

    print(" Matching songs.....")
    print()
    start_time = time.time()
    video_ids = []
    for query in search_query_list:
        try:
            search_results = ytmusic.search(query, 'songs')
            if search_results and 'videoId' in search_results[0]:
                video_ids.append(search_results[0]['videoId'])
        except Exception:
            pass

    elapsed = time.time() - start_time
    print(f" Matching took {str(datetime.timedelta(seconds=elapsed))}")
    print()
    print(" Songs being transferred......")
    print()

    status = ytmusic.add_playlist_items(playlist_id, video_ids, '', 'False')
    if status.get('status') == "STATUS_SUCCEEDED":
        print(" ✅ Playlist : Spotify Liked Songs successfully created on YT Music.")
    else:
        print(" 🚫 Something went wrong.")
