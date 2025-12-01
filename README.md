# Welcome to Spotify Mood Playlist Generator!

This is microservices project written in Python as part of the CMSC 319 Software Engineering Concepts Class. This project ideally generates a playlist for users based on user-input mood and artists. It access the Spotify Web API and matches songs based on user input, ultimately outputting them for the user. 
The program is built in one main program titled MainWorkspace.py. This program has a series of methods that attempt to perform just one function, acting as the services aspect of the microservices project. 

## Features 
- Input a mood and favorite artists
- Maps mood to a list of genres and genres to favorite artists
- Selects popular songs from artists
- Outputs the list of tracks

## Run Instructions
1. Clone the Repository
2. Create your own virtual environment
3. Install dependencies 

Follow these instructions to install dependencies:
- run pip install -r requirements.txt in terminal
4. Create a .env file by copying a provided one into the root directory or creating your own. 

Follow these instructions to create a .env file:
- Name the file .env
- The file should have two variables, namely clientID and clientSecret
- Set those variables equal to your own credentials from the Spotify Developer Website
- view .env.example for a better understanding
5. Run the project

## Dependencies
- Python 3.12+
- python-dotenv
- requests

## Testing
testing.py provides a suite of unit tests and integration tests for the code. 
Includes a series of unit tests for methods (services) that do not rely on HTTP requests or other methods. 

Integration Tests are written for methods use HTTP requests since they rely on the workings of an external API. In addition, integeration tests are provided for methods that call another method internally. 

## OpenAPIDocs
openapi.json provides OpenAPI doc-style example requests and responses to the Spotify API in json format. It provides examples requests and responses for three methods (services) that call the Spotify API which includes getting an access token, getting top tracks, and getting artist id/genres. 

HTTP GET requests are sent to the following urls:
- https://api.spotify.com/v1/search
- https://api.spotify.com/v1/artists/3WrFJ7ztbogyGnTHbHJFl2/top-tracks?market=US
- https://accounts.spotify.com/api/token