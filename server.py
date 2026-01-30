from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/trigger", methods=["GET", "POST"])
def trigger():
    source = request.headers.get("User-Agent", "unknown")
    return jsonify({
        "status": "ok",
        "message": "Triggered successfully",
        "source": source,
        "time": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
