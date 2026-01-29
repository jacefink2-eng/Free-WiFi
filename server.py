from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Track who clicked "Agree" by their IP address
authorized_ips = set()

# The HTML for your "Agree to Terms" page
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>School Van WiFi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #f0f0f0; }
        .box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        button { background: #007bff; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Welcome to Van WiFi</h1>
        <p>By clicking agree, you promise to follow school rules while browsing.</p>
        <form action="/agree" method="post">
            <button type="submit">I Agree to the Terms</button>
        </form>
    </div>
</body>
</html>
"""

# 1. Handle Apple/Android "Captive Network" detection
@app.route('/')
@app.route('/generate_204')       # Android
@app.route('/hotspot-detect.html') # Apple
def captive_portal():
    user_ip = request.remote_addr
    if user_ip in authorized_ips:
        # If already agreed, return "Success" so the phone lets them browse
        return "<title>Success</title>Success", 200
    return HTML_PAGE

# 2. When the user clicks the button
@app.route('/agree', methods=['POST'])
def agree():
    user_ip = request.remote_addr
    authorized_ips.add(user_ip)
    return "<h1>You are now connected!</h1><p>You can close this window and use the internet.</p>"

if __name__ == '__main__':
    # PORT 80 is required for the "Pop-up" to work on mobile devices
    # Use 5000 if testing on GitHub Codespaces
    app.run(host='0.0.0.0', port=80)
