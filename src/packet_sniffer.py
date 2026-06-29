from scapy.all import sniff

def process_packet(packet):
    """
    This function automatically handles every single packet 
    captured by your network card.
    """
    # Print a clean, one-line summary of the captured network traffic
    print(packet.summary())

print("=== Starting Live Packet Sniffer ===")
print("Press Ctrl+C to stop sniffing...")

# Capture exactly 10 packets and pass each one to our process_packet function
sniff(prn=process_packet, count=10)

print("=== Successfully captured 10 packets! ===")