import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("Starting Raspberry Pi auto setup...")

# Update system
run("sudo apt update -y")

# Install required packages
run("sudo apt install -y hostapd dnsmasq python3-flask git")

# Enable services
run("sudo systemctl enable hostapd")
run("sudo systemctl enable dnsmasq")

print("Base install complete.")
