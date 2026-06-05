import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("Configuring Wi-Fi hotspot...")

hostapd_conf = """
interface=wlan0
ssid=PiHotspot
channel=6
driver=nl80211
"""

dnsmasq_conf = """
interface=wlan0
dhcp-range=192.168.4.10,192.168.4.200,255.255.255.0,24h
address=/#/192.168.4.1
"""

open("/tmp/hostapd.conf", "w").write(hostapd_conf)
open("/tmp/dnsmasq.conf", "w").write(dnsmasq_conf)

run("sudo mv /tmp/hostapd.conf /etc/hostapd/hostapd.conf")
run("sudo mv /tmp/dnsmasq.conf /etc/dnsmasq.conf")

run("sudo systemctl restart hostapd")
run("sudo systemctl restart dnsmasq")

print("Hotspot ready.")
