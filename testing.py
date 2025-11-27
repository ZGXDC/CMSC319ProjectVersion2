#This is a python script providing unit tests and integration tests for the playlist generator code
import requests
from dotenv import load_dotenv
import os
from MainWorkspace import getAccessToken, getArtistIDAndGenre, createArtistInfoList, getTopTracks, getGenreFromMood
from MainWorkspace import validArtist

load_dotenv()

#UNIT TESTS
def testEnv():
    clientID = os.getenv("clientID")
    clientSecret = os.getenv("clientSecret")
    
    if clientID is None:
        print('FAIL clientID is None')
    if clientSecret is None:
        print("FAIL clientSecret is None")
    
    if clientID is not None and clientSecret is not None:
        print("ClientID: ", clientID)
        print("ClientSecret: ", clientSecret)
        print("testEnv tests passed")
        
def testGetAccessToken():
    token = getAccessToken()
    failure = False
    if token is None:
       print("ERROR: token is none")
       failure = True
    if len(token) < 10:
        print("ERROR: token is small")
        failure = True
    if token is not None:
        print("Access Token: ", token)
        
    if failure == False:
        print("Tests passed for getAccessToken()")

def testGetArtistIDAndGenre():
    artist = getArtistIDAndGenre("Nirvana")
    failure = False
    
    if artist is None:
        print("ERROR: artist is none")
    if "id" in artist is None:
        print("ERROR: id is none")
    if "name" in artist is None:
        print("ERROR: name is none")
    if "genres" in artist is None:
        print("ERROR: genres is none")
        
    #EXTREME CASES
    print(getArtistIDAndGenre("Nirvanaaaaa"))
    print(getArtistIDAndGenre("irvana"))
    #Should be None
    print(getArtistIDAndGenre("doesNotExist"))
    print(getArtistIDAndGenre("   "))
    print(getArtistIDAndGenre("\n"))
    print(getArtistIDAndGenre(""))
    print(getArtistIDAndGenre("??"))
  
def testCreateArtistInfoList():
    failure = False
    list = ["Taylor Swift", "Dua Lipa"]
    if len(createArtistInfoList(list))!=2:
        print("ERROR: not a complete list")
        failure = True

    list = ["Dua Lipa", "Dua Lipa"]
    if len(createArtistInfoList(list))!=1:
        print("ERROR: artists duplicated")
        failure = True
    
    list = ["\n", "", "     ", "\t"]
    if len(createArtistInfoList(list))!=0:
        print("ERROR: blanks not proccessed correctly")
        failure = True
    
    if failure ==False:
        print("tests passed")
    
def testGetTopTracks():
    failure = False
    
    #valid artists
    artists = {
        "Olivia Dean": {"id": "00x1fYSGhdqScXBRpSj3DW"}
    }
    
    tracks = getTopTracks(artists, getAccessToken())
    if len(tracks) != 1:
        print("ERROR: valid artist failed")
        failure=True
    
    #missing ID
    artists = {
        "The Beatles": {}
    }
    tracks = getTopTracks(artists, getAccessToken())
    if tracks != {}:
        print("ERROR: missing ID ")
        failure = True
        
    #API failure
    artists = {
        "Nirvana": {"id": "1"}
    }
    tracks = getTopTracks(artists, getAccessToken())
    if tracks["Nirvana"] != []:
        print("ERROR: api failure")
        failure = True
        
    #No Tracks
    artists = {
        "AC/DC": {"id": ""}
    }
    tracks = getTopTracks(artists, getAccessToken())
    print(tracks)
    if tracks != {}:
        print("ERROR: blank id")
        failure = True
    
    if failure==False:
        print("All tests passed")
    
    #3fMbdgg4jU18AjLCKBhRSm

def testGetGenreFromMood():
    failure = False
    #regular
    genres = getGenreFromMood("sad")
    
    if not genres:
        print("ERROR: returned nothing")
        failure = True
    #blank
    genres = getGenreFromMood("")
    if genres:
        print("ERROR: returned for a blank")
        failure = True
    
    #odd spelling
    genres = getGenreFromMood("SaD")
    if not genres:
        print("ERROR: didn't return for odd spelling")
        failure = True
    
    #added spaces 
    genres = getGenreFromMood("        sAD")
    if not genres:
        print("didn't return for added spaces")
        failure = True
    
    if failure==False:
        print("All tests passed")
            
def testValidArtist():
    failure =False
    #normal
    artistGenres = ["pop", "pop soul", "motown", "soul"] 
    moodGenres = ["pop", "dance pop", "electropop", "indie pop", "viral pop", "motown", "funk", "hip hop", "pop rap", "pop soul", "acoustic", "indie"]
    validity = validArtist(artistGenres, moodGenres)
    if validity ==False:
        print("ERROR on good input")
        failure = True
        
        
    #bad input
    artistGenres = ["metal", "modern rock", "blues"]
    validity = validArtist(artistGenres, moodGenres)
    if validity == True:
        print("ERROR returned true on bad input")
        failure = True
        
    #blank
    artistGenres = []
    validity = validArtist(artistGenres, moodGenres)
    if validity == True:
        print("ERROR: returned true on blank input")
    
    if failure ==False:
        print("all tests passed")
    
#testing unit tests for mood
#blank, sad, SAd, spaces sad, 
#PRINTING UNIT TESTS
print("UNIT TESTS\n")

print('LOADING ENV VARIABLES')
testEnv()

print('\nTEST FOR getAccessToken()')
testGetAccessToken()

print("\nTests for getArtistIdAndGenre")
testGetArtistIDAndGenre()

print("\n Tests for CreateArtistInfoList")
testCreateArtistInfoList()

print("\nTests for Top Tracks")
testGetTopTracks()

print("\nTests for GetGenreFromMood")
testGetGenreFromMood()

print("\nTests for Valid Artist")
testValidArtist()