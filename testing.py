#This is a python script providing unit tests and integration tests for the playlist generator code
import requests
from dotenv import load_dotenv
import os
from MainWorkspace import getAccessToken, getArtistIDAndGenre, createArtistInfoList, getTopTracks

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