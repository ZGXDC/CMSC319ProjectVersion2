# Welcome to Spotify Mood Playlist Generator!

This is microservices project written in Python as part of the CMSC 319 Intro to Software Engineering Class. This project ideally generates a playlist for users based on user-input mood and artists. It access the Spotify Web API and matches songs based on user input, ultimately outputting them for the user. 

## Features 
- Input a mood and favorite artists
- Maps user prefernces to songs from Spotify Web API
- Outputs the list of tracks

## Run Instructions
1. Clone the Repository
2. Create your own virtual environment
3. Install dependencies using pip install -r requirements.txt
4. Create a .env file by copying a provided one into the root directory or creating your own. 
- Name the file .env
- The file should have two variables, namely clientID and clientSecret
- Set those variables equal to your own credentials from the Spotify Developer Website
5. Run the project

## Dependencies
1. Python 3.12+
2. python-dotenv
3. requests