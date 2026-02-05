from flask import Flask, request, redirect, make_response
import subprocess

app = Flask(__name__)

AUTHORIZED_IPS = set()

# -------------------------------------------------
# Apple Captive Network Assistant
# -------------------------------------------------
@app.route("/hotspot-detect.html")
def apple_probe():
    return redirect("/portal", code=302)

# -------------------------------------------------
# Android / Windows connectivity checks
# -------------------------------------------------
@app.route("/generate_204")
@app.route("/ncsi.txt")
def other_probe():
    return redirect("/portal", code=302)

# -------------------------------------------------
# Portal Page
# -------------------------------------------------
@app.route("/portal", methods=["GET", "POST"])
def portal():
    client_ip = request.remote_addr

    if request.method == "POST":
        authorize_ip(client_ip)

        # Apple needs EXACT "Success"
        resp = make_response("Success", 200)
        resp.headers["Content-Type"] = "text/plain"
        resp.headers["Refresh"] = "1; url=/connected"
        return resp

    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<title>Van Wi-Fi</title>
<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
  text-align: center;
  padding: 40px;
}
button {
  font-size: 18px;
  padding: 14px 28px;
  border-radius: 10px;
  border: none;
  background: #007aff;
  color: white;
}
</style>
</head>
<body>
  <h2>Van Wi-Fi Access</h2>
  <p>Please agree to use the van Wi-Fi.</p>

  <form method="POST">
    <button type="submit">Agree to Van Wi-Fi</button>
  </form>
</body>
</html>
"""

# -------------------------------------------------
# Connected Page (Shown After Accept)
# -------------------------------------------------
@app.route("/connected")
def connected():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<title>Connected</title>
<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
  text-align: center;
  padding: 40px;
}
h2 {
  color: #2ecc71;
}
</style>
</head>
<body>
  <h2>✅ Connected to Van Wi-Fi</h2>
  <p>You’re all set. You may now use the Wi-Fi.</p>
  <p style="font-size:14px;color:#666;">
    You can close this page.
  </p>
</body>
</html>
"""

# -------------------------------------------------
# Apple Shortcuts Endpoint (Offline)
# -------------------------------------------------
@app.route("/shortcut", methods=["POST"])
def shortcut():
    client_ip = request.remote_addr
    authorize_ip(client_ip)
    return redirect("/connected")

# -------------------------------------------------
# Firewall Authorization
# -------------------------------------------------
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

    print("Van Wi-Fi authorized:", ip)

# -------------------------------------------------
# Start Server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
