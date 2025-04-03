import requests
import socketio

SERVER_URL = "http://localhost:5000"

sio = socketio.Client()

@sio.on("new_clip")
def on_new_clip(data):
    print(f"\n[🔔 Nouveau contenu reçu] {data['content']}")

sio.connect(SERVER_URL)

while True:
    print("\nOptions : [1] Voir historique  [2] Ajouter  [3] Quitter")
    choix = input("> ")

    if choix == "1":
        response = requests.get(f"{SERVER_URL}/history")
        clips = response.json()
        for c in clips:
            print(f"{c['timestamp']} - {c['content']}")

    elif choix == "2":
        content = input("Entrez le texte à ajouter : ")
        requests.post(f"{SERVER_URL}/add", json={"content": content})

    elif choix == "3":
        break
