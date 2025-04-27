from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)

# Definícia databázového modelu
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'description': self.description,
            'done': self.done
        }

# Inicializácia databázy
with app.app_context():
    db.create_all()

# Pomocná funkcia na broadcast aktuálnych úloh
def broadcast_tasks():
    tasks = Task.query.all()
    tasks_json = [task.to_dict() for task in tasks]
    socketio.emit("update", tasks_json)

@app.route("/ulohy", methods=["GET"])
def get_ulohy():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route("/ulohy", methods=["POST"])
def pridaj_ulohu():
    data = request.json
    nova_ul = Task(
        text=data.get("text", ""),
        description=data.get("description", ""),
        done=data.get("done", False)
    )
    db.session.add(nova_ul)
    db.session.commit()
    broadcast_tasks()
    return jsonify(nova_ul.to_dict()), 201

@app.route("/ulohy/<int:uloha_id>", methods=["DELETE"])
def zmaz_ulohu(uloha_id):
    task = Task.query.get(uloha_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        broadcast_tasks()
        return jsonify({"message": "Úloha zmazaná"}), 200
    else:
        return jsonify({"error": "Úloha nenájdená"}), 404

@app.route("/ulohy/<int:uloha_id>", methods=["PUT"])
def uprav_ulohu(uloha_id):
    task = Task.query.get(uloha_id)
    if task:
        data = request.json
        task.text = data.get("text", task.text)
        task.description = data.get("description", task.description)
        task.done = data.get("done", task.done)
        db.session.commit()
        broadcast_tasks()
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Úloha nenájdená"}), 404

@socketio.on("connect")
def on_connect():
    tasks = Task.query.all()
    tasks_json = [task.to_dict() for task in tasks]
    emit("update", tasks_json)

if __name__ == "__main__":
    socketio.run(app, debug=True)
