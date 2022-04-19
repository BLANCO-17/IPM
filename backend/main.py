# To create the application package(exe), use this file

from flaskr import app

if __name__ == "__main__":
    try:
        app.run()
    except Exception as msg:
        print(msg)