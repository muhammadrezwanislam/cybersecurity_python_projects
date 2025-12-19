import psutil
import ipaddress
import pandas as pd

external_ips = set()  # Keep this for VirusTotal checking
connection_details = [] 
# NEW: Store full connection infoconnections = psutil.net_connections(kind='all')
connections = psutil.net_connections(kind='all')

for conn in connections:
    if conn.status == 'ESTABLISHED' and conn.raddr:
        remote_ip = conn.raddr[0]
        ip_obj = ipaddress.ip_address(remote_ip)
        
        if not ip_obj.is_loopback and not ip_obj.is_private:
            external_ips.add(remote_ip)
            
            # Get process info
            try:
                process_name = psutil.Process(conn.pid).name()
            except:
                process_name = "Unknown"
            
            # Create a dictionary for this connection
            conn_info = {
                'remote_ip': remote_ip,
                'remote_port': conn.raddr[1],  # YOU FILL THIS
                'pid': conn.pid,          # YOU FILL THIS
                'process_name': process_name
            }
            
            connection_details.append(conn_info)

    
import requests
import time

# Your API key (keep this secret!)
API_KEY = ''


    
# Step 2: Check each IP with VirusTotal
vt_results = []

for idx, ip in enumerate(external_ips, 1):
    print(f"Checking {idx}/{len(external_ips)}: {ip}...")
    
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {'x-apikey': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            attributes = data['data']['attributes']
            analysis_stats = attributes.get('last_analysis_stats', {})
            
            ip_info = {
                'IP': ip,
                'Country': attributes.get('country', 'Unknown'),
                'AS_Owner': attributes.get('as_owner', 'Unknown'),
                'ASN': attributes.get('asn', 'Unknown'),
                'Reputation': attributes.get('reputation', 0),
                'Malicious': analysis_stats.get('malicious', 0),
                'Suspicious': analysis_stats.get('suspicious', 0),
                'Harmless': analysis_stats.get('harmless', 0),
                'Undetected': analysis_stats.get('undetected', 0)
            }
            
            vt_results.append(ip_info)
            
        elif response.status_code == 404:
            print(f"  ✗ Not found in VirusTotal")
        elif response.status_code == 429:
            print(f"  ⚠ Rate limit! Waiting 60 seconds...")
            time.sleep(60)
        else:
            print(f"  ✗ Error: {response.status_code}")
            
    except Exception as e:
        print(f"  ✗ Exception: {e}")
    
    # Rate limiting: 4 requests per minute = wait 15 seconds
    if idx < len(external_ips):  # Don't wait after last one
        time.sleep(15)

# After collecting connection_details and vt_results
df_connections = pd.DataFrame(connection_details)
df_vt = pd.DataFrame(vt_results)

# Merge them on IP address
df_final = df_connections.merge(df_vt, left_on='remote_ip', right_on='IP', how='left')


print("\n" + "="*80)
print("VIRUSTOTAL ANALYSIS REPORT")
print("="*80)
print(df_final.to_string(index=False))

# Step 4: Flag suspicious IPs
suspicious = df_final[(df_final['Malicious'] > 0) | (df_final['Suspicious'] > 0)]

if len(suspicious) > 0:
    print("\n" + "="*80)
    print("⚠️  SUSPICIOUS IPs DETECTED!")
    print("="*80)
    print(suspicious.to_string(index=False))
else:
    print("\n✓ No suspicious IPs detected")

# Step 5: Save results
df_final.to_csv('network_threat_analysis.csv', index=False)
df_final.to_excel('network_threat_analysis.xlsx', index=False)
print(f"\n✓ Results saved to network_threat_analysis.csv and .xlsx")
    