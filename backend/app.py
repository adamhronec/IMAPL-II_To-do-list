from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definícia databázového modelu
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    user_name = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'description': self.description,
            'due_date': self.due_date,
            'user_name': self.user_name,
            'done': self.done
        }

# Inicializácia databázy
with app.app_context():
    db.create_all()

@app.route("/ulohy", methods=["GET"])
def get_ulohy():
    user_name = request.args.get('user_name')
    if user_name:
        tasks = Task.query.filter_by(user_name=user_name).all()
    else:
        tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route("/ulohy", methods=["POST"])
def pridaj_ulohu():
    data = request.json
    nova_ul = Task(
        text=data.get("text", ""),
        description=data.get("description", ""),
        due_date=data.get("due_date", ""),
        user_name=data.get("user_name", "anonym"),
        done=data.get("done", False)
    )
    db.session.add(nova_ul)
    db.session.commit()
    return jsonify(nova_ul.to_dict()), 201

@app.route("/ulohy/<int:uloha_id>", methods=["DELETE"])
def zmaz_ulohu(uloha_id):
    task = Task.query.get(uloha_id)
    if task:
        db.session.delete(task)
        db.session.commit()
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
        task.due_date = data.get("due_date", task.due_date)
        task.done = data.get("done", task.done)
        db.session.commit()
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Úloha nenájdená"}), 404

if __name__ == "__main__":
    app.run(debug=True)
