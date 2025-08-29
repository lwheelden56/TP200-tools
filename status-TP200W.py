# Check Status of All printers on Network

import requests, time
from scapy.all import ARP, Ether, srp
import re

# Dictionary to map MAC addresses to device names
mac_name_dict = {
    "00:13:41:xx:xx:xx": "Printer 1",
}

# Scan Subnet for devices
def scan_subnet(subnet):
    print(f"Scanning subnet: {subnet}")
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append((received.psrc, received.hwsrc))  # Store (IP, MAC) pairs
    print(len(devices), "Devices Found")
    return devices

def check_device(ip, mac, exempt_ips, found_macs, found_yes):
    if ip in exempt_ips:
        return

    # Normalize the MAC address
    normalized_mac = mac.lower().strip()
    found_macs.add(normalized_mac)  # Track found MAC addresses

    try:
        response = requests.get(f"http://{ip}/prn_stat.asp", timeout=2)
        if response.status_code == 200:
            # Check if the response contains the specific HTML to identify the device
            if re.search(r'<TITLE>Printer Status</TITLE>', response.text):
                # Check for "YES" in the printer status table
                if re.search(r'<TD>(.*?)</TD>\s*<TD><font color=red>Yes</font></TD>', response.text):
                    # Extract the specific status messages
                    matches = re.findall(r'<TD>(.*?)</TD>\s*<TD><font color=red>Yes</font></TD>', response.text)
                    device_name = mac_name_dict.get(normalized_mac, ip)  # Get name from dict or use IP
                    for match in matches:
                        clean_match = match.replace('&nbsp;', '').strip()  # Remove &nbsp; and strip whitespace
                        print(f"\033[1m{device_name}: {clean_match} is YES.\033[0m")
                    found_yes[0] = True  # Set flag to True if matches are found
                else:
                    # Uncomment if you want to print when the printer is OK
                    # device_name = mac_name_dict.get(normalized_mac, ip)  # Get name from dict or use IP
                    # print(f"{device_name}: PRINTER OK")
                    pass
            else:
                print(f"{ip} is not a printer.")
        else:
            print(f"Device at {ip} returned status code: {response.status_code}")
    except requests.ConnectionError:
        # print(f"{ip}: Conn Refused, Ignoring.")
        pass
    except requests.RequestException as e:
        print(f"Error connecting to {ip}: {e}")

def main():
    subnet = "192.168.0.0/22"
    exempt_ips = ["192.168.0.1"]  # Don't need to scan firewall
    devices = scan_subnet(subnet)
    
    found_macs = set()  # Set to track found MAC addresses
    found_yes = [False]  # Use a list to allow modification within check_device
    for device in devices:
        ip, mac = device
        check_device(ip, mac, exempt_ips, found_macs, found_yes)

    if not found_yes[0]:
        print("\nALL OK")
        time.sleep(0.5)

    # List names of devices in the dict that were not found. MAY NOT ALWAYS BE ACCURATE
    not_found_names = [mac_name_dict[mac] for mac in mac_name_dict.keys() if mac.lower() not in found_macs]
    if not_found_names:
        print("\nDevices not found in the scan:")
        for name in not_found_names:
            print(name)

if __name__ == "__main__":
    main()