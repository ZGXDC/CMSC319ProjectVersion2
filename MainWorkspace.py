from dotenv import load_dotenv
import os
import base64
import requests

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
    
    artist = items[0]
    if not artist["genres"]:
        artist["genres"] = ["uknown"]
    
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
        if name == "":
            print("Note: skipping blank entry")
            continue
        artistInfo = getArtistIDAndGenre(name)
        if artistInfo is None:
            print("Note: no artist found for ",name)
            continue
        else:
            spotifyName = artistInfo["name"]
            if spotifyName in artistDictionary:
                continue
            artistDictionary[spotifyName] = artistInfo
    return artistDictionary
    
