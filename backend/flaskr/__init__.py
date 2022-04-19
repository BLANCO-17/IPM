import os
from flask import Flask, request
from flaskr.tradeHandler import Asset 
#, LoadTrads_Object, LoadCrypto_Object

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass        

    @app.route('/')
    def home():
        return {"status": 200}

    from flaskr import incoming, outgoing
    app.register_blueprint(incoming.bp)
    app.register_blueprint(outgoing.bp)
    
    return app

asset = Asset()
del asset
# LoadObject = LoadAssetObject
app = create_app()
