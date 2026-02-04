from flask import Flask, request, redirect, make_response
import subprocess

app = Flask(__name__)

AUTHORIZED_IPS = set()

# --- Apple captive check ---
@app.route("/hotspot-detect.html")
def apple_probe():
    # Force CNA to open portal
    return redirect("/portal", code=302)

# --- Android / Windows fallback ---
@app.route("/generate_204")
@app.route("/ncsi.txt")
def other_probe():
    return redirect("/portal", code=302)

# --- Portal page ---
@app.route("/portal", methods=["GET", "POST"])
def portal():
    client_ip = request.remote_addr

    if request.method == "POST":
        authorize(client_ip)

        # Apple expects literal "Success"
        resp = make_response("Success", 200)
        resp.headers["Content-Type"] = "text/plain"
        return resp

    return f"""
    <html>
    <head>
      <meta name="viewport" content="width=device-width">
      <title>Free Wi-Fi</title>
    </head>
    <body>
      <h2>Free Wi-Fi Access</h2>
      <p>You must accept to continue.</p>
      <form method="POST">
        <button type="submit">Accept & Connect</button>
      </form>
    </body>
    </html>
    """

def authorize(ip):
    if ip in AUTHORIZED_IPS:
        return

    AUTHORIZED_IPS.add(ip)

    # Allow internet for this IP
    subprocess.call([
        "iptables", "-I", "FORWARD", "-s", ip, "-j", "ACCEPT"
    ])
    subprocess.call([
        "iptables", "-I", "FORWARD", "-d", ip, "-j", "ACCEPT"
    ])

    print("Authorized:", ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
