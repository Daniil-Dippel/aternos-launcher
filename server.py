from flask import Flask, jsonify
from aternos import Client
import os

app = Flask(__name__)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

@app.route("/start", methods=["POST"])
def start_server():
    try:
        at = Client()
        at.login(EMAIL, PASSWORD)
        server = at.account.servers[0]

        if server.status != "online":
            server.start()
            return jsonify({"message": "Сервер запускается..."})
        else:
            return jsonify({"message": "Сервер уже включён."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))