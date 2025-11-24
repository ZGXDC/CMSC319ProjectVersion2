#This is a python script providing unit tests and integration tests for the playlist generator code

from dotenv import load_dotenv
import os

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
 
    
print("UNIT TESTS")
print('LOADING ENV VARIABLES')
testEnv()