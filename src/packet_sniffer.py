import os
import csv
from datetime import datetime
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6

# Dynamically find your absolute project directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CSV_FILE_PATH = os.path.join(DATA_DIR, "captured_packets.csv")

def initialize_csv():
    """Ensures the target folder exists and creates a pristine spreadsheet file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp", "Protocol", "Source_IP", "Source_Port", 
                "Destination_IP", "Destination_Port", "Packet_Size_Bytes"
            ])
    print(f"[*] Absolute Path to your Spreadsheet Database:\n    -> {CSV_FILE_PATH}\n")

def process_packet(packet):
    """Processes traffic and forces an instant hard drive save."""
    src_ip, dst_ip = "Unknown", "Unknown"
    protocol = "Other"
    src_port, dst_port = "N/A", "N/A"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    packet_size = len(packet)

    # 1. Identify Network Layer (IPv4 or IPv6)
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
    elif packet.haslayer(IPv6):
        src_ip = packet[IPv6].src
        dst_ip = packet[IPv6].dst
    else:
        return # Skip background noise like ARP

    # 2. Identify Transport Layer (TCP or UDP)
    if packet.haslayer(TCP):
        protocol = "TCP"
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = "UDP"
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    # 3. Print out to the terminal
    print(f"[{protocol}] {src_ip}:{src_port} -> {dst_ip}:{dst_port} ({packet_size} B)")

    # 4. Save directly to the CSV file
    with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, protocol, src_ip, src_port, dst_ip, dst_port, packet_size])
        file.flush() # Force immediate save

# --- ENGINE START ---
initialize_csv()
print("=== Starting Persistent Logging Network Sniffer ===")
print("Capturing 100 packets so you have time to generate web traffic...\n")

sniff(prn=process_packet, count=100)

print("\n=== Sniffing Milestone Complete! ===")