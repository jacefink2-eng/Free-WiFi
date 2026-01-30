from flask import Flask, request, abort

app = Flask(__name__)

SECRET_KEY = "FREEWIFI-9f3cA1x"

@app.route("/")
def home():
    return "Server running"

@app.route("/trigger")
def trigger():
    key = request.args.get("key")
    if key != SECRET_KEY:
        abort(403)  # Forbidden

    # 🔥 Action goes here
    print("Authorized trigger received")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
