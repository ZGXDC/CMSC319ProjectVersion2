from dotenv import load_dotenv
import os
import base64
import requests
import random

#METHOD getAccessToken
# makes a post request to Spotify Web API url https://accounts.spotify.com/api/token
# using clientID and clientSecret credentials
# Uses Client Credentials Flow
# - accepts no parameters, returns an access token

def getAccessToken():
    clientID = os.getenv("clientID")
    clientSecret = os.getenv("clientSecret")
    
    authorizationString = f"{clientID}:{clientSecret}"
    #Client Credentials Floq requires that the string is Base64 Encoded 
    b64AuthString = base64.b64encode(authorizationString.encode()).decode()
    
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": f"Basic {b64AuthString}",
    }
   
    data = {
        "grant_type": "client_credentials"
    }
    
    #Makes HHTP Post request to URL, returns response object
    try:
        response = requests.post(url, headers=headers, data=data)
    except Exception as e:
        print("ERROR: ", e)
        print(response.text)
        
    if response.status_code !=200:
        raise Exception(response.status_code)
   
    #Converts JSON Response to Python Dictionary
    token = response.json()
    return token["access_token"]

#METHOD getArtistIDAndGenre
# finds an artist's ID and music genres from the Spotify Web API search URL
# takes a name parameter and makes a get request to the API
# returns a dictionary object with the artists ID, name, and genres
def getArtistIDAndGenre(name):
    if name == "" or name.strip()=="":
        return None
    
    accesstoken = getAccessToken()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {accesstoken}"}
    params = {
        "q": name,
        "type" : "artist",
        "limit": 1
    }

    #Makes a GET request to search url and returns a Response object with HTTP 
    try:
        response = requests.get(url, headers=headers, params=params)
    except Exception as e:
        print("ERROR: ", e)
    
    if response.status_code != 200:
        raise Exception(response.text)
   
   
    #puts json into python dictionary
    jsonData = response.json()
    
    items = jsonData.get("artists", {}).get("items", [])
    
    #If the input artist has no matches, none is returned
    if not items:
        return None
    
    #if artists returns no genre, replace genre with unknown
    artist = items[0]
    if not artist["genres"]:
        artist["genres"] = ["unknown"]
    
    artistInfo = {
        "id": artist["id"],
        "name": artist["name"],
        "genres": artist["genres"]
    }
    return artistInfo

#METHOD creatArtistInfoList
# creates a dictionary of artistInfo based on user input list of artists
# calls on getArtistIdAndGenre method
# accepts a list object of artists and returns a dictionary
def createArtistInfoList(list):
    artistDictionary = {}
    for name in list:
        name = name.strip()
        #Skips Blank Entries and prints warning
        if name == "":
            print("Note: skipping blank entry")
            continue
        artistInfo = getArtistIDAndGenre(name)
        #Warning if match is not returned for an artist
        if artistInfo is None:
            print("Note: no artist found for ",name)
            continue
        else:
            spotifyName = artistInfo["name"]
            #prevents duplicates
            if spotifyName in artistDictionary:
                continue
            artistDictionary[spotifyName] = artistInfo
    return artistDictionary

#METHOD getTopTracks
# creates a dictionary of each artist's top songs based on dictionary of artists info
# uses HTTP Get to spotify URL to get top songs for each listed artist
# appends the song id, name, and album to a list and finally puts that in a dicitionary paired with the artist name
def getTopTracks(dictionary, token):
    toptracks = {}
    
    for name, info in dictionary.items():
        id = info.get("id")
        
        if not id:
            print("Warning: no id found for ", name)
            continue
        
        url = "https://api.spotify.com/v1/artists/" + id + "/top-tracks?market=US"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print("ERROR: ", e)
        
        if response.status_code!=200:
            print("FAILURE to fetch tracks for ", name)
            toptracks[name] = []
            continue
        
        jsonData = response.json()
        tracks = jsonData.get("tracks", [])
        
        #Returns a warning if artist has no top tracks
        if not tracks:
            print("Warning: no tracks found for ", name)
            toptracks[name] = []
            continue
        
        #From Top Track Info, gets id, name, and album and puts it into one object
        #gets this from all top tracks 
        tracksInfo = []
        for t in tracks:
            tracksInfo.append({
                "id": t.get("id"),
                "name": t.get("name"),
                "album": t.get("album", {}).get("name")
            })
        #sets the artist name key value pair to be the 
        toptracks[name] = tracksInfo
    return toptracks

#METHOD getGenreFromMood
#takes a user input mood and returns a list of genres associated with that mood
#parameter userMood is the input mood from the user
#method has a dictionary of moods associated with a list of genres. 
#method formats the input and maps it to the dictionary and returns none if the mood is not found or the associated genres
def getGenreFromMood(userMood):
    
    moods = {
        "happy": ["pop", "dance pop", "electropop", "indie pop", "viral pop", "motown", "funk", "hip hop", "pop rap", "pop soul", "acoustic", "indie"],
        "sad": ["indie", "acoustic", 'singer-songwriter', "classic rock", "folk rock", "psychedelic rock", "soul", "neo soul", "classical", "orchestral", "trap", "modern rock", "soul blues"],
        "angry": ["rock", "metal", "alt-metal", "modern rock", "death metal", "pop rap", "trap"],
        "chill": ["lofi", "ambient", "chillhop", "soul", "neo soul", "rnb", "soul blues", "pop soul", "classic rock", "acoustic"]
    }
    
    userMood = userMood.strip()
    userMood = userMood.lower()
    
    if userMood not in moods:
        return None
    
    return moods[userMood]

#METHOD validArtist
#accepts a list of artistGenres and a list of moodGenres
#returns a boolean. Returns true if one of the artis's genres matches a moodGenre and false if otherwise
def validArtist(artistGenres, moodGenres):
    for genre in moodGenres:
        for g in artistGenres:
            if g in genre:
                return True
    return False

#METHOD matchArtistsToMood
def artistsToInclude(genres, artists):
    toInclude = {}
    
    for name, info in artists.items():
        if "unknown" in info["genres"]:
            toInclude[name] = info
        else:
            if validArtist(info["genres"], genres):
                toInclude[name] = info
    
    #if no artists match, return all artists
    if not toInclude:
        return artists
    else:
        return toInclude

#METHOD buildPlaylist
def buildPlaylist(topTracks, trackNum=3):
    playlist = []
    artistOrder = []
    for name, tracks in topTracks.items():
        numIncluded = min(trackNum, len(tracks))
        for i in range(numIncluded):
            artistOrder.append(name)
            playlist.append(tracks[i])
            
    return playlist, artistOrder
    
def printPlaylist(playlist, order):
    print("\nHere's your playlist!\n")
    i=0
    for track in playlist:
        print(track["name"], "--", order[i])
        i+=1

list = ["The Police", "Dominic Fike", "The Supremes", "Avril Lavigne"]
playlist, order = buildPlaylist(getTopTracks(artistsToInclude(["indie", "acoustic", 'singer-songwriter', "classic rock", "folk rock", "psychedelic rock", "soul", "neo soul", "classical", "orchestral", "trap", "modern rock", "soul blues"],createArtistInfoList(list)), getAccessToken()))
printPlaylist(playlist, order)
