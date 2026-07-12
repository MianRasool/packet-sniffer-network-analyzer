import os
import pandas as pd

# Dynamically resolve paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "captured_packets.csv")

def analyze_traffic():
    """Reads the captured packet database and prints terminal statistics."""
    print("=" * 65)
    print("      NETWORK TRAFFIC ANALYZER")
    print("=" * 65)

    if not os.path.exists(CSV_FILE_PATH):
        print(f"[!] Error: Could not find '{CSV_FILE_PATH}'.")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"[!] Error loading CSV: {e}")
        return

    if df.empty:
        print("[-] The database contains no packet records.")
        return

    # --- TERMINAL STATISTICS ---
    print(f"\n[*] Total Packets Analyzed: {len(df)}")

    print("\n[*] Protocol Breakdown:")
    print("-" * 25)
    print(df['Protocol'].value_counts().to_string())

    print("\n[*] Top 5 Most Active Source IPs:")
    print("-" * 35)
    print(df['Source_IP'].value_counts().head(5).to_string())

    print("\n[*] Top 5 Most Active Destination IPs:")
    print("-" * 38)
    print(df['Destination_IP'].value_counts().head(5).to_string())

    print("\n[*] Top 5 Most Used Destination Ports:")
    print("-" * 38)
    valid_ports = df[df['Destination_Port'] != "N/A"]
    if not valid_ports.empty:
        print(valid_ports['Destination_Port'].value_counts().head(5).to_string())
    else:
        print("No valid destination ports found.")
        

if __name__ == "__main__":
    analyze_traffic()