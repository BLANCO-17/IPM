from tests import client
import pytest, json

def test_index(client):
    rec = client.get('/toapp/')
    assert rec.data == b"incoming stream"

def test_getItems(client):
    rec = client.get('/fromapp/getItemList')
    data = json.loads(rec.data)
    assert data['code'] == 200
    
# def test_addItem_success(client):
#     rec = client.get('/toapp/addItem?item=eth&cur=usd&testing=on')
#     data = json.loads(rec.data)
#     assert data['request'] == 200    
# def test_addItem_duplicate(client):
#     rec = client.get('/toapp/addItem?item=btc&cur=usd&testing=on')
#     data = json.loads(rec.data)
#     assert data['request'] == "failed"

# def test_delItem(client):
#     rec = client.get('/toapp/delItem?item=btc&cur=usd&testing=on')
#     data = json.loads(rec.data)
#     assert data['request'] == 200
#     assert data['output'] == "success"  
    
def test_addTradeItem_success(client):
    rec = client.get('/toapp/addTradeItem?item=btc&cur=usd&cost=20000&shares=0.1&type=cryp&month=1&testing=on')
    data = json.loads(rec.data)
    assert data['request'] == 200
    
def test_addTradeItem_fail(client):
    rec = client.get('/toapp/addTradeItem?item=btc&cur=usd&cost=20000&shares=0.1&type=crypto&month=1&testing=on')
    data = json.loads(rec.data)
    assert data['request'] == "failed"
            