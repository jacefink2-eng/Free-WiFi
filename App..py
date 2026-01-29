from flask import Flask, request, render_template_string

app = Flask(__name__)

# List of IP addresses that have clicked "Agree"
authorized_users = []

# The HTML page for the Terms
TERMS_HTML = """
<h1>School Van Guest WiFi</h1>
<p>By clicking below, you agree not to be a jerk on the network.</p>
<form action="/accept" method="post">
    <input type="submit" value="I Agree to the Terms">
</form>
"""

@app.route('/')
@app.route('/generate_204') # Android detection
@app.route('/hotspot-detect.html') # Apple detection
def captive_portal():
    user_ip = request.remote_addr
    if user_ip in authorized_users:
        return "<title>Success</title>Body: Success", 200
    return TERMS_HTML

@app.route('/accept', methods=['POST'])
def accept_terms():
    user_ip = request.remote_addr
    authorized_users.append(user_ip)
    return "<h1>Success!</h1><p>You can now close this window and browse.</p>"

if __name__ == '__main__':
    # Must run on Port 80 for Apple's system to find it instantly
    app.run(host='0.0.0.0', port=80)
