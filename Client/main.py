from tkinter import *
import threading
from gui import interface
from client import Client
from player import player




def switch(client, i, myP):
    while True:
        process(client, i, myP)
        prepareSend(client, i, myP)


def process(client, i, myP):

        recievedArray=client.getData()
        recArraySize=len(recievedArray)


        if recArraySize>0:
            #print ("entered\n")
            #print("\nthe length is: " + str(len(str(recievedSize))) + str(client.getData()[0]))
            protocol=int.from_bytes(recievedArray[0],'little')

            #print ("The Protocol recieved was: "+str(protocol))
            if protocol==0:
                exit()
            elif protocol==1:
                #print ("Message")
                if len(recievedArray) > 67:
                    #print (len(recievedArray))
                    #get message length
                    messlen1 = ord(recievedArray[1])
                    messlen2 = ord(recievedArray[2])
                    messlen12 = (messlen1.to_bytes(1, "little") + messlen2.to_bytes(1, "little"))
                    messageLenth = int.from_bytes(messlen12, "little")

                    #get recipient name
                    recipient = ""
                    for x in range(3,34):
                        recipient += recievedArray[x].decode("utf-8")
                        recipient = recipient.replace("0", "")
                        #get sender name
                    sender = ""
                    for x in range(35, 66):
                        sender += recievedArray[x].decode("utf-8")
                    sender = sender.replace("0", "")
                    #get message
                    message = ""
                    if len(recievedArray)>=messageLenth+67:
                        for x in range(67, messageLenth+67):
                            message += recievedArray[x].decode("utf-8")
                        message = message.replace("0", "")
                        #combine recipient, sender, message
                        toPost="Sender: "+sender\
                                +"\nReciever: "+recipient\
                                +"\nMessage: "+message
                        #post message to GUI
                        i.postPlayerMessages(toPost)
                        client.updateData(67+messageLenth)

            elif protocol==7:
                if len(recievedArray) > 4:
                    #getting error code
                    errorCode=int.from_bytes(recievedArray[1],'little')
                    #getting message length
                    emesslen1 = ord(recievedArray[2])
                    emesslen2 = ord(recievedArray[3])
                    emesslen12 = (emesslen1.to_bytes(1, "little") + emesslen2.to_bytes(1, "little"))
                    emessageLenth = int.from_bytes(emesslen12, "little")
                    #getting message
                    errorMessage = ""
                    if len(recievedArray)>=emessageLenth+4:
                        for x in range(4,emessageLenth+4):
                            errorMessage += recievedArray[x].decode("utf-8")
                        if errorCode==0:
                            pass
                        elif errorCode==1:
                            pass
                        elif errorCode ==2:
                            pass
                        elif errorCode ==3:
                            pass
                        elif errorCode ==4:
                            pass
                        elif errorCode ==5:
                            pass
                        elif errorCode ==6:
                            pass
                        elif errorCode ==7:
                            pass
                        i.postPlayerMessages(errorMessage)
                        client.updateData(4+emessageLenth)

            elif protocol==8:
                #print (len(recievedArray))
                if len(recievedArray)>1:
                    acknowledgement="ACKNOWLEDGED: "\
                                    +str(int.from_bytes(recievedArray[1],'little'))
                    i.postPlayerMessages(acknowledgement)
                    client.updateData(2)

            elif protocol==9:
                #print ("Room")
                if len(recievedArray)>37:
                    #getting room number. USED FOR CHANGEROOM
                    room1 = ord(recievedArray[1])
                    room2 = ord(recievedArray[2])
                    room12 = (room1.to_bytes(1, "little") + room2.to_bytes(1, "little"))
                    roomNumber = int.from_bytes(room12, "little")
                    #get room name
                    roomName=""
                    for x in range(3,34):
                        roomName+=recievedArray[x].decode('utf-8')

                    #get description length
                    rd1 = ord(recievedArray[35])
                    rd2 = ord(recievedArray[36])
                    rd12 = (rd1.to_bytes(1, "little") + rd2.to_bytes(1, "little"))
                    roomDescriptionLength= int.from_bytes(rd12, "little")
                    #get description
                    description=""
                    if len(recievedArray) >=roomDescriptionLength+37:
                        for x in range(37, roomDescriptionLength+37):
                            description+=recievedArray[x].decode('utf-8')
                        #post description
                        mess="******************************"\
                            +"\nRoom Number: "+str(roomNumber)\
                        +"\nRoom Name: "+roomName\
                        +"\nRoom Description: "+description\
                        +"\n******************************"
                        i.postRoomMessages(mess)
                        client.updateData(37+roomDescriptionLength)

            elif protocol==10:
                #print(len(recievedArray))
                if len(recievedArray)>48:
                    # get player name
                    playerName = ""
                    for x in range(1,32):
                        playerName += recievedArray[x].decode("utf-8")
                    #get flags
                    Flag=(recievedArray[33])

                    byte_binary = bin(ord(Flag))
                    #print (byte_binary)
                    byte_binary=byte_binary[2:]
                    #print (byte_binary)
                    binaryList=[]
                    for x in range(len(byte_binary)-1, -1,-1):
                        binaryList.append(byte_binary[x])
                    littleBinary=''
                    for x in binaryList:
                        littleBinary+=x
                    #print (littleBinary)
                    if len(littleBinary)<8:
                        littleBinary+='000'
                    status=""
                    if littleBinary[3]=='1':
                        status+="Ready/"
                    if littleBinary[4]=='1':
                        status+="Started/"
                    if littleBinary[5]=='1':
                        status+="Monster/"
                    if littleBinary[6]=='1':
                        status+="Join Battle/"
                    if littleBinary[7]=='1':
                        status+="Alive/"
                    #print (status)

                    #get attack
                    att1 = ord(recievedArray[34])
                    att2 = ord(recievedArray[35])
                    att12 = (att1.to_bytes(1, "little") + att2.to_bytes(1, "little"))
                    attack= int.from_bytes(att12, "little")
                    #get defense
                    def1 = ord(recievedArray[36])
                    def2 = ord(recievedArray[37])
                    def12 = (def1.to_bytes(1, "little") + def2.to_bytes(1, "little"))
                    defense = int.from_bytes(def12, "little")
                    #get Regen
                    reg1 = ord(recievedArray[38])
                    reg2 = ord(recievedArray[39])
                    reg12 = (reg1.to_bytes(1, "little") + reg2.to_bytes(1, "little"))
                    regeneration = int.from_bytes(reg12, "little")
                    #get health
                    hea1 = ord(recievedArray[40])
                    hea2 = ord(recievedArray[41])
                    hea12 = (hea1.to_bytes(1, "little") + hea2.to_bytes(1, "little"))
                    health = int.from_bytes(hea12, "little", signed=True)
                    #get Gold
                    gold1 = ord(recievedArray[42])
                    gold2 = ord(recievedArray[43])
                    gold12 = (gold1.to_bytes(1, "little") + gold2.to_bytes(1, "little"))
                    gold = int.from_bytes(gold12, "little")
                    #get current room number
                    roomNm1 = ord(recievedArray[44])
                    roomNm2 = ord(recievedArray[45])
                    roomNm12 = (roomNm1.to_bytes(1, "little") + roomNm2.to_bytes(1, "little"))
                    roomNum = int.from_bytes(roomNm12, "little")
                    #what to do with roomNum?????

                    #get description length
                    description1 = int.from_bytes(recievedArray[46], 'little')
                    description2 = int.from_bytes(recievedArray[47], 'little')
                    description12 = (description1.to_bytes(1, "little") + description2.to_bytes(1, "little"))
                    descriptionLength = int.from_bytes(description12, "little")
                    #get Player description
                    playerDescription=""
                    #print("Recieved Array size: " + str(len(recievedArray)) + "\n\n")
                    if len(recievedArray)>=48+descriptionLength:
                        print ("times ran")
                        for x in range(48,descriptionLength+48):
                            print (x)
                            #print (recievedArray[x].decode("utf-8"))
                            playerDescription += recievedArray[x].decode("utf-8")
                        #strip playerName of its padding zeros
                        playerName = playerName.replace("\0", "")

                        #check to see if I am this player
                        if playerName==myP.getName():
                            myP.setAttack(attack)
                            myP.setDefense(defense)
                            myP.setRegen(regeneration)
                            myP.setGold(gold)
                            myP.setHealth(health)
                            myP.setStatus(status)
                            i.postStats(myP.statsToGui())
                            client.updateData(48 + descriptionLength)
                        else:
                            statList=[]
                            statList.append("Name: " + playerName)
                            statList.append("Description: " + playerDescription)
                            statList.append("Gold: " + str(gold))
                            statList.append("Attack: " + str(attack))
                            statList.append("Defense: " + str(defense))
                            statList.append("Regen: " + str(regeneration))
                            statList.append("Status: " + status)
                            #statList.append("Location: " + self.Location)
                            statList.append("Health: " + str(health))
                            #statList.append("Started: " + self.Started)

                            i.postPeople(statList)
                            client.updateData(48 + descriptionLength)

            elif protocol==11:
                if len(recievedArray)>7:
                    #getting initialPoints
                    init1 = ord(recievedArray[1])
                    init2 = ord(recievedArray[2])
                    init12 = (init1.to_bytes(1, "little") + init2.to_bytes(1, "little"))
                    initialPoints=int.from_bytes(init12, "little")
                    myP.setInitialPoints(initialPoints)

                   #getting stat Limit
                    stat1 = ord(recievedArray[3])
                    stat2 = ord(recievedArray[4])
                    stat12 = (stat1.to_bytes(1, "little") + stat2.to_bytes(1, "little"))
                    statLimit=int.from_bytes(stat12, "little")
                    if statLimit>0:
                        myP.setStatLim(statLimit)

                    #getting description length
                    desc1=ord(recievedArray[5])
                    desc2=ord(recievedArray[6])
                    desc12=(desc1.to_bytes(1, "little")+desc2.to_bytes(1,"little"))
                    descriptionLen=int.from_bytes(desc12, "little")
                    #print (descriptionLen)
                    #getting description
                    description=""
                    if len(recievedArray) >=descriptionLen+7:
                        for x in range(7,descriptionLen+7):
                            #print (x)
                            description+=recievedArray[x].decode("utf-8")
                        #print ("\n\n\n")
                        i.postPlayerMessages("Description: "+description)
                        client.updateData(descriptionLen+7)
                        #print (len(recievedArray))

            elif protocol==13:
                if len(recievedArray)>37:
                    #get room number
                    roo1 = ord(recievedArray[1])
                    roo2 = ord(recievedArray[2])
                    roo12 = (roo1.to_bytes(1, "little") + roo2.to_bytes(1, "little"))
                    room_number = int.from_bytes(roo12, "little")
                    #get room name
                    room_name=""
                    for x in range(3, 34):
                        room_name+=recievedArray[x].decode('utf-8')

                    #get room description length
                    leng1 = ord(recievedArray[35])
                    leng2 = ord(recievedArray[36])
                    leng12 = (leng1.to_bytes(1, "little") + leng2.to_bytes(1, "little"))
                    description_length = int.from_bytes(leng12, "little")
                    #get room description
                    room_desc=""
                    if len(recievedArray)>=description_length+37:
                        for x in range(37,description_length+37):
                            room_desc+=recievedArray[x].decode('utf-8')
                        roomMessage="CONNECTION"+\
                                    "\nName: "+room_name\
                                    +"\nNumber: "+str(room_number)\
                                    +"\nDescription: "+room_desc+"\n"
                        i.postRoomMessages(roomMessage)
                        client.updateData(37+description_length)


def prepareSend(client, i, myP):
    #to send character at first
    if myP.getAttack()==0 and myP.getDefense()==0 and myP.getRegen()==0:
        setCharacter(client, i, myP)

    sendList = i.getSend()
    listLength = len(sendList)
    if listLength>0:
        type = sendList[0].upper()
        type=type.strip()

        if type=='P':
            i.setSend(1)
            setCharacter(client, i, myP)
        # FIGHT
        elif type=='F':
            protocol=3
            myByte=bytearray()
            myByte.extend(protocol.to_bytes(1, 'little'))
            client.sendMsg(myByte)
            i.setSend(1)
            #i.setPromptLabel("Enter Command:")

            #START
        elif type == 'S':
            protocol = 6
            myByte = bytearray()
            myByte.extend(protocol.to_bytes(1, 'little'))
            client.sendMsg(myByte)
            i.setSend(1)
            i.postStats(myP.statsToGui())

            #QUIT
        elif type == 'Q':
            #print("we got here: " + type)
            protocol = 12
            myByte = bytearray()
            myByte.extend(protocol.to_bytes(1, 'little'))
            client.sendMsg(myByte)
            i.setSend(1)
            #interrupt_main()
            i.quit()


        # CHANGEROOM
        elif type == 'C':
            i.setPromptLabel("Enter Room Number:")
            if listLength >=2:
                protocol = 2
                zero = 0
                roomNumber=int(sendList[1].strip())
                #print (roomNumber)
                myByte=bytearray()
                myByte.extend(protocol.to_bytes(1, "little"))
                myByte.extend(roomNumber.to_bytes(1, "little"))
                myByte.extend(zero.to_bytes(1, "little"))
                client.sendMsg(myByte)
                i.setSend(2)
                i.setPromptLabel("Enter Command:")


        # PLAYER VS PLAYER
        elif type == 'V':
            i.setPromptLabel("Name of Player to target:")
            if listLength >= 2:
                protocol = 4
                playerName=sendList[1].strip()
                while len(playerName)<32:
                    playerName+='\0'
                myByte=bytearray()
                myByte.extend(protocol.to_bytes(1, "little"))
                myByte.extend(playerName.encode('utf-8'))
                client.sendMsg(myByte)
                i.setSend(2)
                i.setPromptLabel("Enter Command:")
        # LOOT
        elif type == 'L':
            i.setPromptLabel("Name of Player to loot:")
            if listLength >= 2:
                protocol = 5
                playerName = sendList[1].strip()
                while len(playerName) < 32:
                    playerName += '\0'
                myByte = bytearray()
                myByte.extend(protocol.to_bytes(1, "little"))
                myByte.extend(playerName.encode('utf-8'))
                client.sendMsg(myByte)
                i.setSend(33)
                i.setPromptLabel("Enter Command:")


        #MESSAGE
        elif type=='M':
            if listLength==1:
                i.setPromptLabel("Recipient Name:")
            if listLength ==2:
                i.setPromptLabel("Type Message:")
            if listLength>2:
                #protocol
                protocol = 1
                zero=0
                #pad recipient name
                recipient=sendList[1].strip()
                while len(recipient)<32:
                    recipient+='\0'

                # pad my(sender) name
                myName=myP.getName().strip()
                while len(myName)<32:
                   myName+='\0'

                #get message
                message=sendList[2]
                #get message length
                messageLength=len(message)
                #to byteArray
                myByte = bytearray()
                myByte.extend(protocol.to_bytes(1, "little"))
                myByte.extend(messageLength.to_bytes(1,"little"))
                myByte.extend(zero.to_bytes(1, "little"))
                myByte.extend(recipient.encode('utf-8'))
                myByte.extend(myName.encode('utf-8'))
                myByte.extend(message.encode('utf-8'))
                client.sendMsg(myByte)
                i.setSend(3)
                i.setPromptLabel("Enter Command:")
        #to allow program to continue running if user enters a wierd value first
        #must work with setCharacter though, and it does'nt so its commented out
        #else:
            #i.setSend(1)



def setCharacter(client, i, myP):
    sendList = i.getSend()
    if len(sendList) == 0:
        i.setPromptLabel("Enter your Player Name:")
    if len(sendList) == 1:
        i.setPromptLabel("Enter your Attack:")
    if len(sendList) == 2:
        i.setPromptLabel("Enter your Defense:")
    if len(sendList) == 3:
        i.setPromptLabel("Enter your Regen:")
    if len(sendList) == 4:
        i.setPromptLabel("Enter a description of yourself:")
    if len(sendList) >= 5:
        if int(sendList[1]) + int(sendList[2]) + int(sendList[3]) <= myP.getInitialPoints():


            # set dat types in player class
            myP.setName(sendList[0])
            myP.setAttack(sendList[1])
            myP.setDefense(sendList[2])
            myP.setRegen(sendList[3])
            myP.setDescr(sendList[4])
            myP.setStatus("Ready")
            i.postStats(myP.statsToGui())

            zero = 0
            # preparing data to send
            playerName = sendList[0]
            while len(playerName) < 32:
                playerName += "\0"
            # attack
            a1 = int(sendList[1])
            a2 = 0
            if a1 > 255:
                a2 = a1 - 255
                a1 = 255
            # defense
            d1 = int(sendList[2])
            d2 = 0
            if d1 > 255:
                d2 = d1 - 255
                d1 = 255
            # regeneration
            r1 = int(sendList[3])
            r2 = 0
            if r1 > 255:
                r2 = r1 - 255
                r1 = 255
            # description length
            length1 = len(sendList[4])
            length2 = 0
            if length1 > 255:
                length2 = length1 - 255
                length1 = 255
            prot = 10
            #ready, started, alive
            flag = 19
            #ready, started, join battle, alive
            #flag=72
            bA = bytearray()
            # protocol
            bA.extend(prot.to_bytes(1, "little"))
            # playerName
            bA.extend(playerName.encode('utf-8'))
            # flag number
            bA.extend(flag.to_bytes(1, "little"))
            # Attack
            bA.extend(a1.to_bytes(1, "little"))
            bA.extend(a2.to_bytes(1, "little"))
            # Defense
            bA.extend(d1.to_bytes(1, "little"))
            bA.extend(d2.to_bytes(1, "little"))
            # Regeneration
            bA.extend(r1.to_bytes(1, "little"))
            bA.extend(r2.to_bytes(1, "little"))
            # Health
            bA.extend(zero.to_bytes(1, "little"))
            bA.extend(zero.to_bytes(1, "little"))
            # Gold
            bA.extend(zero.to_bytes(1, "little"))
            bA.extend(zero.to_bytes(1, "little"))
            # Current Room #
            bA.extend(zero.to_bytes(1, "little"))
            bA.extend(zero.to_bytes(1, "little"))
            # Description Length
            bA.extend(length1.to_bytes(1, "little"))
            bA.extend(length2.to_bytes(1, "little"))
            # Description
            bA.extend(sendList[4].encode('utf-8'))
            #for x in bA:
            #    print(x)

            client.sendMsg(bA)
            i.setSend(5)
            i.setPromptLabel("Enter Command:")
        else:
            i.postPlayerMessages("WARNING- your stats are too high. \
            Attack+Defense+Regen must be lower than "\
            +str(myP.getInitialPoints()))
            i.setSend(len(sendList))



def main():
    #interface creation
    root=Tk()
    i=interface(root)

    #player creation
    myP=player()

    #client creation
    client=Client()
    client.start()

    #processing Thread
    pThread = threading.Thread(target=switch, args=(client,i,myP))
    pThread.daemon = True
    pThread.start()


    root.mainloop()

if __name__=='__main__':
    main()

