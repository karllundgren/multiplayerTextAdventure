from tkinter import *
import threading
class interface():
    send=[]
    sendLock = threading.Lock()

    def retrieveSend(self, event=None):
        with self.sendLock:
            self.send.append(self.myMessage.get(1.0, END).rstrip())
            self.myMessage.delete(1.0, END)
            #print (len(self.send))

    def setSend(self, number):
        with self.sendLock:
            for x in range(number):
                self.send.pop(0)

    def setPromptLabel(self, text):
        self.prompt['text'] = text

    def quit(self):
        print ("we have quit")


    def postPlayerMessages(self, message):
        self.playerMessages.insert(2.0, "\n")
        self.playerMessages.insert(2.0, message)

    def postRoomMessages(self, message):
        self.rooms.insert(2.0, "\n")
        self.rooms.insert(2.0, message)


    def postPeople(self,messageList):
        self.people.insert(2.0, "\n")
        for lmnop in reversed(messageList):
            self.people.insert(2.0, "\n"+lmnop)


    def postStats(self, messageList):
        self.stats.delete(2.0,END)
        for lmnop in reversed(messageList):
            self.stats.insert(2.0, "\n"+lmnop)


    def getSend(self):
        with self.sendLock:
            return self.send


    def __init__(self, master):
        master.title("COMMANDS: F-Fight;    S-Start;    Q-Quit;    C-Change room;    V-Player VS Player;    L-loot;    M-Message")
        master.geometry("1200x560")
        for r in range(12):
            master.rowconfigure(r, weight=1)
        for c in range(20):
            master.columnconfigure(c, weight=1)

        topFrame=Frame(master, bg='cyan')

        leftFrame = Frame(master, bg='gray')
        midLeftFrame = Frame(master, bg='gray')
        midRightFrame = Frame(master, bg='gray')
        rightFrame = Frame(master, bg='gray')

        lineFrame = Frame(master, bg='cyan')
        bottomFrame = Frame(master, bg='cyan')

        topFrame.grid(row=0,column=0, rowspan=1, columnspan=20, sticky=N+W+E+S)
        leftFrame.grid(row=1, column=0, rowspan=8, columnspan=5, sticky=N + E + S + W)
        midLeftFrame.grid(row=1, column=5, rowspan=8, columnspan=5, sticky=N + E + S + W)
        midRightFrame.grid(row=1, column=10, rowspan=8, columnspan=5, sticky=N + E + S + W)
        rightFrame.grid(row=1, column=15, rowspan=8, columnspan=5, sticky=N + E + S + W)

        lineFrame.grid(row=9, column=0, rowspan=1, columnspan=20, sticky=N + W + E + S)
        bottomFrame.grid(row=10, column=0, rowspan=1, columnspan=20, sticky=N + E + S + W)

        #top
        #slabel=Label(topFrame, text="Your Stats")
        #slabel.grid(row=0, column=1)
        #elabel = Label(topFrame, text="Environment")
        #elabel.grid(row=0, column=10)

        #left
        self.stats = Text(leftFrame, height=30, width=30, borderwidth=3, relief="sunken")
        self.stats.insert(END, "YOUR STATS\n")
        self.stats.grid(row=0, column=0, columnspan=5, rowspan=8)

        #midLeft
        self.rooms = Text(midLeftFrame, height=30, width=30, borderwidth=3, relief="sunken")
        self.rooms.insert(END,"ROOMS\n")
        self.rooms.grid(column=5, columnspan=5, rowspan=8)

        #midRight
        self.people = Text(midRightFrame, height=30, width=30, borderwidth=3, relief="sunken")
        self.people.insert(END, "PEOPLE/MONSTERS\n")
        self.people.grid(row=0, column=10, columnspan=5, rowspan=8)

        #Right
        self.playerMessages = Text(rightFrame, height=30, width=30, borderwidth=3, relief="sunken")
        self.playerMessages.insert(END, "MESSAGES\n")
        self.playerMessages.grid(row=0, column=15, columnspan=5, rowspan=8, sticky="nsew")

        #scrollb = Scrollbar(self.playerMessages, command=self.playerMessages.yview)
        #scrollb.grid(row=0, column=15, sticky='nsew')
        #self.playerMessages['yscrollcommand'] = scrollb.set
        #scrollb.place(in_=self.playerMessages, relx=1.0, relheight=1.0)

        #bottom
        self.prompt=Label(bottomFrame, text="Enter Command:")
        self.prompt.grid(row=1, column=1)
        self.myMessage = Text(bottomFrame, height=2.5, width=130)
        self.myMessage.grid(row=1, column=2)
        self.myMessage.bind("<Return>", self.retrieveSend)




'''


tex=Text(leftFrame)
labelr=Label(bottomFrame, text="Right Frame")
label=Label(bottomFrame, text="Type here")
message=Entry(bottomFrame)
button=Button(bottomFrame, text="Submit")


tex.insert(END,"what the heckdddddddddddddddddddddddddddddddddddddddddddddddd")
tex.grid(column=1,columnspan=3)

label.grid(row=0,column=7)
message.grid(row=0,column=8)
button.grid(row=1,columnspan=2)
message.bind("<Button-1>", GUItext)
'''