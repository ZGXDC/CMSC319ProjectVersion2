#This is a python script providing unit tests and integration tests for the playlist generator code
import requests
from dotenv import load_dotenv
import os
from MainWorkspace import getAccessToken, getArtistIDAndGenre, createArtistInfoList, getTopTracks, getGenreFromMood
from MainWorkspace import validArtist, artistsToInclude, buildPlaylist

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
def testBuildPlaylist():
    failure = False
    topTracks = {'Rihanna': [{'id': '5EcG8eMMlwkHRVa4aTR1qd', 'name': "Breakin' Dishes", 'album': 'Good Girl Gone Bad'}, 
                             {'id': '5WQQIDU3HRaMyPkob8mpFb', 'name': 'Where Have You Been', 'album': 'Talk That Talk'}, 
                             {'id': '6qn9YLKt13AGvpq9jfO8py', 'name': 'We Found Love', 'album': 'Talk That Talk'}, 
                             {'id': '2ENexcMEMsYk0rVJigVD3i', 'name': 'Only Girl (In The World)', 'album': 'Loud'}, 
                             {'id': '1Jo0Zg7XlrA6z0mFTZVdkn', 'name': "Don't Stop The Music", 'album': 'Good Girl Gone Bad'}, 
                             {'id': '5oO3drDxtziYU2H1X23ZIp', 'name': 'Love On The Brain', 'album': 'ANTI (Deluxe)'}, 
                             {'id': '2yPoXCs7BSIUrucMdK5PzV', 'name': 'Umbrella', 'album': 'Good Girl Gone Bad'}, 
                             {'id': '789CxjEOtO76BVD1A9yJQH', 'name': 'Stay', 'album': 'Unapologetic (Edited Version)'}, 
                             {'id': '7ySUcLPVX7KudhnmNcgY2D', 'name': 'S&M', 'album': 'Loud'}, 
                             {'id': '1z9kQ14XBSN0r2v6fx4IdG', 'name': 'Diamonds', 'album': 'Unapologetic (Edited Version)'}],
                 
                 'Olivia Dean': [{'id': '1qbmS6ep2hbBRaEZFpn7BX', 'name': 'Man I Need', 'album': 'Man I Need'}, 
                                 {'id': '6sGIMrtIzQjdzNndVxe397', 'name': 'So Easy (To Fall In Love)', 'album': 'The Art of Loving'}, 
                                 {'id': '7gKxCvTDWwV9wBhdeBbr3l', 'name': 'Nice To Each Other', 'album': 'Nice To Each Other'}, 
                                 {'id': '5SruEBX3KpgpDvEcIuN53P', 'name': 'Baby Steps', 'album': 'The Art of Loving'}, 
                                 {'id': '3Vd4fHzwS6pBS3muymjiDi', 'name': 'Let Alone The One You Love', 'album': 'The Art of Loving'}, 
                                 {'id': '36vmaZyO0iAE6FZ7287fg2', 'name': 'Dive', 'album': 'Messy'}, 
                                 {'id': '312z6PZ8wwREck8613PkJk', 'name': 'A Couple Minutes', 'album': 'The Art of Loving'}, 
                                 {'id': '3cPoiK69oQ1SdbB2j2ulGm', 'name': 'The Hardest Part', 'album': 'Messy'}, 
                                 {'id': '1XwbJNPOcLuSRTQNR9zz4r', 'name': 'Lady Lady', 'album': 'Lady Lady'}, 
                                 {'id': '6tHVEMyRfxGgQuXRzl2yOF', 'name': "I've Seen It", 'album': 'The Art of Loving'}]}
    
    #valid input
    playlist, order = buildPlaylist(topTracks)
    if playlist==[] or order==[]:
        print("ERROR for valid input")
        failure = True
    
    #empty input
    topTracks = {}
    playlist, order = buildPlaylist(topTracks)
    if playlist !=[] or order != []:
        print("Error on blank input")
        failure = True
    
    if failure == False:
        print("tests passed")

#INTEGRATION TEST
def testFullProgram():
    failure = False
   #valid input
    mood = "happy"
    artists = ["Olivia Dean", "Metallica", "Michael Jackson", "Bob Dylan", "Def Leppard"]
    
    token = getAccessToken()
    if token is None:
        print("ERROR with token")
        failure = True
        
    infoList = createArtistInfoList(artists)
    if len(infoList)<1:
        print("ERROR artist info list is not long enough")
        failure = True
    
    moodGenres = getGenreFromMood(mood)
    if moodGenres is None:
        print("ERROR returning moods")
        failure = True
        
    includedArtists = artistsToInclude(moodGenres, infoList)
    if includedArtists is None:
        print("ERROR no included artists")
        failure = True
    
    topTracks = getTopTracks(includedArtists, token)
    if topTracks is None:
        print("ERROR in getting top tracks")
        failure = True
    
    playlist, order = buildPlaylist(topTracks)
    if playlist == None or order == None:
        print("Error in building playlist")
        failure = True
    
     #blank input
    mood = ""
    artists = [""]
    token = getAccessToken()
    if token is None:
        print("ERROR with token")
        failure = True
        
    infoList = createArtistInfoList(artists)
    if len(infoList)!=0:
        print("ERROR artist info list is not long enough")
        failure = True
    
    moodGenres = getGenreFromMood(mood)
    if moodGenres is not None:
        print("ERROR returning moods")
        failure = True
        
    includedArtists = artistsToInclude(moodGenres, infoList)
    if includedArtists != {}:
        print("ERROR included artists")
        failure = True
    
    topTracks = getTopTracks(includedArtists, token)
    if topTracks != {}:
        print("ERROR in getting top tracks")
        failure = True
    
    playlist, order = buildPlaylist(topTracks)
    if playlist != [] or order != []:
        print("Error in building playlist")
        failure = True
    
    if failure == False:
        print("all tests passed")
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
    
    #3fMbdgg4jU18AjLCKBhRSm
def testArtistsToInclude():
    failure = False
    genres = ["pop", "metal", "blues"]
    artists = {'Rihanna': {'id': '5pKCCKE2ajJHZ9KAiaK11H', 'name': 'Rihanna', 'genres': ['unknown']}, 
               'Olivia Dean': {'id': '00x1fYSGhdqScXBRpSj3DW', 'name': 'Olivia Dean', 'genres': ['pop soul']}, 
               'Michael Jackson': {'id': '3fMbdgg4jU18AjLCKBhRSm', 'name': 'Michael Jackson', 'genres': ['unknown']}, 
               'ROSALÍA': {'id': '7ltDVBr6mKbRvohxheJ9h1', 'name': 'ROSALÍA', 'genres': ['latin']}}
    #valid input
    include = artistsToInclude(genres, artists)
    if include == []:
        print("ERROR on valid input")
        failure = True
    
    #empty input
    artists = {}
    include = artistsToInclude(genres, artists)
    if include != {}:
        print("ERROR on empty input")
        failure = True
    
    if failure == False:
        print("Tests passed")

#PRINTING UNIT TESTS
print("UNIT TESTS\n")

print('LOADING ENV VARIABLES')
testEnv()

print("\nTests for GetGenreFromMood")
testGetGenreFromMood()

print("\nTests for Valid Artist")
testValidArtist()

print("\nTests for buildPlaylist")
testBuildPlaylist()

#INTEGRATION TESTS
#Tests rely on data flowing between methods and more than one method working
#Tests of methods that require HTTP requests and the external API working
print("\nINTEGRATION TESTS")

print("\nTests for Top Tracks")
testGetTopTracks()

print("\n Tests for CreateArtistInfoList")
testCreateArtistInfoList()

print('\nTEST FOR getAccessToken()')
testGetAccessToken()

print("\nTests for getArtistIdAndGenre")
testGetArtistIDAndGenre()

print("\nTests for artistsToInclude")
testArtistsToInclude()

print("\nTests for Full Program")
testFullProgram()