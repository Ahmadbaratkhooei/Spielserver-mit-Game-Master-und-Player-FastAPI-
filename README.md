# Spielserver mit Game Master und Player (FastAPI)

# Game Master and Player
This project consists of two servers: Game Master and Player. The Game Master server handles the game logic, generating a random number and accepting guesses, while the Player server interacts with the Game Master, submitting guesses to find the generated number. The servers are containerized using Docker and can be orchestrated using Docker Compose and This project is written with FastApi.



![alt text](drawio.svg)
## Components
### Game Master
The Game Master server is responsible for:
- Starting new games
- Generating random numbers
- Processing guesses
- Maintaining game state

### Player
The Player server:
- Interacts with the Game Master to play the game
- Implements a binary search algorithm to guess numbers efficiently
- Can play multiple rounds of the game

## Technologies Used
- Python 3.10
- FastAPI
- SQLAlchemy (for database operations in Game Master)
- Docker
- Docker Compose

## Setup and Running

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone this repository
3. Build and run using Docker Compose:
4. The servers will be available at:
- Game Master: http://localhost:8000/doc
- Player: http://localhost:8001/doc

## API Endpoints

### Game Master

- `POST /start-game`: Start a new game
- `POST /submit-guess/{session_id}`: Submit a guess for a specific game
- `GET /health`: Check the health of the server
- `GET /hostname`: Get the hostname of the server
- `POST /clear-data`: Clear all game data from database
- `GET/get-all-data`: Get all data from the database

### Player

- `GET /play`: Play one or more multipele of the game and history
- `GET /health`: Check the health of the server
- `GET /hostname`: Get the hostname of the server

## Database

The Game Master server uses SQLite as its database. The database file `game_master.db` is stored in a Docker volume for persistence.
## docker and docker-compose
  - `docker-compose up --build `in vscode terminal
  -  login in docker 
  - `docker images`see images
  - `docker tag number-guessing-game1-player:latest  ahmadbarat/player`new tag for push in docker hub
  - `docker push ahmadbarat/player`
  - `docker tag number-guessing-game1-game-master:latest  ahmadbarat/game-master`
  - `docker push ahmadbarat/game-master`
## Docker hub
* push images in Docker hub
- player:`docker pull ahmadbarat/player:latest`
- Game master: `docker pull ahmadbarat/game-master:latest`


# Steps
- Create IAM user
- create VPC 12.0.0.0/16
- create public and private subnet (pu:12.0.1.0/24)(pr:12.0.2.0/24)
- create Nat Gateway
  - Attach to VPC
- Create public Route tables
  - **attach internet gatway(access to internet)**
  - associations to subnet public(Edit subnet associations)
- create private Route tables
  - associations to subnet private 
- Setup Nat Gateway
  - select public subnet and Allocate Elastic IP
- update subnet privat
  - **attach Nat Gateway(connet to internet )**
- create Bastion Host in public subnet 
- create player and game-master in privat subnet
- add security group (80-22--8000-8001)
  - install Docker 
```
#!/bin/bash
sudo apt update -y

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] 
https://download.docker.com/linux/ubuntu focal stable"

sudo apt update -y

sudo apt install docker-ce -y

sudo systemctl status docker
```
- Enter in Bastion Host with ssh 
  - touch new file for private key 
  - copy key in new file and only ready
    - `chmod 400 file-name`
  - ssh in player or game-master with private ipv4
- push Images from dokcer-hub
  - `docker images`see new image
   - `docker run -d -p 8000:8000 game-master-image`
   - `docker run -d -p 8001:8001 player-image`
   - `docker ps` show container 
   - `docker inspect id-container`more Inforamtin 
- in new cmd for player:`ssh -i key -L 8001:localhost:8001 ubuntu@<Public-IP-of-Bastion-Host>`
- in new cmd for game-master:`ssh -i number-guessing-game.pem -L 8000:privat ip:8000 ubuntu@Bastion Host ip`
- in Braowser:
  - `http://localhost:8001/docs#/` and `http://localhost:8000/docs#/`

* The connection between player and game-master is not established. I think the problem is with Docker Compose file`- CONFIG_SERVER_A_URL=http://game-master:8000`


## load Balancing and Target Groups
 - create target group 
   - instances
   - include as pending below
 - load balancers
   - Application load balancers
   - select mappings(need 2 AZ)
   - create security group for load balancers
   - select tatget group(public and private subnet).
   






















  
