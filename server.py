# Hybrid Flask Server
from flask import Flask, request, abort
from pyngrok import ngrok
import requests

app = Flask(__name__)
SECRET_KEY = "FREEWIFI-9f3cA1x"

@app.route("/trigger")
def trigger():
    key = request.args.get("key")
    if key != SECRET_KEY:
        abort(403)
    print("Authorized trigger received")
    return "OK"

def internet_available():
    try:
        requests.get("https://google.com", timeout=3)
        return True
    except:
        return False

if __name__ == "__main__":
    if internet_available():
        public_url = ngrok.connect(5000)
        print("🌐 Online URL:", public_url)
    else:
        print("⚡ Offline mode, local network only")
    app.run(host="0.0.0.0", port=5000)
