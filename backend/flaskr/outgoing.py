from sys import prefix
from flask import Blueprint, request
from flaskr.tradeHandler import Trades, LoadAssetObject, LoadCryptoObject, LoadTradsObject
from flaskr.scrapper import priceExtractor
from datetime import date

_TriggerCDS = False

bp = Blueprint("outgoing", __name__, url_prefix='/fromapp')

def calculate_details(tradeDict, item, cur):
    totalCost = 0.0
    totalShares = 0.0
    hodlValue = 0.0
    netGain = 0.0
    
    pe = priceExtractor()    
    # marketPrice = getPriceFun
    marketPrice = repPrice = None
    try:
        marketPrice, repPrice = pe.getPrice(item, cur) # 42000.00, 42,000.00
        for x in tradeDict:
            t_item = tradeDict[x]
            totalCost += t_item['cost'] * t_item['shares']
            totalShares += t_item['shares']
            
            realPrice = t_item['cost'] * t_item['shares']
            netGain += (marketPrice * t_item['shares']) - realPrice        
            
        hodlValue = totalShares * marketPrice
    except Exception as e:
        print("error", e)
        return {"request": "failed", "error": e}
    finally:
        pe.closeDriver()
                
    return {"totalCost":round(totalCost, 2), "totalShares": totalShares, "hodlValue": round(hodlValue, 2), "netGain": round(netGain, 2), "Price": repPrice}#,netGain


@bp.route('/')
def something():
    return "outgoing stream"

@bp.route("/getItemList")
def getItemList():
    
    try:
        asset = LoadAssetObject()    
        cryp, trad = asset.getAllItems()
        return {"data": {"crypto":cryp, "trads":trad}, "code":200}
    except Exception as e:
        print("error[getItemList] -", e)
        return{"request": 500}

@bp.route('/getWatchlist')
def getWatchlist():
    
    try:
        asset = LoadAssetObject()
        return {"data": asset.getWatchlist()}
    except Exception as e:
        print("error[/getwatchlist] -", e)
        return {"request":"500"}
    
@bp.route('/getDashboardInfo')
def getDashboardInfo():
    
    try:
        asset = LoadAssetObject()
        cryp, trad = asset.getAllItems()
        totalCost = totalValue = totalGain = 0
        
        for c in cryp:
            item, cur = c.split('_')
            x = LoadCryptoObject(item, cur)
            sh, cost = x.getTotalDetails()
            totalCost += cost
            # print(item, cur)

        for t in trad:
            item, cur = c.split('_')
            x = LoadTradsObject(item, cur)
            sh, cost = x.getTotalDetails()
            totalCost += cost
            
        return {"data": {"Totalcost":totalCost, "TotalValue": totalValue, "Totalgain": totalGain},
                "request": 200}

    except Exception as e:
        print("error[getDashboardinfo] -", e)
        return {"request": 500}
        
@bp.route('/getItemDetails')
def getItemDetails():
    
    try:      
        item = request.args.get('item')
        cur = request.args.get('cur')
        type = request.args.get('type')

        tradeObj = None

        if type=="trad": tradeObj = LoadTradsObject(item, cur)
        elif type=="cryp": tradeObj = LoadCryptoObject(item, cur)
        else: return {"request": "failed", "error": "invalid Item type"}
        
        td = tradeObj.getAllTrades()    
        out = calculate_details(td, item, cur)
        
        return {"item": out,
                "request": 200}
    except Exception as e:
        print("error[getItemDetails] -", e)

@bp.route('/getCardStructure')
def getCardData():

    if _TriggerCDS == False:
    
        crypto = {}    

        try:
            pe = priceExtractor()
            asset = LoadAssetObject()
            cryp, trad = asset.getAllItems()
            for c in cryp:
                item, cur = c.split('_')
                cryp_obj = LoadCryptoObject(item, cur)
                sh, cost = cryp_obj.getTotalDetails()
                x_trades = cryp_obj.getNetCost()
                price, change = pe.getPrice(item, cur)
                gain = 0
                
                for x in x_trades:
                    gain += (price[0]*sh)-x
                    # print(x, price[0])
                
                
                # print(change)

                if float(change['diff']) > 0.1: change['diff'] = round(change['diff'], 2)
                
                crypto[item+'/'+cur] = {"shares": sh, 
                                        "cost": cost,
                                        "netgain": round(gain, 2),
                                        "prices": price,
                                        "change": change}
                
                today = date.today().day

                if today == 1:
                    month = date.today().month
                    
                    if month == 1: month = 13
                    
                    cryp_obj.setMonthData((sh*price[0]), round(gain, 2), month)
                
        except Exception as e:
            print("error [getCardData] -", e)
        finally:
            pe.closeDriver()
        
        return {"ItemObject": crypto,
                "request": 200}

    else:
        return {"request": 500,
                "error": "http requests out of sync"}

@bp.route('/getMonthlyData')
def getMonthlyData():
    
    obj={}
    try:
        asset = LoadAssetObject()
        cryp, trad = asset.getAllItems()
        
        for c in cryp:
            item, cur = c.split('_')
            cryp_obj = LoadCryptoObject(item, cur)
            x, y, z = cryp_obj.getMonthData()
        
            obj[item+'/'+cur] = {"cost": x,
                                "hodl": y,
                                "netgain": z}
    except Exception as e:
        print("error[/getMonthlyData]", e)
        return {"request": 500,
                "error": e}
        
    obj['request'] = 200
    return obj

@bp.route('/getChartsData')
def getChartsData():
    
    try:
        asset = LoadAssetObject()
        cryp, trad = asset.getAllItems()
        
        monthly_cost = {"1":0, "2":0, "3":0, "4":0,
                        "5":0, "6":0, "7":0, "8":0,
                        "9":0, "10":0, "11":0, "12":0}
        monthly_hodl = {"1":0, "2":0, "3":0, "4":0,
                        "5":0, "6":0, "7":0, "8":0,
                        "9":0, "10":0, "11":0, "12":0}
        monthly_netgain = {"1":0, "2":0, "3":0, "4":0,
                        "5":0, "6":0, "7":0, "8":0,
                        "9":0, "10":0, "11":0, "12":0}
        
        
        for x in cryp:
            item, cur = x.split("_")
            obj = LoadCryptoObject(item, cur)
            
            cost, hodl, netgain = obj.getMonthData()
            
            for i in range(1, 13):
                monthly_cost[str(i)] += cost[str(i)]
                monthly_hodl[str(i)] += hodl[str(i)]
                monthly_netgain[str(i)] += netgain[str(i)]
                
            
            # invst += sum(list(cost.values()))
            # net_hodl += sum(list(hodl.values()))
            # net_gain += sum(list(netgain.values()))
            
        
        return{"investment": monthly_cost,
               "hodl": monthly_hodl,
               "netgain": monthly_netgain,
               "request": 200}
            
    except Exception as e:
        print("error[/getChartsData] -", e)
        return {"request": 500,
                "error": e}
    
