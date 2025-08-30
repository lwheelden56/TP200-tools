import socket
import time
import sys

def send_to_printer(ip_address, text, feed_lines=7):
    # Create a socket connection to the printer
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip_address, 9100))
        
        # Feed once to prevent cutoff
        sock.sendall(b'\n')

        # Send text
        sock.sendall(text.encode('utf-8'))
        
        # Line Feed
        for _ in range(feed_lines):
            sock.sendall(b'\n')
        
        # Cut the paper
        cut_command = b'\x1Bm'  # ESC m
        sock.sendall(cut_command)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 print-TP200.py <printer_ip> <text_to_print>")
        sys.exit(1)

    printer_ip = sys.argv[1]
    text_to_print = sys.argv[2]
    
    send_to_printer(printer_ip, text_to_print)
    print("Text sent")
