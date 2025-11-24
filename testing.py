#This is a python script providing unit tests and integration tests for the playlist generator code
import requests
from dotenv import load_dotenv
import os
from MainWorkspace import getAccessToken, getArtistIDAndGenre

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
  

#PRINTING UNIT TESTS
print("UNIT TESTS\n")

print('LOADING ENV VARIABLES')
testEnv()

print('\nTEST FOR getAccessToken()')
testGetAccessToken()

print("\nTests for getArtistIdAndGenre")
testGetArtistIDAndGenre()