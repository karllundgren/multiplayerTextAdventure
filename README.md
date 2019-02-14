# multiplayerTextAdventure

#Run:
1. run server.py
2. run main.py
3. experience the adventure!

#Gameplay:
All of the information you will type will be in the text box that spans across the bottom of the window. The tag to the left of the bar will prompt for the kind of information to enter.

First you will begin by entering your player information
1. You'll enter your Name
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/gui1.PNG)

2. You'll enter your attack, defense and regeneration values (total is to be between 0 and 500 or you will get the error message shown below in the top right of the window)
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/gui2.PNG)

3. Enter the letter 'S' to enter the game
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiStart.PNG)

4. Upon starting the game notice that you're now seeing your room (the one in between lines of asteriks), the characters and monsters in your room and updated stats.
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiStarted.PNG)

Notice also what actions you are able to do- shown across the top bar of the window:
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiTopBar.PNG)

Change Room:
To go to a connection, type 'C' followed by pressing Enter
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiChangeRoom1.PNG)

Notice below that the prompt changes and now you'll type the room number you want to go to
(The room connections and their numbers are shown to you)
![alt text](https://github.com/karllundgren/multiplayerTextAdventure/blob/master/images/guiChangeRoom2.PNG)


#Winning the Game:
The game is won by defeating Lord Voldemort and all of the other monsters (this is most easily done by naming your character Harry Potter, or entering the Room of Requirement)

#Host and port definitions:
In the server the host and port are at line 872 in server.py
In the client, the host and port are at line 6 in client.py

These can be changed to run server.py on a server so users on different computers can connect
