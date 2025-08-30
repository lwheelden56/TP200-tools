# Script to automate Toast TP200/TP200W printer reboots

import requests
from scapy.all import ARP, Ether, srp
import re

# Scan Subnet for devices
def scan_subnet(subnet):
    print(f"Scanning subnet: {subnet}")
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append(received.psrc)
    print(len(devices), "Devices Found")
    return devices

# Verify it is a printer
def check_device(ip, exempt_ips):
    if ip in exempt_ips:
        return

    try:
        response = requests.get(f"http://{ip}", timeout=2)
        if response.status_code == 200:
            # Check if the response contains the specific HTML to id
            if re.search(r'<TITLE>Ethernet port configuration</TITLE>', response.text):
                print(f"{ip}: Rebooting...")
                reboot_device(ip)
            else:
                print(f"{ip} is not a printer.")
        else:
            print(f"Device at {ip} returned status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"{ip}: Conn Refused, Ignoring.")
    except requests.RequestException as e:
        print(f"Error connecting to {ip}: {e}")

# Reboot
def reboot_device(ip):
    try:
        response = requests.post(f"http://{ip}/cgi-bin/reboot", data={'reboot': 'Reboot'}, timeout=0.1)
        print(f"Reboot command sent to {ip}.")
    except requests.RequestException as e:
        #print(f"Error sending reboot command to {ip}: {e}")
        pass

def main():
    subnet = "192.168.0.0/24"
    exempt_ips = ["192.168.0.1"] # Don't need to scan firewall
    devices = scan_subnet(subnet)
    for device in devices:
        check_device(device, exempt_ips)

if __name__ == "__main__":
    main()
