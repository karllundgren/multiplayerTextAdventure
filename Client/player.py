
class player():
    name=""
    initialPoints=0
    Gold=0
    Attack=0
    Defense=0
    Regen=0
    Status=""
    Location=""
    Health=0
    Started="NO"
    statLimit="NO"
    description=""

    def __init__(self):
        #initialPoints= combo of health defense, and regen (cannot be exceeded)
        pass

    def statsToGui(self):
        statList=[]
        statList.append("Name: "+ self.name)
        statList.append("Description: "+str(self.description))
        statList.append("Gold: "+str(self.Gold))
        statList.append("Attack: " + str(self.Attack))
        statList.append("Defense: " + str(self.Defense))
        statList.append("Regen: " + str(self.Regen))
        statList.append("Status: " + self.Status+"\n")
        #statList.append("Location: " + self.Location)
        statList.append("Health: " + str(self.Health))
        return statList

    def setInitialPoints(self, ip):
        # initialPoints= combo of health defense, and regen (cannot be exceeded)
        self.initialPoints=ip
    def setGold(self, g):
        self.Gold=g
    def setAttack(self, g):
        self.Attack=g
    def setDefense(self, g):
        self.Defense=g
    def setRegen(self, g):
        self.Regen=g
    def setStatus(self, g):
        self.Status=g
    def setLocation(self, g):
        self.Location=g
    def setHealth(self, g):
        self.Health=g
    def setStarted(self, g):
        self.Started=g
    def setStatLim(self,s):
        self.statLimit=s

    def setName(self, s):
        self.name = s

    def setDescr(self, s):
        self.description = s

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