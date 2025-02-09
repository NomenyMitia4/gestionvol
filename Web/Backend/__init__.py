from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app
