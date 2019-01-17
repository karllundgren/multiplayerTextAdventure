
class player():
    currentRoom = 1
    name = ""
    initialPoints = 500
    Flags='11111'
    Gold = 0
    Attack = 0
    Defense = 0
    Regen = 0
    Status = ""
    Location = "0"
    Health = 1
    Started = "NO"
    statLimit = 65535
    description = ""
    roomOfRequirement=0

    def setROQ(self):
        self.roomOfRequirement+=1
    def getROQ(self):
        return self.roomOfRequirement

    def setFlags(self, f):
        new=f+'000'
        #print("set flags old: "+self.Flags+" new flag: "+new)
        self.Flags=self.Flags.replace('0', '')
        self.Flags = self.Flags.replace('1', '')

        self.Flags=new
    def setInitialPoints(self, ip):
        # initialPoints= combo of health defense, and regen (cannot be exceeded)
        self.initialPoints = ip

    def setGold(self, g):
        self.Gold += g

    def setAttack(self, g):
        self.Attack = g

    def setDefense(self, g):
        self.Defense = g

    def setRegen(self, g):
        self.Regen = g

    def setStatus(self, g):
        self.Status = g

    def setLocation(self, g):
        self.Location = g

    def setHealth(self, g):
        self.Health = g

    def setStarted(self, g):
        self.Started = g

    def setStatLim(self, s):
        self.statLimit = s

    def setName(self, s):
        self.name = s

    def setDescr(self, s):
        self.description = s

    def setCurrentRoom(self, r):
        self.currentRoom = r

    def getCurrentRoom(self):
        return self.currentRoom

    def getFlags(self):
        return self.Flags

    def getFlagInt(self):
        number=0
        for x in range(len(self.Flags)):
            if self.Flags[x]=='1':
                if x==0:
                    number+=128
                elif x==1:
                    number+=64
                elif x == 2:
                    number+=32
                elif x == 3:
                    number+=16
                elif x == 4:
                    if self.Health > 0:
                        number+=8
        return number
    def died(self):
        string='0'+self.Flags[1]+self.Flags[2]+self.Flags[3]+self.Flags[4]
        #print("the players corpse flag string is: " + string)
        self.setFlags(string)


    def isAlive(self):
        flags=self.Flags
        if flags[0]=='1':
            return True
        else:
            return False


    def getDescr(self):
        return self.description

    def getName(self):
        return self.name

    def getGold(self):
        return self.Gold

    def getAttack(self):
        return self.Attack

    def getDefense(self):
        return self.Defense

    def getRegen(self):
        return self.Regen

    def getStatus(self):
        return self.Status

    def getLocation(self):
        return self.Location

    def getHealth(self):
        return self.Health

    def getStarted(self):
        return self.Started

    def getInitialPoints(self):
        return self.initialPoints