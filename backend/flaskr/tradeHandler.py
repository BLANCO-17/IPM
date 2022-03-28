from genericpath import isfile
import os, sys, json, pickle

def pre_setup():
    try:
        os.mkdir("./data")
    except Exception as e:
        pass

def checkTrade(itemname):
    
    if(os.path.isfile("data\\Trades\\Crypto\\"+itemname+".dat")): return True
    elif(os.path.isfile("data\\Trades\\Tradational\\"+itemname+".dat")): return True
    
    return False
        
def LoadAssetObject():
        try:
            file = open("data\\Trades\\porto.dat", "rb")
            obj = pickle.load(file)
            file.close()
            return obj
        except Exception as e:
            print("error with loading Asset object -", e)
            return {"output": "error"}

def LoadCryptoObject(item, cur):
    text = item+'_'+cur
    return pickle.load(open("data\\Trades\\Crypto\\"+ text +".dat", "rb"))

def LoadTradsObject(item, cur):
    return pickle.load(open("data\\Trades\\Tradational\\"+(item+'_'+cur)+".dat", "rb"))

    
class History:
    
    def __init__(self):
        self.months = {"1":0, "2":0, "3":0, "4":0,
                       "5":0, "6":0, "7":0, "8":0,
                       "9":0, "10":0, "11":0, "12":0}
    
    def setMonthData(self, data, name=None, number=None):
        
        if(name==None and number==None) or (number>12 or number<1) or (name not in self.months.keys()):
            raise Exception("name or number cannot be null / Out of bounds.")
                
        self.months[str(number)] =+ data
        
        return "success"
    
    def getMonthData(self, name=None, number=None):
        
        if(name==None and number==None) or (number>12 or number<1) or (name not in self.months.keys()):
            raise Exception("name or number cannot be null / Out of bounds.")
                
        if name != None:
            return self.months[name]
        else:
            return self.months[number]

#Trades class for storing item's info
class TradeChain:
    cost = None
    shares = None
    next = None
    prev = None
    month = None

class Trades:
    
    def __init__(self, item, cur):
        self.name = item
        self.cur = cur
        self.head = TradeChain()
        self.current = self.head
        
        self.monthly_cost = {"1":0, "2":0, "3":0, "4":0,
                              "5":0, "6":0, "7":0, "8":0,
                              "9":0, "10":0, "11":0, "12":0}
        self.monthly_hodl = {"1":0, "2":0, "3":0, "4":0,
                              "5":0, "6":0, "7":0, "8":0,
                              "9":0, "10":0, "11":0, "12":0}
        self.monthly_netgain = {"1":0, "2":0, "3":0, "4":0,
                              "5":0, "6":0, "7":0, "8":0,
                              "9":0, "10":0, "11":0, "12":0}
                

    def addTrade(self, cost, shares, month):
        temp = TradeChain()
        temp.cost = float(cost)
        temp.shares = float(shares)
        temp.month = int(month)
        
        temp.prev = self.current
        self.current.next = temp
        self.current = self.current.next
        self.monthly_cost[str(month)] += float(cost)
        
        return "success"

    def saveTradeObject(self, type):
        
        text = self.name+ '_' + self.cur
        if type=="cryp":        
            file = open("data\\Trades\\Crypto\\"+text+".dat", "wb")
            pickle.dump(self, file)
            file.close()
        elif type=="trad":                            
            file = open("data\\Trades\\Tradational\\"+text+".dat", "wb")
            pickle.dump(self, file)
            file.close()        
        
    def getAllTrades(self):
        temp = self.head.next        
        trades={}
        i=0
        while temp != None:
            # print(temp.cost)
            i+=1
            trades["trade "+str(i)] = {"cost":float(temp.cost), "shares":float(temp.shares), "month":temp.month}
            temp = temp.next
        
        return trades
        
    def getNetCost(self):
        temp = self.head.next        
        cost = []
        while temp != None:
            # print(temp.cost)            
            cost.append(float(temp.shares) * float(temp.cost))
            # trades["trade "+str(i)] = {"cost":float(temp.cost), "shares":float(temp.shares), "month":temp.month}
            temp = temp.next
        
        return cost        
    
    def getTotalDetails(self):
        shares=0
        cost=0
        temp = self.head.next
        while temp != None:
            cost += float(temp.cost) * float(temp.shares)
            shares += float(temp.shares)
            temp = temp.next
        return shares, cost
        
    def getCur(self):
        return self.cur
        
    def setMonthData(self, hodl, netgain, month, investment=0):
        self.monthly_hodl[str(month)] = float(hodl)
        self.monthly_netgain[str(month)] = float(netgain)
        
        if investment != 0: self.monthly_cost[str(month)] = investment
    
    def getMonthData(self):
        return self.monthly_cost, self.monthly_hodl, self.monthly_netgain
        
    def printdata(self):
        temp = self.head.next
        while temp != None:
            print(temp.shares, temp.cost)
            temp = temp.next

#Asset class for storing items info
class Asset:
        
    invst_hist = History()
    net_hist = History()
    gain_hist = History()
    # TradeObj = None

    def __init__(self):
        self.items = []
        self.crypto = []
        self.trads = []
        
        self.watchlist = []                
        
        self.init_Dir()

    def init_Dir(self):
        try:
            os.mkdir("data")
            os.mkdir("data\\Trades")
            os.mkdir("data\\Trades\\Crypto")
            os.mkdir("data\\Trades\\Tradational")

            file = open("data\\Trades\\porto.dat", "wb")
            pickle.dump(self, file)
            file.close()
            
        except Exception as e:
            pass
            # print(e)

    def SaveObject(self):
        
        file = open("data\\Trades\\porto.dat", "wb")
        pickle.dump(self, file)
        file.close()
    
    def addTradeItem(self, item, cur, type):
        text = item + '_' + cur
        if type == "cryp":
            self.crypto.append(text)
        elif type == "trad":
            self.trads.append(text)
        else: return "Invalid data"
        
        return "success"

    def addItemWL(self, item, cur):
        text = item + '_' + cur
        if text not in self.watchlist:
            self.watchlist.append(text)
            return {"request": "success"}
        else: return {"request": "failed", "error":"duplicate / Doesn't Exist"}
        
    def delItemWL(self, item, cur):
        text = item + '_' + cur
        if text in self.watchlist:
            self.watchlist.remove(text)
            return {"request": "success"}
        else: return {"request": "failed", "error":"duplicate / Doesn't Exist"}
                
    def getWatchlist(self):
        return self.watchlist
        
    def checkList(self, item, cur):
        # print(self.crypto)
        text = item + '_' + cur
        if text in self.crypto or item in self.trads: return True
        else: return False

    def getAllItems(self):
        return self.crypto, self.trads
    


# tr = Trades("BTC", "INR")
# tr.addTrade(430, 15)
# tr.addTrade(460, 20)

# us = User("user2", 1234)
# us.createUser()
# print(os.path.exists("..\\data\\test"))
# tr.saveObject("test")
# tr.printdata()
# tr = pickle.load(open("..\data\\test\\Trades\\BTC.dat", "rb"))
# tr.printdata()


