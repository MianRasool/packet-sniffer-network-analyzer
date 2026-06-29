from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

def process_packet(packet):
    """
    This advanced callback function inspects each packet, checks if it's an 
    IPv4 packet, filters its protocol layer, and extracts key data fields.
    """
    # 1. We only want to look at packets containing an IP layer (IPv4)
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        
        # Pull out the core network layer information
        src_ip = ip_layer.src          # Source IP Address
        dst_ip = ip_layer.dst          # Destination IP Address
        packet_size = len(packet)      # Packet length/size
        
        # Set up default placeholders for the transport layer fields
        protocol = "Other"
        src_port = "N/A"
        dst_port = "N/A"

        # 2. Check if the transport layer is using TCP
        if packet.haslayer(TCP):
            protocol = "TCP"
            src_port = packet[TCP].sport    # Source Port
            dst_port = packet[TCP].dport    # Destination Port
            
        # 3. Check if the transport layer instead uses UDP
        elif packet.haslayer(UDP):
            protocol = "UDP"
            src_port = packet[UDP].sport    # Source Port
            dst_port = packet[UDP].dport    # Destination Port
            
        # 4. Print the extracted information cleanly on the console screen
        print("-" * 60)
        print(f"Protocol: {protocol:<6} | Size: {packet_size:<5} bytes")
        print(f"Source Connection:      {src_ip}:{src_port}")
        print(f"Destination Connection: {dst_ip}:{dst_port}")

print("=== Starting Advanced Info Extraction Sniffer ===")
print("Listening for incoming traffic... (Capturing 5 sample packets)")

# Sniff 5 IPv4 network packets to inspect our formatting
sniff(prn=process_packet, count=5)

print("-" * 60)
print("=== Extraction Complete ===")