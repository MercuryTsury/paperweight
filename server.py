from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connexion MySQL
db = pymysql.connect(host="localhost", user="root", password="", database="clipboard")
cursor = db.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clipboard (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
db.commit()

# Récupérer l'historique
@app.route("/history", methods=["GET"])
def get_history():
    cursor.execute("SELECT * FROM clipboard ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    return jsonify([{"id": row[0], "content": row[1], "timestamp": row[2]} for row in data])

# Ajouter un élément
@app.route("/add", methods=["POST"])
def add_clipboard():
    content = request.json.get("content")
    if content:
        cursor.execute("INSERT INTO clipboard (content) VALUES (%s)", (content,))
        db.commit()
        socketio.emit("new_clip", {"content": content})  # Notifier les clients
        return jsonify({"message": "Ajouté"}), 201
    return jsonify({"error": "Contenu vide"}), 400

@socketio.on("connect")
def handle_connect():
    print("Client connecté")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
