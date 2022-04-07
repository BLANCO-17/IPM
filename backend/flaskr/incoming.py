from tkinter import E
from flask import Blueprint, request
from flaskr.tradeHandler import Trades, LoadAssetObject, LoadCryptoObject, LoadTradsObject

bp = Blueprint("incoming", __name__, url_prefix='/toapp')

@bp.route("/")
def Index_Inc():
    return "incoming stream"

@bp.route("/addTradeItem")
def addTradeItem():
    
    asset = LoadAssetObject()
    
    try:
        item = request.args.get('item')
        cur = request.args.get('cur')
        cost = request.args.get('cost')
        shares = request.args.get('shares')
        type = request.args.get('type')
        month = int(request.args.get('month'))
        testing = request.args.get('testing')

        if type != "cryp" and type != "trad": return {"request": "failed", "error":"invalid Item type"}
        if month < 1 or month > 12: return {"request": "failed", "error": "Invalid month var value"}
        
        tradeObj = None
        output = "null"
        if not asset.checkList(item, cur):
            tradeObj = Trades(item, cur)
            tradeObj.addTrade(cost, shares, month)
            tradeObj.saveTradeObject(type)
            output = asset.addTradeItem(item, cur, type)
            
        else:
            
            if type == "cryp":
                tradeObj = LoadCryptoObject(item, cur)
                output = tradeObj.addTrade(cost, shares, month)
            elif type == "trad":
                tradeObj = LoadTradsObject(item, cur)
                output = tradeObj.addTrade(cost, shares, month)
                
            
        if testing != "on":
            asset.SaveObject()
            tradeObj.saveTradeObject(type)

        return {"request": 200,
                "output": output}

    except Exception as e:
        print(e)
        return {"output": "error - "+str(e)}

@bp.route('/addWatchlistItem')
def addItemWL():

    asset = LoadAssetObject()
    item = request.args.get('item')
    cur = request.args.get('cur')
    testing = request.args.get('testing')
    
    out = asset.addItemWL(item, cur)
    
    if testing != "on":
        asset.SaveObject()
    
    return out

@bp.route('/delItem')
def delItemWL():
    
    try:
        
        asset = LoadAssetObject()
        item = request.args.get('item')
        cur = request.args.get('cur')
        testing = request.args.get('testing')
        
        out = asset.delItemWL(item, cur)
        
        if testing != "on":
            asset.SaveObject()
        
        return{"request": 200,
               "output": out}
    except Exception as e:
        return{"request": 500,
               "error": e}

@bp.route('/setMonthData')
def setMonthData():
    
    try:
        item = request.args.get('item')
        cur = request.args.get('cur')
        month = request.args.get('month')
        invst = request.args.get('investment')
        netgain = request.args.get('netgain')
        hodl = request.args.get('hodl')
        testing = request.args.get('testing')
        
        obj = LoadCryptoObject(item, cur)
        obj.setMonthData(float(hodl), float(netgain), int(month), investment=float(invst))

        if testing != "on":
            obj.saveTradeObject("cryp")
            
        return {"request": 200}
        
    except Exception as e:
        err = "error[/setMonthData] - " + e
        print(err)
        
        return {"request": 500,
                "error": err}
