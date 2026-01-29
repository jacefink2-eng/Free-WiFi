import os
import subprocess
import sys

def run(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def install_system():
    print("--- Installing System Dependencies ---")
    # dnsmasq handles DNS, hostapd handles the WiFi signal
    run("sudo apt update")
    run("sudo apt install -y python3-flask dnsmasq hostapd git")

def configure_networking():
    print("--- Configuring WiFi Hotspot ---")
    # 1. Set static IP for the Pi's antenna
    with open("/etc/dhcpcd.conf", "a") as f:
        f.write("\ninterface wlan0\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant\n")

    # 2. Configure the WiFi Name and Password
    hostapd_conf = """
interface=wlan0
driver=nl80211
ssid=Van_WiFi_Free
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=schoolvan
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(hostapd_conf)

def create_auto_start():
    print("--- Setting Python Server to Start on Boot ---")
    # Creates a Linux service so the portal starts when the van turns on
    service_code = """
[Unit]
Description=Captive Portal Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/raspi-captive-portal/server/server.py
WorkingDirectory=/home/pi/raspi-captive-portal/server
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
    with open("/etc/systemd/system/portal.service", "w") as f:
        f.write(service_code)
    run("sudo systemctl enable portal.service")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("You must run this as root! Use: sudo python3 setup.py")
        sys.exit(1)
    
    install_system()
    configure_networking()
    create_auto_start()
    print("\nSUCCESS: Reboot your Pi now to activate the Van WiFi!")
