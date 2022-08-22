# $ python3 spot.py user_id

import os
import sys
import json
import spotipy
import webbrowser
import time
import datetime

import spotipy.util as util
from json.decoder import JSONDecodeError
from ytmusicapi import YTMusic

# ---- THEME -----

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# ---- AUTHORIZATION CODE FLOW ------

username = ""

# Declare scope
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-library-read'

# Main loop
while True:
    
    if(os.path.exists('user.yml')):
        # reading user.yml file
        f = open("user.yml", "r")
        user_dict = {}
        for line in f:
            line = line.strip()
            name, var = line.partition(":")[::2]
            user_dict[name.strip()] = str(var)

        # setting environment variables
        username = format(user_dict['USERNAME'])
        os.environ["SPOTIPY_CLIENT_ID"] = format(user_dict['CLIENT'])
        os.environ["SPOTIPY_CLIENT_SECRET"] = format(user_dict['SECRET'])
        os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8888/callback/'
    else:
        print()
        print(" ----- INSTRUCTIONS -----")
        print()
        port = '8888'
        instructions = [
            "Go to the Spotify dashboard - https://developer.spotify.com/dashboard/applications",
            "Click create an app and note the Client ID and Client Secret",
            "Now click `Edit Settings`",
            "Add `http://localhost:"+port+"/callback` to the Redirect URIs",
            "Note your username from account page - https://www.spotify.com/account/overview/ ",
            "You are now ready to authenticate with Spotify!",
        ]
        number = 1;
        for item in instructions:
            print(" "+str(number)+"] "+item)
            number += 1
        
        f = open("user.yml", "x")
        f = open("user.yml", "a")

        # getting client_id and secret from user and storing to user.yml file
        print()
        client_id = input("Enter your Client ID : ")
        f.write("CLIENT:"+client_id+"\n")
        secret_client_id = input("Enter your Client Secret : ")
        f.write("SECRET:"+secret_client_id+"\n")
        username = input("Enter your Username : ")
        f.write("USERNAME:"+username+"\n")
        f.write("PORT:"+port+"\n")
        f.close()

        # setting environment variables
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = secret_client_id
        os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8888/callback/'

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)

    # Create our spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)
    # Retrieve user information
    user = spotifyObject.current_user()
    displayName = user['display_name']
    followers = user['followers']['total']
    if user['product'] == "open":
        product = "Free"
    else:
        product = user['product']


    # Welcome message and display user info
    
    print()
    print("-------------------------------------------- ")
    print()
    print(" Welcome " + color.BOLD+displayName+color.END + "!")
    print(" You have " + str(followers) + " followers.")
    print(" "+product +" user")
    print()
    print("-------------------------------------------- ")
    
    # Display info about current track playing, basic user information and current devices
    playback = spotifyObject.current_playback()
    if playback is None: # if no activity
        print()
        print(color.BOLD+" Currently nothing playing."+color.END)
    elif playback['currently_playing_type'] == 'episode': # if playback is a podcast
        print()
        print(color.BOLD+" Podcasts not supported."+color.END)
    elif playback['currently_playing_type'] == 'ad': # if playback is an ad
        print()
        print(color.BOLD+" Ad playing."+color.END)
    else: # if playback is a song
        devices = spotifyObject.devices()
        track = spotifyObject.current_user_playing_track()
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']
        d=0
        if artist != "":
            print()
            print(" Currently playing "+color.BOLD+ artist + " - " + track+" 🎸"+color.END)
            print()
            print(" Devices :")
            print()
            while d < len(devices['devices']):
                deviceName = devices['devices'][d]['name']
                deviceType = devices['devices'][d]['type']
                if devices['devices'][d]['is_active']:
                    print("     "+color.BOLD+deviceName+" ("+deviceType+") ✅"+color.END)
                else:
                    print("     "+deviceName+" ("+deviceType+")")
                d+=1
            print()
    
    # Menu for various functions
    print()
    print(" 1 - Get album art from Spotify")
    print(" 2 - List your songs in a playlist on Spotify")
    print(" 3 - Transfer songs from Spotify playlist to Youtube Music")
    print(" 4 - Transfer Liked Songs from Spotify to Youtube Music")
    print(" 0 - Exit")
    print()
    choice = input(" Your choice : ")     

    if choice == "1": # Search for an artist and retreive album art of any songs by them
        print()
        searchQuery = input(" What's the artist name? : ") 
        print()

        # Retrieve artist search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        # Display first artist details (More options to be added)
        artist = searchResults['artists']['items'][0]
        print(" 🎨 Artist Name - "+artist['name']) # name
        print(" 👥 Followers - "+str(artist['followers']['total']) + " followers") # followers
        genreList = []
        for genre in artist['genres']:
            genreList.append(genre)
        print(" 🎶 Genres - "+','.join(genreList)) # genres
        print()

        artistID = artist['id']

        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        # Display all albums of the artist along with songs in them
        for item in albumResults:
            print(" ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(" "+str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album art
        while True:
            songSelection = input(" Enter a number to see album art of a song or e to exit : ") 
            print()
            if songSelection == "e":
                break

            # Open art in browser
            print(" ✅ Album art opened in default browser.")
            print()
            webbrowser.open(trackArt[int(songSelection)])

    if choice == "2": # List user's playlist and songs within them

        playlistURIs = []
        z = 0 #Playlist counter
        offsetPlaylists = 0
        print()
        print(" Your Spotify playlists : ") 
        print()

        # Retrive Playlist details
        playlists = spotifyObject.user_playlists(username)
        totalPlaylists = playlists['total'] # total no. of playlists
        playlistResults = playlists['items']

        while z < totalPlaylists:
            playlistName = playlistResults[z-offsetPlaylists]['name']
            playlistURI = playlistResults[z-offsetPlaylists]['uri']
            print(" "+str(z) + ": " +playlistName) # displaying playlist in format - index : playlistname
            playlistURIs.append(playlistURI)
            if (z+1)%50 == 0:
                playlistNext = spotifyObject.next(playlists)
                playlistResults = playlistNext['items']
                offsetPlaylists = z+1
            z+=1
        print()

        # Songs in specific playlist
        # heirarchy - playlist > tracks > items

        while True:
            playlistSelection = input(" Enter the index number of a playlist to see all songs in it or e to exit : " )
            if playlistSelection == "e":
                break  
            playlistURI = playlistURIs[int(playlistSelection)] 
            results = spotifyObject.playlist(playlistURI)
            nooftracks = results["tracks"]["total"]; # total tracks in a playlist

            song_list = []
            album_list = []
            artist_list = []
            releaseDate_list = []

            tracks = results["tracks"]
            items = tracks["items"]
            offset = 0
            x = 0 # Track counter
            print()
            print(" Songs in the playlist :")
            print()
            while x < nooftracks:
                song = items[x-offset]["track"]["name"]
                album = items[x-offset]["track"]["album"]["name"]
                release_date = items[x-offset]["track"]["album"]["release_date"]
                artists = [k["name"] for k in items[x-offset]["track"]["artists"]]
                artists = ','.join(artists)
                print(" "+str(x)+" : "+song+" - "+artists) # displaying songs in format :- index : songname - artists
                song_list.append(song)
                album_list.append(album)
                releaseDate_list.append(release_date)
                artist_list.append(artists)
                if (x+1)%100 == 0:
                    tracks = spotifyObject.next(tracks)
                    if tracks is None:
                        break
                    else:
                        items = tracks["items"]
                        offset = x+1
                x+=1

            # Saving details to a .csv file (songlist.csv)

            final_data = list(zip(song_list,artist_list,album_list,releaseDate_list))
            import csv
            Details = ["Name","Artists","Album","Release Date"]
            rows = final_data
            with open("songlist.csv", 'w', newline='') as f:
                write = csv.writer(f)
                write.writerow(Details)
                write.writerows(rows)

            f.close()
            print()
            print(" ✅ Details saved in 'songlist.csv' file.")
            break

    if choice == "3": # List user's playlists on Spotify and transfer songs within them to YT Music
        
        playlistURIs = []
        playlistNames = []
        z = 0 # Playlist counter
        offsetPlaylists = 0
        print()
        print(" Your Spotify playlists : ") 
        print()

        # Retrive Playlist details
        playlists = spotifyObject.user_playlists(username)
        totalPlaylists = playlists['total'] # total no. of playlists
        playlistResults = playlists['items']

        while z < totalPlaylists:
            playlistName = playlistResults[z-offsetPlaylists]['name']
            playlistURI = playlistResults[z-offsetPlaylists]['uri']
            print(" "+str(z) + ": " +playlistName) # displaying playlists in format - index : playlistname
            playlistURIs.append(playlistURI)
            playlistNames.append(playlistName)
            if (z+1)%50 == 0:
                playlistNext = spotifyObject.next(playlists)
                playlistResults = playlistNext['items']
                offsetPlaylists = z+1
            z+=1
        print()

        # Retreiving songs in specific playlist
        # heirarchy - playlist > tracks > items

        while True:
            print()
            playlistSelection = input(" Enter a playlist number to transfer songs from or e to exit : " )
            if playlistSelection == "e":
                break
            
            playlistURI = playlistURIs[int(playlistSelection)]
            playlistName = playlistNames[int(playlistSelection)]

            results = spotifyObject.playlist(playlistURI)
            nooftracks = results["tracks"]["total"]; # total tracks in a playlist

            song_list = []
            album_list = []
            artist_list = []
            releaseDate_list = []
            searchQueryList = []

            tracks = results["tracks"]
            items = tracks["items"]
            offset = 0
            x = 0 # Track counter
            print()
            print(" Collecting songs from Spotify.......")
            print()
            while x < nooftracks:
                song = items[x-offset]["track"]["name"]
                album = items[x-offset]["track"]["album"]["name"]
                release_date = items[x-offset]["track"]["album"]["release_date"]
                artists = [k["name"] for k in items[x-offset]["track"]["artists"]]
                artists = ','.join(artists)
                # print(str(x)+" : "+song+" - "+artists) # uncomment if you want to display all songs in the playlist
                song_list.append(song)
                album_list.append(album)
                releaseDate_list.append(release_date)
                artist_list.append(artists)
                searchQueryList.append(song+" "+artists)
                if (x+1)%100 == 0:
                    tracks= spotifyObject.next(tracks)
                    if tracks is None:
                        break
                    else:
                        items = tracks["items"]
                        offset = x+1
                x+=1
            print()

            ######## YT MUSIC (DESTINATION) #############

            print(" Creating playlist on YT Music.....")
            print()

            # Creating playlist on YT Music

            ytmusic = YTMusic('headers_auth.json')
            playlistId = ytmusic.create_playlist(playlistName, "Playlist made by Songfer", 'PRIVATE')

            print(" Matching songs.....")
            print()

            # Searching for retrived songs on YT Music

            y = 0
            videoIds = []

            while y < nooftracks:
                searchQ = searchQueryList[y]
                searchResults = ytmusic.search(searchQ, 'songs')
                videoIds.append(searchResults[0]['videoId'])
                # print(searchResults[0]['videoId'])
                y+=1

            print(" Songs being transferred......")
            print()

            # adding songs to the playlist created on YT Music

            status = ytmusic.add_playlist_items(playlistId, videoIds, '', 'False')
            if status['status'] == "STATUS_SUCCEEDED":
                print(" ✅ Playlist : "+playlistName+" successfully transferred to YT Music.")
            else:
                print(" 🚫 Something went wrong.")

    if choice == "4": # Transfer Spotify Liked songs  to YT Music

        # Retrieve Liked songs
        likedSongs = spotifyObject.current_user_saved_tracks(20)
        nooftracks = likedSongs["total"]; # total no. of liked songs

        song_list = []
        artist_list = []
        searchQueryList = []

        items = likedSongs["items"]
        offsetLiked = 0
        b = 0 # Track counter

        # Retreive song names and artists from Spotify
        
        print()
        print(" Collecting songs from Spotify.......")
        print()

        while likedSongs["next"]:
            likedSongs = spotifyObject.next(likedSongs)
            items.extend(likedSongs["items"])

        for i in items:
            song = i['track']['name']
            artists = [k["name"] for k in i["track"]["artists"]]
            artists = ','.join(artists)
            # print(str(b)+" : "+song+" - "+artists)
            song_list.append(song)
            artist_list.append(artists)
            searchQueryList.append(song+" "+artists)
            b+=1

        ######## YT MUSIC (DESTINATION) #############

        # Creating playlist on YT Music

        print(" Creating playlist on YT Music.....")
        print()

        ytmusic = YTMusic('headers_auth.json')
        playlistId = ytmusic.create_playlist("Spotify Liked Songs", "Playlist made by Songfer", 'PRIVATE')

        # Searching for retrived songs on YT Music

        print(" Matching songs.....")
        print()
        start = time.time()
        y = 0
        videoIds = []

        for query in searchQueryList:
            searchResults = ytmusic.search(query, 'songs')
            videoIds.append(searchResults[0]['videoId'])

        end = time.time()
        seconds = end-start
        print(" Matching took "+str(datetime.timedelta(seconds=seconds)))
        print()
        # took 0:16:13.568975 for 2240 songs, may vary
        print(" Songs being transferred......")
        print()

        # adding songs to the playlist created on YT Music

        status = ytmusic.add_playlist_items(playlistId, videoIds, '', 'False')
        if status['status'] == "STATUS_SUCCEEDED":
            print(" ✅ Playlist : Spotify Liked Songs successfully created on YT Music.")
        else:
            print(" 🚫 Something went wrong.")

    if choice == "0": # Exit application
        print()
        break