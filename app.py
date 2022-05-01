from flask import Flask
from app_blueprint import app_blueprint
app = Flask(__name__)
app.register_blueprint(app_blueprint)
app.secret_key = "Donttestmypatience"

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
