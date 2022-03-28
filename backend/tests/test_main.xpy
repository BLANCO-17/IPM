# import os, tempfile, pytest, json
# from flaskr import app

# @pytest.fixture
# def client():

#     # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
    
#     with app.test_client() as client:
#         with app.app_context():
#             # flaskr.app.init_db()
#             pass
#         yield client
       
    
# def test_index_status(client):
#     rv = client.get('/')
#     data = json.loads(rv.data)
#     assert data['status'] == 200
    

    