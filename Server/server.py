import socket
from _thread import *
import threading
from player import player




dataList=[]
dataLock=threading.RLock()

playerList=[]
playerLock=threading.RLock()

connectionList=[]
connectionLock=threading.RLock()


roomList=[]
roomLock=threading.RLock()

gameDescription=''
position=0
hasLeft=[]
leftLock=threading.RLock()

monsterList=[]
monsterLock=threading.RLock()

characterLocationList=[]


def reciever(connection, position):
    global hasLeft

    while True:
        d = connection.recv(1)
        with dataLock:
            dataList[position].append(d)
        if not d:
            break
        with leftLock:
            if hasLeft[position]:
                break


def error(errorCode, errorMessage, conn):
    bA = bytearray()
    s = 7
    length = len(errorMessage)
    bA.extend(s.to_bytes(1, "little"))
    bA.extend(errorCode.to_bytes(1, "little"))
    bA.extend(length.to_bytes(2, "little"))
    bA.extend(errorMessage.encode("utf-8"))
    conn.send(bA)

def acknowledge(prot, conn):
    e = 8
    bA = bytearray()
    bA.extend(e.to_bytes(1, "little"))
    bA.extend(prot.to_bytes(1, "little"))
    conn.send(bA)

def updateData(pos, i):
    for x in range(i):
        with dataLock:
            dataList[pos].pop(0)

def sendCharacterMessage(parameterList, y):
    bA = bytearray()
    # protocol
    ten = 10

    bA.extend(ten.to_bytes(1, "little"))
    #print (parameterList[0])
    #print(parameterList[5])
    # playerName
    bA.extend((parameterList[0]).encode("utf-8"))
    # flag number
    bA.extend(parameterList[1].to_bytes(1, "little"))
    # Attack
    bA.extend(parameterList[2].to_bytes(2, "little"))
    # Defense
    bA.extend(parameterList[3].to_bytes(2, "little"))
    # Regeneration
    bA.extend(parameterList[4].to_bytes(2, "little"))
    # Health
    bA.extend(parameterList[5].to_bytes(2, "little", signed=True))
    # Gold
    bA.extend(parameterList[6].to_bytes(2, "little"))
    # Current Room #
    bA.extend(parameterList[7].to_bytes(2, "little"))
    # Description Length
    bA.extend(parameterList[8].to_bytes(2, "little"))
    # Description
    bA.extend(parameterList[9].encode("utf-8"))
    with connectionLock:
        connectionList[y].send(bA)

def sendCharacters(pos, playerCurrentRoom):
    with playerLock:
        for x in range(len(playerList)):
            if playerList[x].getCurrentRoom() == playerCurrentRoom:
                if x != position:
                    # send message 10 for player at this position
                    # pad player name
                    playerName = playerList[x].getName()
                    while len(playerName) < 32:
                        playerName += "\0"
                    parameters=[]
                    parameters.extend((playerName, playerList[x].getFlagInt(), int(playerList[x].getAttack()),
                            int(playerList[x].getDefense()),int(playerList[x].getRegen()),
                            int(playerList[x].getHealth()), int(playerList[x].getGold()),
                            int(playerList[x].getCurrentRoom()), len(playerList[x].getDescr()),playerList[x].getDescr()))
                    with leftLock:
                        if not hasLeft[pos]:
                            sendCharacterMessage(parameters, pos)
    with monsterLock:
        for x in range(len(monsterList)):
            # alive  join battle     started     ready
            if monsterList[x][1] == playerCurrentRoom:

                # send message 10 for monster at this location
                # send message 10 for player at this position
                # turn flag to int
                flag = monsterList[x][8]
                flagNumber = 0
                for i in range(len(flag)):
                    if flag[i] == '1':
                        if i == 0:
                            flagNumber += 128
                            print("alive\n")
                        elif i == 1:
                            flagNumber += 64
                            print("join battle\n")
                        elif i == 2:
                            flagNumber += 32
                            print("monster\n")
                        elif i == 3:
                            flagNumber += 16
                            print("started\n")
                        elif i == 4:
                            flagNumber += 8
                            print("ready\n")
                # pad player name
                playerName = monsterList[x][0]

                while len(playerName) < 32:
                    playerName += "\0"

                parameters = []
                parameters.extend((playerName, flagNumber,int(monsterList[x][3]),
                        int(monsterList[x][4]), int(monsterList[x][5]),
                        int(monsterList[x][2]), int(monsterList[x][6]),
                        int(monsterList[x][1]), len(monsterList[x][7]),
                        monsterList[x][7]))
                #potential hasLeft problem???
                with leftLock:
                    if not hasLeft[pos]:
                        sendCharacterMessage(parameters, pos)

def sendSelf(x):
    #x=position...

    # pad player name
    playerName = playerList[x].getName()
    while len(playerName) < 32:
        playerName += "\0"
    # attack
    length1 = len(playerList[x].getDescr())
    print ("theHealthis "+str(playerList[x].getHealth()))
    parameters=[]
    parameters.extend((playerName, playerList[x].getFlagInt(), int(playerList[x].getAttack()), int(playerList[x].getDefense()),
        int(playerList[x].getRegen()), int(playerList[x].getHealth()), int(playerList[x].getGold()),
        int(playerList[x].getCurrentRoom()),length1, playerList[x].getDescr()))
    with leftLock:
        if not hasLeft[x]:
            with connectionLock:
                sendCharacterMessage(parameters, x)

def sendGameMessage(conn, initialPoints, statLimit):
    type = 11
    descriptionLength = len(gameDescription)

    bk = bytearray()
    bk.extend(type.to_bytes(1, "little"))
    bk.extend(initialPoints.to_bytes(2, "little"))
    bk.extend(statLimit.to_bytes(2, "little"))
    bk.extend(descriptionLength.to_bytes(2, "little"))
    bk.extend(gameDescription.encode("utf-8"))
    conn.send(bk)

def massMessage(message, position):
    for x in range(len(playerList)):
        if x!=position:
            one = 1
            messageLength=len(message)

            recipientName=playerList[x].getName()
            senderName='LURK SERVER'

            while len(recipientName)<32:
                recipientName+="\0"
            while len(senderName) < 32:
                senderName += "\0"

            bA = bytearray()
            bA.extend(one.to_bytes(1, "little"))
            bA.extend(messageLength.to_bytes(2, "little"))
            bA.extend(recipientName.encode("utf-8"))
            bA.extend(senderName.encode("utf-8"))
            bA.extend(message.encode("utf-8"))
            with leftLock:
                if not hasLeft[x]:
                    connectionList[x].send(bA)

def messageFromHeaven(message, x):
    one = 1
    messageLength = len(message)

    recipientName = playerList[x].getName()
    senderName = 'LURK SERVER'

    while len(recipientName) < 32:
        recipientName += "\0"
    while len(senderName) < 32:
        senderName += "\0"

    bA = bytearray()
    bA.extend(one.to_bytes(1, "little"))
    bA.extend(messageLength.to_bytes(2, "little"))
    bA.extend(recipientName.encode("utf-8"))
    bA.extend(senderName.encode("utf-8"))
    bA.extend(message.encode("utf-8"))
    with leftLock:
        if not hasLeft[x]:
            connectionList[x].send(bA)

def massPlayer():
    for x in range(len(playerList)):
        playerName = playerList[x].getName()
        while len(playerName) < 32:
            playerName += "\0"
        parameters = []
        parameters.extend((playerName, playerList[x].getFlagInt(), int(playerList[x].getAttack()),
                           int(playerList[x].getDefense()), int(playerList[x].getRegen()),
                           int(playerList[x].getHealth()), int(playerList[x].getGold()),
                           int(playerList[x].getCurrentRoom()), len(playerList[x].getDescr()),
                           playerList[x].getDescr()))
        for y in range(len(connectionList)):
            with leftLock:
                if not hasLeft[y]:
                    sendCharacterMessage(parameters, y)



def protocolOne(recievedArray, pos, conn):
    print("entered protocol 1")
    length1 = ord(recievedArray[1])
    length2 = ord(recievedArray[2])
    length12 = (length1.to_bytes(1, "little") + length2.to_bytes(1, "little"))
    messageLength = int.from_bytes(length12, "little")
    if len(recievedArray) >= 67 + messageLength:
        recipientName = ""
        for x in range(3, 35):
            print (recipientName)
            print(recievedArray[x])
            if recievedArray[x]==b'\0' or recievedArray[x]==b'\00' or recievedArray[x]==b'\x00':
                break
            else:
                try:
                    recipientName += recievedArray[x].decode("utf-8")
                except:
                    continue
                #error(0, "only alpha numeric characters allowed", conn)
        recipientName = recipientName.replace('\0', '')
        print (recipientName)
        senderName = ""
        for x in range(35, 67):
            if recievedArray[x]==b'\0' or recievedArray[x]==b'\00' or recievedArray[x]==b'\x00':
                break
            else:

                try:
                    senderName += recievedArray[x].decode("utf-8")
                except:
                    continue
                #error(0, "only alpha numeric characters allowed", conn)
        message = ''
        for x in range(67, 67 + messageLength):
            if recievedArray[x] == b'\0' or recievedArray[x] == b'\00' or recievedArray[x] == b'\x00':
                break
            else:
                try:
                    message += recievedArray[x].decode("utf-8")
                except:
                    continue
            #error(0, "only alpha numeric characters allowed", conn)

        senderName = senderName.replace('\n', '')
        recipientName = recipientName.replace('\n', '')
        message = message.replace('\n', '')
        print ("sender" +senderName)
        print ("reciever "+recipientName)

        print(recipientName)
        foundPlayer=False
        with playerLock:
            for x in range(len(playerList)):
                # alive  join battle     started     ready
                print ("player name at location"+str(x)+playerList[x].getName())
                if playerList[x].getName() == recipientName:
                    foundPlayer=True
                    if not playerList[pos].isAlive():
                            error(5, "you're already dead yo. Move on", conn)
                    else:
                        print("found player"+recipientName+" sending message from "+senderName)
                        while len(recipientName) < 32:
                            recipientName += '\0'
                        while len(senderName) < 32:
                            senderName += '\0'
                        bA = bytearray()
                        one = 1
                        bA.extend(one.to_bytes(1, "little"))
                        bA.extend(messageLength.to_bytes(2, "little"))
                        bA.extend(recipientName.encode("utf-8"))
                        bA.extend(senderName.encode("utf-8"))
                        bA.extend(message.encode("utf-8"))
                        with leftLock:
                            if not hasLeft[x]:
                                connectionList[x].send(bA)
        if foundPlayer==False:
            print("did not find player" + recipientName + " to send message from " + senderName)
            error(6, "no player exists with that name", conn)
        updateData(pos, 67 + messageLength)


def protocolTwo(recievedArray, conn, pos):
    print("entered protocol 2")
    rm1 = ord(recievedArray[1])
    rm2 = ord(recievedArray[2])
    rm12 = (rm1.to_bytes(1, "little") + rm2.to_bytes(1, "little"))
    roomName = int.from_bytes(rm12, "little")
    updateData(pos, 3)
    if not playerList[pos].isAlive():
        error(5, "you're already dead yo. Move on", conn)
    else:
        with playerLock:
            if playerList[pos].getFlags()[1] == '0':
                error(5, "action performed too early",conn)
            elif playerList[pos].getCurrentRoom() == roomName:
                desc = "already in room " + str(roomName)
                error(1,desc,conn)
            elif roomName not in roomList[playerList[pos].getCurrentRoom() - 1][3]:
                desc = "no connection to room " + str(roomName)
                error(1, desc, conn)

            else:
                # acceptance of room change
                #set room of requirement crap
                if roomName==7:
                    playerList[pos].setROQ()
                    if playerList[pos].getROQ()>=3:
                        messageFromHeaven("CONGRATULATIONS! You may now enter the 'room of requirement",pos)
                        roomList[6][3].append(8)
                        print(roomList[6][3])
                if roomName == 8:
                    playerList[pos].setAttack(65535)
                    playerList[pos].setDefense(65535)
                    playerList[pos].setRegen(65535)
                    playerList[pos].setHealth(1000)
                    parameterList=[]
                    print (playerList[pos].getName())
                    pname=playerList[pos].getName()
                    while len(pname)<32:
                        pname+="\0"
                    parameterList.append(pname)
                    parameterList.append(playerList[pos].getFlagInt())
                    parameterList.append(playerList[pos].getAttack())
                    parameterList.append(playerList[pos].getDefense())
                    parameterList.append(playerList[pos].getRegen())
                    parameterList.append(playerList[pos].getHealth())
                    parameterList.append(playerList[pos].getGold())
                    parameterList.append(playerList[pos].getCurrentRoom())
                    parameterList.append(len(playerList[pos].getDescr()))
                    parameterList.append(playerList[pos].getDescr())
                    with leftLock:
                        if not hasLeft[pos]:
                            sendCharacterMessage(parameterList, pos)

                playerList[pos].setCurrentRoom(roomName)
                playerCurrentRoom = playerList[pos].getCurrentRoom()
                # send players and characters that are in that room
                sendCharacters(pos, playerCurrentRoom)
                nine = 9
                with dataLock:
                    dataList[pos].insert(0, nine.to_bytes(1, "little"))



def protocolThree(conn, pos):
    #acknowledge(3, conn)
    print("entered protocol 3")
    playerAttack = []
    monsterAttack = []

    with playerLock:
        attackRoomName = playerList[pos].getCurrentRoom()
        playerAttack.append(pos)
        for x in range(len(playerList)):

            # alive  join battle     started     ready
            if playerList[x].getCurrentRoom() == attackRoomName:
                print (playerList[x].getFlags())
                if playerList[x].getName() != playerList[pos].getName() and playerList[x].getFlags()[0] == '1' and \
                                playerList[x].getFlags()[1] == '1' and playerList[x].getFlags()[3] == '1' and playerList[x].getFlags()[4] == '1':
                    print("added to player Attack")
                    playerAttack.append(x)
    with monsterLock:
        for x in range(len(monsterList)):
            # alive  join battle     started     ready
            if int(monsterList[x][1]) == attackRoomName:
                # if monsterList[x][8][0]==1 and monsterList[x][8][1]==1 and monsterList[x][8][3]==1 and monsterList[x][8][4]==1:
                monsterAttack.append(x)
    if not playerList[pos].isAlive():
        error(5, "you're already dead yo. Move on", conn)
    elif len(monsterAttack) == 0:
        desc = "no characters in your room to attack"
        error(6, desc, conn)
    else:
        totalAttack = 0
        # attacking monsters
        print ("player attack is: "+str(len(playerAttack)))
        for i in playerAttack:
            with playerLock:
                totalAttack += playerList[i].getAttack()
        for y in monsterAttack:
            with monsterLock:
                # hit=attack-defense- monsterList[y][4]
                hit = totalAttack
                if hit>50000:
                    hit=50000
                # if health > hit
                if hit > 0:
                    monsterList[y][2] -= hit
                    if monsterList[y][2]<-20000:
                        monsterList[y][2]=-20000
                    #health is not negative
                    if monsterList[y][2] > 0:

                        # regen if will not exceed max health
                        if monsterList[y][2] + int(.25 * monsterList[y][5]) <= monsterList[y][9]:
                            monsterList[y][2] += int(.25 * monsterList[y][5])
                    else:
                        monsterList[y][8]='00100'
                        print("monster is dead")
        # attacking players
        totalAttack = 0
        for i in monsterAttack:
            with monsterLock:
                totalAttack += monsterList[i][3]
        for y in playerAttack:
            with playerLock:
                # hit=attack-defense
                hit = totalAttack - playerList[y].getDefense()
                if hit>50000:
                    hit=50000
                # if health > hit
                if hit > 0:
                    playerList[y].setHealth(playerList[y].getHealth() - hit)
                    if playerList[y].getHealth()<-20000:
                        playerList[y].setHealth(-20000)
                    # regen
                    #sendSelf(pos)
                    if playerList[y].getHealth()>0:
                        playerList[y].setHealth(int(.25 * playerList[y].getRegen()))
                    elif playerList[y].getHealth()<=0:
                        playerList[y].died()
                        print("player is dead")

        for p in playerAttack:
            with leftLock:
                if not hasLeft[p]:
                    sendSelf(p)
                    with playerLock:
                        sendCharacters(p, playerList[p].getCurrentRoom())

    updateData(pos, 1)
    winCheck()

def winCheck():
    with monsterLock:
        for monster in monsterList:
            if monster[8][0]=='0':
                continue
            else:
                return
    #players have won the game
    massMessage("CONGRATULATIONS. HOGWARTS HAS BEEN SUCCESSFULLY DEFENDED. YOU WIN.", -1)

def protocolFour( conn, pos):
    #pvp disabled
    print("entered protocol 4")
    updateData(pos, 33)
    # send accept
    if not playerList[position].isAlive():
        error(5, "you're already dead yo. Move on", conn)
    else:
        error(8,"PvP is not enabled on this server", conn)

def protocolFive(recievedArray, conn, pos):
    print("entered protocol 5")
    name = ""
    for x in range(1, 33):
        if recievedArray[x] == b'\0' or recievedArray[x] == b'\00' or recievedArray[x] == b'\x00':
            break
        else:
            try:
                name += recievedArray[x].decode("utf-8")
            except:
                continue
            #error(0, "only alpha numeric characters allowed", conn)
    name = name.replace('\0', '')
    name = name.replace('\n', '')
    isPlayer = False
    isMonster = False
    if not playerList[pos].isAlive():
        error(5, "you're already dead yo. Move on", conn)
    else:
        with playerLock:
            currentRoom = playerList[pos].getCurrentRoom()
            for x in range(len(playerList)):
                if name == playerList[x].getName():
                    isPlayer = True
                    if currentRoom == playerList[x].getCurrentRoom():
                        flags = playerList[x].getFlags()
                        # if dead
                        if flags[0] == '0':
                            # loot them
                            playerList[pos].setGold(playerList[x].getGold())
                            playerList[x].setGold(0)
                    else:
                        desc = "attempting to loot player outside of room " + str(currentRoom)
                        error(3, desc, conn)
        if not isPlayer:
            with monsterLock:
                for x in range(len(monsterList)):
                    monsterName = monsterList[x][0]
                    monsterName = monsterName.replace('\0', '')
                    monsterName = monsterName.replace('\n', '')
                    if name.upper() == monsterName.upper():
                        isMonster=True
                        print(name)
                        print(len(name))
                        print(monsterName)
                        print(len(monsterName))
                        if currentRoom == monsterList[x][1]:
                            print("matched name and room")
                            flags = monsterList[x][8]
                            # if dead
                            if flags[4] == '0':
                                print("deadddddd")
                                # loot them
                                playerList[pos].setGold(monsterList[x][6])
                                monsterList[x][6] = 0
                        else:
                            desc = "attempting to loot monster outside of room " + str(currentRoom)
                            error(3, desc, conn)
        if not isPlayer and not isMonster:
            desc = "attempting to loot nonexistent character"
            error(3, desc, conn)
    updateData(pos, 33)
    if isPlayer or isMonster:
        sendSelf(pos)
        sendCharacters(pos, playerList[pos].getCurrentRoom())

def protocolSix(conn, pos):
    print("entered protocol 6")
    acknowledge(6, conn)
    updateData(pos, 1)
    nine = 9
    playerList[pos].setFlags("11011")
    with dataLock:
        dataList[pos].insert(0, nine.to_bytes(1, "little"))
    sendCharacters(pos, playerList[pos].getCurrentRoom())

    #send new character message to all players
    #massMessage("Player: "+playerList[pos].getName()+" has joined the game.", pos)
    massPlayer()


def protocolNine(conn, pos):
    print("entered protocol 9")
    bA = bytearray()
    num = 9
    with playerLock:
        currentRoom = playerList[pos].getCurrentRoom()

    rmNumber = currentRoom - 1
    # protocol
    bA.extend(num.to_bytes(1, "little"))
    # room number
    bA.extend(roomList[rmNumber][0].to_bytes(2, "little"))
    # room name
    bA.extend(roomList[rmNumber][1].encode("utf-8"))
    # room description length
    descLength = len(roomList[rmNumber][2])
    bA.extend(descLength.to_bytes(2, "little"))
    # room description
    bA.extend(roomList[rmNumber][2].encode("utf-8"))

    conn.send(bA)

    updateData(pos, 1)
    thirteen = 13
    with dataLock:
       dataList[pos].insert(0, thirteen.to_bytes(1, "little"))

def protocolTen(recievedArray, conn, pos, initialPoints):
    print("entered protocol 10")
    # get player name
    playerName = ""
    for x in range(1, 33):
        if recievedArray[x] == b'\0' or recievedArray[x] == b'\00' or recievedArray[x] == b'\x00':
            break
        else:
            try:
                playerName += recievedArray[x].decode("utf-8")
            except:
                continue
            #error(0, "only alpha numeric characters allowed", conn)

    # get flags
    Flag = (recievedArray[33])
    byte_binary = bin(ord(Flag))
    byte_binary = byte_binary[2:]
    binaryList = []
    for x in range(len(byte_binary) - 1, -1, -1):
        binaryList.append(byte_binary[x])
    littleBinary = ''
    for x in binaryList:
        littleBinary += x
    while len(littleBinary) < 8:
        littleBinary += '0'
    status = ""
    if littleBinary[4] == '1':
        status += "Ready/"
    if littleBinary[3] == '1':
        status += "Started/"
    if littleBinary[2] == '1':
        status += "Monster/"
    if littleBinary[1] == '1':
        status += "Join Battle/"
    if littleBinary[0] == '1':
        status += "Alive/"
    # get attack
    att1 = ord(recievedArray[34])
    att2 = ord(recievedArray[35])
    att12 = (att1.to_bytes(1, "little") + att2.to_bytes(1, "little"))
    attack = int.from_bytes(att12, "little")
    # get defense
    def1 = ord(recievedArray[36])
    def2 = ord(recievedArray[37])
    def12 = (def1.to_bytes(1, "little") + def2.to_bytes(1, "little"))
    defense = int.from_bytes(def12, "little")
    # get Regen
    reg1 = ord(recievedArray[38])
    reg2 = ord(recievedArray[39])
    reg12 = (reg1.to_bytes(1, "little") + reg2.to_bytes(1, "little"))
    regeneration = int.from_bytes(reg12, "little")
    # get health
    hea1 = ord(recievedArray[40])
    hea2 = ord(recievedArray[41])
    hea12 = (hea1.to_bytes(1, "little") + hea2.to_bytes(1, "little"))
    health = int.from_bytes(hea12, "little", signed=True)
    # get Gold
    gold1 = ord(recievedArray[42])
    gold2 = ord(recievedArray[43])
    gold12 = (gold1.to_bytes(1, "little") + gold2.to_bytes(1, "little"))
    gold = int.from_bytes(gold12, "little")
    # get current room number
    roomNm1 = ord(recievedArray[44])
    roomNm2 = ord(recievedArray[45])
    roomNm12 = (roomNm1.to_bytes(1, "little") + roomNm2.to_bytes(1, "little"))
    roomNum = int.from_bytes(roomNm12, "little")
    # what to do with roomNum?????

    # get description length
    description1 = int.from_bytes(recievedArray[46], 'little')
    description2 = int.from_bytes(recievedArray[47], 'little')
    description12 = (description1.to_bytes(1, "little") + description2.to_bytes(1, "little"))
    descriptionLength = int.from_bytes(description12, "little")

    # get Player description
    playerDescription = ""
    if len(recievedArray) >= 48 + descriptionLength:
        for x in range(48, descriptionLength + 48):
            if recievedArray[x]==b'\0' or recievedArray[x]==b'\00' or recievedArray[x]==b'\x00':
                break
            else:
                try:
                    playerDescription += recievedArray[x].decode("utf-8")
                except:
                    continue
                #error(0, "only alpha numeric characters allowed", conn)

        # strip playerName of its padding zeros
        playerName = playerName.replace("\0", "")
        used = False
        reprise = False
        potter=False
        for nam in range(len(playerList)):
            if playerName == playerList[nam].getName():
                if playerList[nam].getFlags()[0] == '1':
                    used = True

                else:
                    # reprise dead character
                    # move this character to that characters position
                    playerList[pos] = playerList[nam]
                    reprise = True

        # character data validation
        if attack + defense + regeneration <= initialPoints:
            if used == False:
                if reprise == False:
                    playerList[pos].setAttack(attack)
                    playerList[pos].setDefense(defense)
                    playerList[pos].setRegen(regeneration)
                    playerList[pos].setGold(0)
                    playerList[pos].setHealth(100)
                    playerList[pos].setStatus(status)
                    playerList[pos].setName(playerName)
                    playerList[pos].setFlags(littleBinary)
                    playerList[pos].setDescr(playerDescription)
                elif reprise == True:
                    # Send ACCEPTANCE
                    playerList[pos].setHealth(100)
                    playerList[pos].setFlags(littleBinary)
                #print("sending 10 back for "+playerName)
                if playerName.upper()=="HARRY POTTER":
                    playerList[pos].setAttack(65535)
                    playerList[pos].setDefense(65535)
                    playerList[pos].setRegen(65535)
                    potter=True
                while len(playerName) < 32:
                    playerName += "\0"
                parameters = []
                parameters.extend((playerName, playerList[pos].getFlagInt(), attack,defense,regeneration,100,
                                   0,0, len(playerDescription), playerDescription))

                acknowledge(10, conn)
                sendCharacterMessage(parameters,pos)
                if reprise==True and potter==False:
                    massMessage("player, '" + playerList[pos].getName() + "' has been reprised to defend Hogwarts.",pos)
                elif reprise==True and potter==True:
                    massMessage(playerList[pos].getName().upper() + "' has returned from the dead to save us from voldemort.",pos)
                    messageFromHeaven("CONGRATULATIONS! you're harry potter. Your stats have been set to maximum. It's up to you to save the day.",pos)
                elif reprise==False and potter==False:
                    massMessage("New player, '" + playerList[pos].getName() + "' has arrived to defend Hogwarts.",pos)
                elif reprise == False and potter == True:
                    massMessage( playerList[pos].getName() + "' has finally arrived to save us from voldemort.",pos)
                    messageFromHeaven("CONGRATULATIONS! you're harry potter. Your stats have been set to maximum. It's up to you to save the day.",pos)

            elif used == True:
                desc = "player name: " + str(playerName) + " already in use"
                error(1, desc, conn)
        else:
            desc = "Stats too high, need to be <= " + str(initialPoints)
            error(4, desc, conn)
        updateData(pos, 48 + descriptionLength)

def protocolThirteen(conn, pos):
    print("entered protocol 13")
    with playerLock:
        roomNumber = playerList[pos].getCurrentRoom() - 1
    for roomConnection in roomList[roomNumber][3]:
        roomConNumber = roomConnection - 1
        bA = bytearray()
        num = 13
        # protocol
        bA.extend(num.to_bytes(1, "little"))
        # room number
        bA.extend(roomList[roomConNumber][0].to_bytes(2, "little"))
        # room name
        bA.extend(roomList[roomConNumber][1].encode("utf-8"))
        # room description length
        descLength = len(roomList[roomConNumber][2])
        bA.extend(descLength.to_bytes(2, "little"))
        # room description
        bA.extend(roomList[roomConNumber][2].encode("utf-8"))

        conn.send(bA)
    updateData(pos, 1)



def processer(conn, position):
    # send game message

    initialPoints = 500
    statLimit = 65535
    sendGameMessage(conn, initialPoints, statLimit)
    global hasLeft
    while True:
        if len(dataList)>0:
            with dataLock:
                recievedArray = dataList[position]

            if len(recievedArray) > 0:

                protocol = int.from_bytes(recievedArray[0], 'little')
                if protocol == 1:
                    if len(recievedArray) >= 67:
                        protocolOne(recievedArray, position, conn)


                elif protocol == 2:
                    if len(recievedArray) > 2:
                        protocolTwo(recievedArray, conn, position)

                elif protocol==3:
                    protocolThree( conn, position)

                elif protocol==4:
                    #PvP Fight is disabled
                    if len(recievedArray)>32:
                        protocolFour( conn, position)

                elif protocol==5:
                    if len(recievedArray)>=33:
                        protocolFive(recievedArray, conn, position)

                elif protocol == 6:
                    #send accept
                    protocolSix(conn, position)

                elif protocol == 9:

                    protocolNine(conn, position)

                elif protocol == 10:
                    # initialize player
                    if len(recievedArray) > 48:
                        protocolTen(recievedArray, conn, position, initialPoints)

                elif protocol==12:
                    print("entered protocol 12")
                    with playerLock:
                        if playerList[position].isAlive():
                            playerList[position].setFlags('10000')
                        else:
                            playerList[position].setFlags('00000')
                    with leftLock:
                        hasLeft[position]=True
                    updateData(position, 1)

                elif protocol == 13:
                    protocolThirteen(conn, position)
                elif str(protocol).isnumeric() == False:
                    print("the protocol is not a number...")
        with leftLock:
            if hasLeft[position]:
                break




def main():

    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1',5022))
    sock.listen(1)
    global connectionList
    global objectList

    #read in rooms from file
    global roomList
    fh=open('rooms.txt','r')
    list=fh.readlines()
    i=0
    while i<len(list)/4:
        room = []
        # room number
        room.append(int(list[i * 4]))

        # adding padding to the room name
        while len(list[1 + i * 4]) < 32:
            list[1 + i * 4] += '\0'
        # 1room name
       #list[1 + i * 4]=list[1 + i * 4].replace('\n','')
        room.append(list[1 + i * 4])
        # 2description
        room.append(list[2 + i * 4])
        cons = []
        # 3connections
        for x in list[3 + i * 4].split():
            if int(x)!=8:
                cons.append(int(x))
        room.append(cons)
        roomList.append(room)
        i += 1
    fh.close()
    #read in monsters from file
    global monsterList
    fh = open('monsters.txt', 'r')
    list = fh.readlines()
    i = 0
    while i < len(list) / 10:
        monster = []
        #remove endline in name
        list[i * 10]=list[i * 10].replace('\n','')
        # adding padding to the monster name
        while len(list[i * 10]) < 32:
            list[i * 10] += '\0'
        monster.append(list[ i * 10])
        #room number
        monster.append(int(list[1 + i * 10]))
        #health
        monster.append(int(list[2 + i * 10]))
        #attack
        monster.append(int(list[3 + i * 10]))
        #defense
        monster.append(int(list[4 + i * 10]))
        #regeneration
        monster.append(int(list[5 + i * 10]))
        #gold
        monster.append(int(list[6 + i * 10]))
        #description
        des=list[7 + i * 10].replace('\n','')
        monster.append(des)
        #flags
        monster.append(list[8 + i * 10])
        #maxHealth
        monster.append(int(list[9 + i * 10]))
        monsterList.append(monster)
        i += 1
    fh.close()

    #create character list by room
    global characterLocationList
    for x in range(14):
        characterLocationList.append([x+1])

    #read in game description from file
    fh = open('gameDescription.txt', 'r')
    global gameDescription
    gameDescription = fh.readline()

    fh.close()
    global position
    while True:
        conn, addr=sock.accept()
        with connectionLock:
            connectionList.append(conn)
        newPlayer=player()
        with playerLock:
            playerList.append(newPlayer)
        start_new_thread(reciever, (conn, position))
        #pThread = threading.Thread(target=reciever, args=(conn,position,))
        #pThread.daemon = True
        #pThread.start()
        with dataLock:
            dataList.append([])
        with leftLock:
            hasLeft.append(False)
        pThread = threading.Thread(target=processer, args=(conn, position,))
        pThread.daemon = True
        pThread.start()


        position+=1


main()


if __name__=="__main__":
    main()
