import os
import pandas as pd
import matplotlib.pyplot as plt

# Dynamically find your absolute project directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "captured_packets.csv")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "figures")

def analyze_traffic():
    print("=== Network Traffic Analyzer ===")
    
    if not os.path.exists(CSV_FILE_PATH):
        print("[-] Error: Could not find captured_packets.csv. Please run the sniffer first!")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except pd.errors.EmptyDataError:
        print("[-] The CSV file is empty. Please capture some traffic first.")
        return

    if df.empty:
        print("[-] No data found in the CSV.")
        return

    # --- TERMINAL STATISTICS ---
    total_packets = len(df)
    print(f"\n[*] Total Packets Analyzed: {total_packets}")

    print("\n[*] Protocol Breakdown:")
    print(df['Protocol'].value_counts().to_string())

    print("\n[*] Top 5 Most Active Source IPs:")
    print(df['Source_IP'].value_counts().head(5).to_string())

    # --- CHART 1: PROTOCOL DISTRIBUTION ---
    print("\n[*] Generating Protocol Chart...")
    plt.figure(figsize=(8, 5))
    protocol_counts = df['Protocol'].value_counts()
    protocol_counts.plot(kind='bar', color=['#4C72B0', '#DD8452', '#55A868'])
    
    plt.title('Network Traffic by Protocol')
    plt.xlabel('Transport Protocol')
    plt.ylabel('Number of Packets Captured')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    os.makedirs(FIGURES_DIR, exist_ok=True)
    protocol_fig_path = os.path.join(FIGURES_DIR, "protocol_distribution.png")
    plt.savefig(protocol_fig_path)
    print(f"[*] Chart 1 saved to: {protocol_fig_path}")
    plt.show() # This will pause the script and show the first graph

    # --- CHART 2: TOP IP ADDRESSES ---
    print("[*] Generating Top IP Addresses Chart...")
    plt.figure(figsize=(10, 5))
    
    # Isolate only the top 5 IPs so the graph isn't too crowded
    top_ips = df['Source_IP'].value_counts().head(5)
    top_ips.plot(kind='bar', color='#C44E52')
    
    plt.title('Top 5 Most Active Source IP Addresses')
    plt.xlabel('Source IP Address')
    plt.ylabel('Packet Count')
    plt.xticks(rotation=15) # Slightly tilt the IPs so they don't overlap
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    ip_fig_path = os.path.join(FIGURES_DIR, "top_source_ips.png")
    plt.savefig(ip_fig_path)
    print(f"[*] Chart 2 saved to: {ip_fig_path}")
    plt.show() # This will show the second graph

# --- ENGINE START ---
if __name__ == "__main__":
    analyze_traffic()