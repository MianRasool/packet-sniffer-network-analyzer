import os
import pandas as pd
import matplotlib.pyplot as plt

# Dynamically resolve paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "captured_packets.csv")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")

def generate_all_visualizations():
    print("=" * 65)
    print("      NETWORK TRAFFIC VISUALIZER (4 CHARTS)")
    print("=" * 65)

    if not os.path.exists(CSV_FILE_PATH):
        print(f"[!] Error: Could not find '{CSV_FILE_PATH}'.")
        print("    Please run the packet sniffer first to generate data.")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df.columns = df.columns.str.strip() # Sanitize headers
    except Exception as e:
        print(f"[!] Error loading CSV: {e}")
        return

    if df.empty:
        print("[-] The database contains no packet records.")
        return

    # Ensure the figures directory exists
    os.makedirs(FIGURES_DIR, exist_ok=True)
    print("[*] Generating 4 separate graphs...\n")

    # --- 1. PROTOCOL DISTRIBUTION BAR CHART ---
    print("[1] Creating Protocol Distribution Bar Chart...")
    plt.figure("Protocol Bar Chart", figsize=(8, 5))
    protocol_counts = df['Protocol'].value_counts()
    protocol_counts.plot(kind='bar', color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
    
    plt.title('Protocol Distribution (Bar Chart)', fontsize=14, pad=15)
    plt.xlabel('Transport Protocol', fontsize=12)
    plt.ylabel('Packet Count', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "1_protocol_bar.png"), dpi=300)

    # --- 2. PROTOCOL DISTRIBUTION PIE CHART ---
    print("[2] Creating Protocol Distribution Pie Chart...")
    plt.figure("Protocol Pie Chart", figsize=(7, 7))
    
    # autopct='%1.1f%%' adds the percentages directly onto the pie slices
    protocol_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, 
                         colors=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
    
    plt.title('Protocol Distribution (Pie Chart)', fontsize=14, pad=15)
    plt.ylabel('') # Hides the default y-label which looks messy on pie charts
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "2_protocol_pie.png"), dpi=300)

    # --- 3. TOP SOURCE IP ADDRESSES GRAPH ---
    print("[3] Creating Top Source IPs Bar Chart...")
    plt.figure("Top Source IPs", figsize=(10, 5))
    top_ips = df['Source_IP'].value_counts().head(5)
    top_ips.plot(kind='bar', color='#C44E52')
    
    plt.title('Top 5 Source IP Addresses', fontsize=14, pad=15)
    plt.xlabel('Source IP Address', fontsize=12)
    plt.ylabel('Packet Count', fontsize=12)
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "3_top_source_ips.png"), dpi=300)

    # --- 4. TOP DESTINATION PORTS GRAPH ---
    print("[4] Creating Top Destination Ports Bar Chart...")
    valid_ports = df[df['Destination_Port'] != "N/A"]
    
    if not valid_ports.empty:
        plt.figure("Top Destination Ports", figsize=(10, 5))
        top_ports = valid_ports['Destination_Port'].value_counts().head(5)
        top_ports.plot(kind='bar', color='#55A868')
        
        plt.title('Top 5 Destination Ports', fontsize=14, pad=15)
        plt.xlabel('Destination Port Number', fontsize=12)
        plt.ylabel('Packet Count', fontsize=12)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "4_top_dest_ports.png"), dpi=300)
    else:
        print("    -> Skipping Port Graph: No valid destination ports found (e.g., only ICMP traffic).")

    print("\n[*] All charts have been successfully generated and saved to the 'figures/' folder.")
    print("[*] Opening charts on screen now...")
    print("    (Note: If only one window appears, drag it to the side! The others are stacked underneath.)")
    
    # Displays all generated figures in separate windows simultaneously
    plt.show()

# --- ENGINE START ---
if __name__ == "__main__":
    generate_all_visualizations()