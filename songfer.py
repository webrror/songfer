# run -> $ python3 songfer.py

from curses import echo
import os
from platform import platform
import sys
import json
import spotipy
import webbrowser
import time
import datetime
import subprocess

import spotipy.util as util
from json.decoder import JSONDecodeError
from ytmusicapi import YTMusic

# CONSTANT IMPORTS
import constants

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

# ---- METHODS ----

# Print "Not a valid choice! Try again" that's it
def printNotAValidChoice():
    print()
    print(" Not a valid choice! Try again")

def printToGoBack(letter):
    print()
    print(" Press any '"+letter+"' key to go back ....")
    print()

# Print instructions with step number
def printInstructions():
    instructionNumber = 1;
    for instruction in constants.INSTRUCTIONS:
        print(" "+str(instructionNumber)+"] "+instruction)
        instructionNumber += 1

# Print menu with index (starts from 0)
# Args - pass the menu array
def printMenu(menus):
    menuNumber = 1
    for menu in menus:
        print(" "+str(menuNumber)+" - "+menu)
        menuNumber += 1

# Get comma seperated values
# Args - pass the array of maps
def getCommaSeperatedValuesForArrayMaps(resultArray):
    values = ""
    for name in resultArray:
        if name == resultArray[-1]:
            values = values + name['name']
        else:
            values = values + name['name']+", "
    return values

# Get comma seperated values
# Args - pass the array
def getCommaSeperatedValuesForArray(resultArray):
    values = ""
    for value in resultArray:
        if value == resultArray[-1]:
            values = values + value
        else:
            values = values + value + ", "
    return values

# Get Album art functionality with 3 sub functionalities
def albumArt(currentSongIfAny):
    while True:
        print()
        print(" ---- "+constants.SELECT_SOURCE+" ---- ")
        print()
        printMenu(constants.ALBUM_ART_SUB_MENU)
        print()
        choice = input(" Your choice : ")

        if choice == "1": # Get album art of current playing song
            if (currentSongIfAny is None or currentSongIfAny == "") :
                print()
                print(color.BOLD+constants.CURRENTLY_NOTHING_PLAYING+color.END)
            else:
                print()
                print(" ✅ Album art opened in default browser.")
                print()
                webbrowser.open(currentSongIfAny)

        elif choice == "2": # Search for album art using songname, artist, album
            print()
            searchQuery = input(" Enter song name, artist or album : ")
            print()
            searchResults = spotifyObject.search(searchQuery,limit=4,type="album,track")
            resultCount = 0
            # print(searchResults)
            tracksResultArray = searchResults['tracks']['items']
            albumsResultArray = searchResults['albums']['items']
            resultsArray = tracksResultArray+albumsResultArray
            print(" "+str(len(resultsArray))+" Results : ")
            while True:
                print()
                for result in resultsArray:
                    artistNames = getCommaSeperatedValuesForArrayMaps(result['artists'])
                    if(result['type'] == "track"):
                        print(" "+str(resultCount)+" - 🎸 "+result['name']+" - "+artistNames)
                    elif(result['type'] == "album"):
                        print(" "+str(resultCount)+" - 💿 "+result['name']+" - "+artistNames)
                    resultCount += 1
                printToGoBack("e")
                choice = input(" Your choice : ")
                if(choice == "e"):
                    break
                else:
                    try:
                        choice = int(choice)
                        if(choice < 0 or choice >= len(resultsArray)):
                            resultCount = 0
                            printNotAValidChoice()
                            continue
                        else:
                            print()
                            print(" ✅ Album art opened in default browser.")
                            if(resultsArray[choice]['type'] == "track"):
                                webbrowser.open(resultsArray[choice]['album']['images'][0]['url'])
                            elif(resultsArray[choice]['type'] == "album"):
                                webbrowser.open(resultsArray[choice]['images'][0]['url'])
                            resultCount = 0
                    except ValueError:
                        resultCount = 0
                        printNotAValidChoice()
                        continue
                    
        elif choice == "3":
            def getPopularity(e): # used for sorting
                return 0 if e['popularity'] is None else e['popularity']
            print()
            searchQuery = input(" What's the artist name? : ")
            print()
            # Retrieve artist search results
            searchResults = spotifyObject.search(searchQuery,limit=5,type="artist")
            resultCount = 0
            resultArray = searchResults['artists']['items']
            resultArray.sort(reverse=True,key=getPopularity)
            print(" "+str(len(resultArray))+" Results : ")
            print()
            for artist in resultArray:
                if artist['genres'] is None or artist['genres'] == []:
                    genre = "NA"
                else:
                    genre = artist['genres'][0]
                print(" "+str(resultCount)+" - 🎨 "+artist['name']+" - "+genre+" - "+str(artist['followers']['total'])+" followers - 🔥"+str(artist['popularity']))
                resultCount += 1

            printToGoBack("e")
            choice = input(" Your choice : ")
            if(choice == "e"):
                break
            else:
                try:
                    choice = int(choice)   
                    artist = resultArray[choice]
                    genres = getCommaSeperatedValuesForArray(artist['genres'])
                    # Display artist details
                    print()
                    print(" 🎨 Artist Name - "+artist['name']) # name
                    print(" 👥 Followers - "+str(artist['followers']['total']) + " followers") # followers
                    print(" 🎶 Genres - "+genres) # genres

                    artistID = artist['id']
                    # Extract album data
                    albumResults = spotifyObject.artist_albums(artistID, limit=50)
                    filteredArray = []

                    for album in albumResults['items']:
                        if album['album_type'] == 'album' or album['album_type'] == 'single':
                            filteredArray.append(album)
                    print()
                    print(" "+str(len(filteredArray))+" albums :")
                    # print()
                    albumCount = 0
                    # Display all albums of the artist along with songs in them
                    for item in filteredArray:
                        print("\n "+str(albumCount)+" - 💿 " + item['name'])
                        # Extract track data
                        trackResults = spotifyObject.album_tracks(item['id'])
                        trackResults = trackResults['items']
                        print()
                        for song in trackResults:
                            print(song['name'], end=", ")
                        print()
                        albumCount += 1


                except ValueError:
                    resultCount = 0
                    printNotAValidChoice()
                    continue

            

            # # Album and track details
            # trackURIs = []
            # trackArt = []
            # z = 0

            # # Extract album data
            # albumResults = spotifyObject.artist_albums(artistID)
            # albumResults = albumResults['items']

            # # Display all albums of the artist along with songs in them
            # for item in albumResults:
            #     print(" ALBUM: " + item['name'])
            #     albumID = item['id']
            #     albumArt = item['images'][0]['url']

            #     # Extract track data
            #     trackResults = spotifyObject.album_tracks(albumID)
            #     trackResults = trackResults['items']

            #     for item in trackResults:
            #         print(" "+str(z) + ": " + item['name'])
            #         trackURIs.append(item['uri'])
            #         trackArt.append(albumArt)
            #         z+=1
            #     print()

            # # See album art
            # while True:
            #     songSelection = input(" Enter a number to see album art of a song or e to exit : ") 
            #     print()
            #     if songSelection == "e":
            #         break

            #     # Open art in browser
            #     print(" ✅ Album art opened in default browser.")
            #     print()
            #     webbrowser.open(trackArt[int(songSelection)])
 
        elif choice == "4": # Exit to main menu
            print()
            break

        else:
            printNotAValidChoice()

def listSongsFromPlaylist():  #! TO BE WORKED ON
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


# ---- AUTHORIZATION CODE FLOW ------

username = ""

# MAIN LOOP
while True:
    # if 'user.yaml' exists, read dev details from file
    if(os.path.exists(constants.USER_YML)):
        # reading user.yml file
        f = open(constants.USER_YML, "r")
        user_dict = {}
        for line in f:
            line = line.strip()
            name, var = line.partition(":")[::2]
            user_dict[name.strip()] = str(var)

        # setting environment variables
        username = format(user_dict['USERNAME'])
        os.environ["SPOTIPY_CLIENT_ID"] = format(user_dict['CLIENT'])
        os.environ["SPOTIPY_CLIENT_SECRET"] = format(user_dict['SECRET'])
        os.environ["SPOTIPY_REDIRECT_URI"] = constants.SPOTIPY_REDIRECT_URI
    # else show instructions to create an app in spotify dev portal and enter necassary details
    else:
        print()
        print(" ----- INSTRUCTIONS -----")
        print()
        printInstructions()
        
        f = open("user.yml", "x")
        f = open("user.yml", "a")

        # getting client_id, secret and username from user and storing to user.yml file
        print()
        client_id = input("Enter your Client ID : ")
        f.write("CLIENT:"+client_id+"\n")
        secret_client_id = input("Enter your Client Secret : ")
        f.write("SECRET:"+secret_client_id+"\n")
        username = input("Enter your Username : ")
        f.write("USERNAME:"+username+"\n")
        f.write("PORT:"+constants.PORT+"\n")
        f.close()

        # setting environment variables
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = secret_client_id
        os.environ["SPOTIPY_REDIRECT_URI"] = constants.SPOTIPY_REDIRECT_URI

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username, constants.SCOPES)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, constants.SCOPES)

    # Create our spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)
    # Retrieve user information
    user = spotifyObject.current_user()
    if user['product'] == "open":
        product = constants.FREE
    else:
        product = ""+color.GREEN+user['product'].capitalize()+color.END+""

    # Welcome message and display user info
    print()
    print(" ---------------------------------------------- ")
    print()
    # Show user's profile picture
    # As of July 8, 2023 - height not changing, so commented
    # if sys.platform == 'darwin':
    #     if os.environ["TERM_PROGRAM"] == 'iTerm.app':
    #         curl = subprocess.run(["curl", "-s", user['images'][0]['url']], capture_output=True)
    #         #subprocess.run(["sed", "'s/^/    /'"])
    #         subprocess.run(["viu", "-n", "-x", "1" , "-w", "10", "-h", "10", "-"], input=curl.stdout)
    print(" Welcome " + color.BOLD+user['display_name']+color.END + "!")
    print(" You have " + str(user['followers']['total']) + " followers.")
    print(" "+product+" User")
    print()
    print(" ---------------------------------------------- ")
    art = ""
    # Display info about current track playing, basic user information and current devices
    playback = spotifyObject.current_playback()
    if playback is None: # if playback has no activity
        print()
        print(color.BOLD+constants.CURRENTLY_NOTHING_PLAYING+color.END)
    elif playback['currently_playing_type'] == 'episode': # if playback is a podcast
        print()
        print(color.BOLD+constants.PODCASTS_NO_SUPPORT+color.END)
    elif playback['currently_playing_type'] == 'ad': # if playback is an ad
        print()
        print(color.BOLD+constants.AD_PLAYING+color.END)
    else: # if playback is a song
        devices = spotifyObject.devices()
        track = spotifyObject.current_user_playing_track()
        art = track['item']['album']['images'][0]['url'] # currently playing album art url
        artist = getCommaSeperatedValuesForArrayMaps(track['item']['artists']) # currently playing artist/'s name/s
        track = track['item']['name'] # currently playing track name
        deviceNumber=0
        if artist != "":
            print()
            print(constants.CURRENTLY_PLAYING, flush=True)
            print()
            # As of July 8, 2023, image support via viu is only for terminals with support for iTerm or Kitty graphics protocol
            # Only able to test on Mac, so limited to darwin and iterm.app
            if sys.platform == 'darwin':
                if os.environ["TERM_PROGRAM"] == 'iTerm.app':
                    curl = subprocess.run(["curl", "-s", art], capture_output=True)
                    subprocess.run(["viu", "-n", "-x", "1" ,"-w", "20", "-"], input=curl.stdout)
            # elif sys.platform == 'linux':
            #     curl = subprocess.run(["curl", "-s", art], capture_output=True)
            #     subprocess.run(["viu", "-n", "-x", "1" ,"-w", "20", "-"], input=curl.stdout)
            #     print()
            # else:
            #     print()

            print(" "+color.BOLD+"🎸  "+track+" - "+artist+color.END)
            print()
            print(" Devices :")
            print()
            while deviceNumber < len(devices['devices']):
                deviceName = devices['devices'][deviceNumber]['name']
                deviceType = devices['devices'][deviceNumber]['type']
                if devices['devices'][deviceNumber]['is_active']:
                    print("     "+color.BOLD+deviceName+" ("+deviceType+") ✅"+color.END)
                else:
                    print("     "+deviceName+" ("+deviceType+")")
                deviceNumber+=1
            print()
    
    # Menu for various functions
    print()
    print(" ----- MENU -----")
    print()
    printMenu(constants.MENU)
    print()
    choice = input(" Your choice : ")     

    if choice == "1": # Search for an artist and retreive album art of any songs by them
        albumArt(art)

    if choice == "2": # List user's playlist and songs within them
        listSongsFromPlaylist()

    # if choice == "3": # List user's playlists on Spotify and transfer songs within them to YT Music
        
    #     playlistURIs = []
    #     playlistNames = []
    #     z = 0 # Playlist counter
    #     offsetPlaylists = 0
    #     print()
    #     print(" Your Spotify playlists : ") 
    #     print()

    #     # Retrive Playlist details
    #     playlists = spotifyObject.user_playlists(username)
    #     totalPlaylists = playlists['total'] # total no. of playlists
    #     playlistResults = playlists['items']

    #     while z < totalPlaylists:
    #         playlistName = playlistResults[z-offsetPlaylists]['name']
    #         playlistURI = playlistResults[z-offsetPlaylists]['uri']
    #         print(" "+str(z) + ": " +playlistName) # displaying playlists in format - index : playlistname
    #         playlistURIs.append(playlistURI)
    #         playlistNames.append(playlistName)
    #         if (z+1)%50 == 0:
    #             playlistNext = spotifyObject.next(playlists)
    #             playlistResults = playlistNext['items']
    #             offsetPlaylists = z+1
    #         z+=1
    #     print()

    #     # Retreiving songs in specific playlist
    #     # heirarchy - playlist > tracks > items

    #     while True:
    #         print()
    #         playlistSelection = input(" Enter a playlist number to transfer songs from or e to exit : " )
    #         if playlistSelection == "e":
    #             break
            
    #         playlistURI = playlistURIs[int(playlistSelection)]
    #         playlistName = playlistNames[int(playlistSelection)]

    #         results = spotifyObject.playlist(playlistURI)
    #         nooftracks = results["tracks"]["total"]; # total tracks in a playlist

    #         song_list = []
    #         album_list = []
    #         artist_list = []
    #         releaseDate_list = []
    #         searchQueryList = []

    #         tracks = results["tracks"]
    #         items = tracks["items"]
    #         offset = 0
    #         x = 0 # Track counter
    #         print()
    #         print(" Collecting songs from Spotify.......")
    #         print()
    #         while x < nooftracks:
    #             song = items[x-offset]["track"]["name"]
    #             album = items[x-offset]["track"]["album"]["name"]
    #             release_date = items[x-offset]["track"]["album"]["release_date"]
    #             artists = [k["name"] for k in items[x-offset]["track"]["artists"]]
    #             artists = ','.join(artists)
    #             # print(str(x)+" : "+song+" - "+artists) # uncomment if you want to display all songs in the playlist
    #             song_list.append(song)
    #             album_list.append(album)
    #             releaseDate_list.append(release_date)
    #             artist_list.append(artists)
    #             searchQueryList.append(song+" "+artists)
    #             if (x+1)%100 == 0:
    #                 tracks= spotifyObject.next(tracks)
    #                 if tracks is None:
    #                     break
    #                 else:
    #                     items = tracks["items"]
    #                     offset = x+1
    #             x+=1
    #         print()

    #         ######## YT MUSIC (DESTINATION) #############

    #         print(" Creating playlist on YT Music.....")
    #         print()

    #         # Creating playlist on YT Music

    #         ytmusic = YTMusic('headers_auth.json')
    #         playlistId = ytmusic.create_playlist(playlistName, "Playlist made by Songfer", 'PRIVATE')

    #         print(" Matching songs.....")
    #         print()

    #         # Searching for retrived songs on YT Music

    #         y = 0
    #         videoIds = []

    #         while y < nooftracks:
    #             searchQ = searchQueryList[y]
    #             searchResults = ytmusic.search(searchQ, 'songs')
    #             videoIds.append(searchResults[0]['videoId'])
    #             # print(searchResults[0]['videoId'])
    #             y+=1

    #         print(" Songs being transferred......")
    #         print()

    #         # adding songs to the playlist created on YT Music

    #         status = ytmusic.add_playlist_items(playlistId, videoIds, '', 'False')
    #         if status['status'] == "STATUS_SUCCEEDED":
    #             print(" ✅ Playlist : "+playlistName+" successfully transferred to YT Music.")
    #         else:
    #             print(" 🚫 Something went wrong.")

    # if choice == "8": # Transfer Spotify Liked songs  to YT Music

    #     # Retrieve Liked songs
    #     likedSongs = spotifyObject.current_user_saved_tracks(20)
    #     nooftracks = likedSongs["total"]; # total no. of liked songs

    #     song_list = []
    #     artist_list = []
    #     searchQueryList = []

    #     items = likedSongs["items"]
    #     offsetLiked = 0
    #     b = 0 # Track counter

    #     # Retreive song names and artists from Spotify
        
    #     print()
    #     print(" Collecting songs from Spotify.......")
    #     print()

    #     while likedSongs["next"]:
    #         likedSongs = spotifyObject.next(likedSongs)
    #         items.extend(likedSongs["items"])

    #     for i in items:
    #         song = i['track']['name']
    #         artists = [k["name"] for k in i["track"]["artists"]]
    #         artists = ','.join(artists)
    #         # print(str(b)+" : "+song+" - "+artists)
    #         song_list.append(song)
    #         artist_list.append(artists)
    #         searchQueryList.append(song+" "+artists)
    #         b+=1

    #     ######## YT MUSIC (DESTINATION) #############

    #     # Creating playlist on YT Music

    #     print(" Creating playlist on YT Music.....")
    #     print()

    #     ytmusic = YTMusic('headers_auth.json')
    #     playlistId = ytmusic.create_playlist("Spotify Liked Songs", "Playlist made by Songfer", 'PRIVATE')

    #     # Searching for retrived songs on YT Music

    #     print(" Matching songs.....")
    #     print()
    #     start = time.time()
    #     y = 0
    #     videoIds = []

    #     for query in searchQueryList:
    #         searchResults = ytmusic.search(query, 'songs')
    #         videoIds.append(searchResults[0]['videoId'])

    #     end = time.time()
    #     seconds = end-start
    #     print(" Matching took "+str(datetime.timedelta(seconds=seconds)))
    #     print()
    #     # took 0:16:13.568975 for 2240 songs, may vary
    #     print(" Songs being transferred......")
    #     print()

    #     # adding songs to the playlist created on YT Music

    #     status = ytmusic.add_playlist_items(playlistId, videoIds, '', 'False')
    #     if status['status'] == "STATUS_SUCCEEDED":
    #         print(" ✅ Playlist : Spotify Liked Songs successfully created on YT Music.")
    #     else:
    #         print(" 🚫 Something went wrong.")

    if choice == "4": # Exit application
        print()
        break
