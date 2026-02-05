from flask import Flask, request, redirect, make_response
import subprocess

app = Flask(__name__)

AUTHORIZED_IPS = set()

# ----------------------------
# Apple Captive Network Assistant
# ----------------------------
@app.route("/hotspot-detect.html")
def apple_probe():
    return redirect("/portal", code=302)

# ----------------------------
# Android / Windows checks
# ----------------------------
@app.route("/generate_204")
@app.route("/ncsi.txt")
def other_probe():
    return redirect("/portal", code=302)

# ----------------------------
# Main portal
# ----------------------------
@app.route("/portal", methods=["GET", "POST"])
def portal():
    client_ip = request.remote_addr

    if request.method == "POST":
        authorize_ip(client_ip)

        # Apple expects EXACT "Success"
        resp = make_response("Success", 200)
        resp.headers["Content-Type"] = "text/plain"
        return resp

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<title>Free Wi-Fi</title>
<style>
body {{
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 40px;
}}
button {{
  font-size: 18px;
  padding: 12px 24px;
}}
</style>
</head>
<body>
  <h2>Free Wi-Fi Access</h2>
  <p>Tap accept to connect.</p>
  <form method="POST">
    <button type="submit">Accept & Connect</button>
  </form>
</body>
</html>
"""

# ----------------------------
# Firewall authorization
# ----------------------------
def authorize_ip(ip):
    if ip in AUTHORIZED_IPS:
        return

    AUTHORIZED_IPS.add(ip)

    subprocess.call([
        "iptables", "-I", "FORWARD", "-s", ip, "-j", "ACCEPT"
    ])
    subprocess.call([
        "iptables", "-I", "FORWARD", "-d", ip, "-j", "ACCEPT"
    ])

    print("Authorized:", ip)

# ----------------------------
# Start server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
