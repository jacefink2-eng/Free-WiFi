from flask import Flask, request, redirect, make_response
import time

app = Flask(__name__)

AUTHORIZED_IPS = set()

# -----------------------------------------
# Northeast Minnesota Bounding Box Example
# -----------------------------------------
LAT_MIN = 46.0
LAT_MAX = 49.4

LON_MIN = -95.2
LON_MAX = -89.4

# -----------------------------------------
# GPS LOCATION FUNCTION
# Replace with actual GPS hardware reading
# -----------------------------------------
def get_current_location():
    """
    Example only.
    Replace with GPS receiver code.
    """

    # Example: Duluth area
    latitude = 46.7867
    longitude = -92.1005

    return latitude, longitude


def location_allowed():
    lat, lon = get_current_location()

    return (
        LAT_MIN <= lat <= LAT_MAX
        and LON_MIN <= lon <= LON_MAX
    )


# -----------------------------------------
# Apple Captive Portal Detection
# -----------------------------------------
@app.route("/hotspot-detect.html")
def apple_probe():
    return redirect("/portal", code=302)


# -----------------------------------------
# Android / Windows Detection
# -----------------------------------------
@app.route("/generate_204")
@app.route("/ncsi.txt")
def other_probe():
    return redirect("/portal", code=302)


# -----------------------------------------
# Portal
# -----------------------------------------
@app.route("/portal", methods=["GET", "POST"])
def portal():
    client_ip = request.remote_addr

    if request.method == "POST":

        if not location_allowed():
            return """
            <html>
            <body style="font-family:Arial;text-align:center;padding:40px;">
                <h2>Service Unavailable</h2>
                <p>This Wi-Fi service is currently outside the allowed coverage area.</p>
            </body>
            </html>
            """, 403

        authorize_ip(client_ip)

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
    </head>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h2>Van Wi-Fi Access</h2>
        <p>Agree to continue.</p>

        <form method="POST">
            <button type="submit">
                Agree to Van Wi-Fi
            </button>
        </form>
    </body>
    </html>
    """


# -----------------------------------------
# Connected
# -----------------------------------------
@app.route("/connected")
def connected():
    lat, lon = get_current_location()

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h2>Connected</h2>

        <p>You may now use the network.</p>

        <p>
            GPS:
            {lat:.4f},
            {lon:.4f}
        </p>
    </body>
    </html>
    """


# -----------------------------------------
# Status Endpoint
# -----------------------------------------
@app.route("/status")
def status():

    lat, lon = get_current_location()

    return {
        "authorized_clients": len(AUTHORIZED_IPS),
        "latitude": lat,
        "longitude": lon,
        "inside_region": location_allowed(),
        "server_time": time.time()
    }


# -----------------------------------------
# Authorization
# -----------------------------------------
def authorize_ip(ip):

    if ip in AUTHORIZED_IPS:
        return

    AUTHORIZED_IPS.add(ip)

    print("Authorized:", ip)


# -----------------------------------------
# Start Server
# -----------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80
    )
