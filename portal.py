from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/portal")

@app.route("/portal", methods=["GET", "POST"])
def portal():
    if request.method == "POST":
        return "<h2>Connected to Pi Hotspot</h2>"

    return """
    <h2>Pi Wi-Fi</h2>
    <form method='POST'>
        <button>Connect</button>
    </form>
    """

app.run(host="0.0.0.0", port=80)
