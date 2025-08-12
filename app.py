import os
import requests
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

API_KEY = "sk_af7eaadd9f8b0813b91e5b94794b04c0f22aaefae4a77bfb"  # your actual API key

def get_all_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json().get("voices", []) if response.status_code == 200 else []

@app.route("/")
def index():
    voices = get_all_voices()
    return render_template("index.html", voices=voices)

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form["text"]
    voice_id = request.form["voice"]

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Use this unless voice requires another
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(tts_url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error from ElevenLabs: {response.text}", 500

    os.makedirs("static", exist_ok=True)
    with open("static/output.mp3", "wb") as f:
        f.write(response.content)

    return "", 204

@app.route("/play")
def play():
    return send_file("static/output.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
