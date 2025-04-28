from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello, Flask server is running!"

    return app

# Exécuter en local avec python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
