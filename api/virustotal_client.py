# virustotal_client.py
import requests

# Your VirusTotal API key
API_KEY = 'YOUR_VIRUSTOTAL_API_KEY'

def fetch_virustotal_data(ip_address):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {
        "x-apikey": API_KEY
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        threat_stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        severity = "High" if threat_stats.get("malicious", 0) > 0 else "Low"
        description = f"Malicious: {threat_stats.get('malicious', 0)}, Suspicious: {threat_stats.get('suspicious', 0)}"
        
        return {
            "ip": ip_address,
            "asn": data.get('data', {}).get('attributes', {}).get('asn'),
            "country": data.get('data', {}).get('attributes', {}).get('country'),
            "reputation": data.get('data', {}).get('attributes', {}).get('reputation'),
            "threat_type": "Malware",
            "severity": severity,
            "description": description,
            "malicious": threat_stats.get("malicious", 0),
            "suspicious": threat_stats.get("suspicious", 0),
            "undetected": threat_stats.get("undetected", 0),
            "harmless": threat_stats.get("harmless", 0)
        }
    else:
        print(f"Error fetching data for IP {ip_address}: {response.status_code}")
        return None
