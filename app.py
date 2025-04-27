from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket server

# Simulovaná databáza
ulohy = []
next_id = 1

@app.route("/ulohy", methods=["GET"])
def get_ulohy():
    return jsonify(ulohy)

@app.route("/ulohy", methods=["POST"])
def pridaj_ulohu():
    global next_id
    data = request.json
    nova_ul = {
        "id": next_id,
        "text": data.get("text", ""),
        "done": data.get("done", False)
    }
    ulohy.append(nova_ul)
    next_id += 1
    socketio.emit("update", ulohy)  # 🔄 Broadcast
    return jsonify(nova_ul), 201

@app.route("/ulohy/<int:uloha_id>", methods=["DELETE"])
def zmaz_ulohu(uloha_id):
    global ulohy
    ulohy = [u for u in ulohy if u["id"] != uloha_id]
    socketio.emit("update", ulohy)  # 🔄 Broadcast
    return jsonify({"message": "Úloha zmazaná"}), 200

@app.route("/ulohy/<int:uloha_id>", methods=["PUT"])
def uprav_ulohu(uloha_id):
    data = request.json
    for uloha in ulohy:
        if uloha["id"] == uloha_id:
            uloha["text"] = data.get("text", uloha["text"])
            uloha["done"] = data.get("done", uloha.get("done", False))
            socketio.emit("update", ulohy)  # 🔄 Broadcast
            return jsonify(uloha)
    return jsonify({"error": "Úloha nenájdená"}), 404

@socketio.on("connect")
def on_connect():
    emit("update", ulohy)  # Po pripojení klientovi pošleme stav

if __name__ == "__main__":
    socketio.run(app, debug=True)
