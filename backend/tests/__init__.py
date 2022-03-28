import os, tempfile, pytest, json
from flaskr import app

@pytest.fixture
def client():

    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # flaskr.app.init_db()
            pass
        yield client
    
    # os.close(db_fd)
    # os.unlink(app.config['DATABASE'])
        

# # def test_addItem_success(client):
# #     rec = client.get('/toapp/addItem?item=xrp&type=cryp&testing=on')
# #     data = json.loads(rec.data)
# #     assert data['request'] == "success"
    
# # def test_addItem_duplicate(client):
# #     rec = client.get('/toapp/addItem?item=btc&type=cryp&testing=on')
# #     data = json.loads(rec.data)
# #     assert data['request'] == "null"
            
    
# # def test_index_status(client):
# #     rv = client.get('/')
# #     data = json.loads(rv.data)
# #     assert data['status'] == 200
    