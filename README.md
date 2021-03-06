# multiplayerTextAdventure

# Run:
### Server
1. navigate to directory with the server files
2. execute 'python3 server.py' command

### Client
1. Navigate to directory with the client files 
2. execute 'python3 main.py' command
3. experience the adventure!


# General Game Controls:

- The horizontal Text Box at the bottom of the window is used for all text entry
- The tag to the left of the bar shows the expected information input (in this case it's 'Enter your Player Name:'):
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/bottomBarGui.PNG)

- The vertical text boxes are used to display game information from the server (rooms, messages, other players, monsters, etc.)
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/gui1.PNG)


# Setup:

Begin by entering your player information (Press 'Enter' after entering)
1. Enter your Name

2. Enter the following values as prompted (total of the three should be between 0 and 500)
- Attack
- Defense
- Regeneration
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/gui2.PNG)

3. Enter the letter 'S' to enter the game
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiStart.PNG)

# Gameplay:

Upon starting the game notice that you're now seeing (from left most column to right)
- Updated stats 
- Room (your room is the one in between the asteriks)
- The characters and monsters in your room
- Messages from other players and the game server
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiStarted.PNG)

## Actions:
Actions are displayed across the top bar of the window:
- Press 'Enter' after each command
- Uppercase or lowercase letters can be used for commands
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiTopBar.PNG)

### Fight:
- Type the letter 'F' to begin a fight against the combined force of the monsters in the room. (If other players have the 'join fight' tag, their attack will join with yours to defeat the monsters)
### Start:
- Type the letter 'S' to start (this is the first command after creating your character)

### Quit:
- Type the letter 'Q' to disconnect from the game server

### Change Room:
- Type the letter 'C'
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiChangeRoom1.PNG)

- Notice below that the prompt changes and now you'll type the room number you want to go to
(The room connections and their numbers are shown to you in the 2nd vertical column from the left)
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiChangeRoom2.PNG)

### Player VS Player:
- Type the letter 'P' to fight another player in the same room as you
- You will then be prompted for a name, enter the name of the player you wish to fight

### Loot:
- Type the letter 'L' 
- You will then be prompted for a name, enter the name of the player or monster you want to steal gold from
- Note: you can only loot from players with no health

### Message:
- Type the letter 'M'
- You will then be prompted to enter the message you wish to send
- Messages are sent to all other players


# Winning the Game:

The game is won by defeating Lord Voldemort and all of the other monsters (this is most easily done by naming your character 'Harry Potter', or entering the Room of Requirement)

# Host and port definitions:

In the server the host and port are at line 872 in server.py
In the client, the host and port are at line 6 in client.py

These can be changed to run server.py on a server so users on different computers can connect
Leave them as they are to run server and client on localhost
