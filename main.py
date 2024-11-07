# Description: This script demonstrates how to query VirusTotal's API for information about an IP address.

import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

from config.settings import VIRUSTOTAL_API_KEY, DB_CONFIG
import requests
import json
import psycopg2

ip_address = "8.8.8.8"  # Replace with the IP you want to check
url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"

headers = {
    "accept": "application/json",
    "x-apikey": VIRUSTOTAL_API_KEY
}

# Make the request to VirusTotal API
response = requests.get(url, headers=headers)

# Check if the response was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract the necessary information
    ip_info = {
        "ip": data['data']['id'],
        "asn": data['data']['attributes'].get('asn'),
        "country": data['data']['attributes'].get('country'),
        "reputation": data['data']['attributes'].get('reputation'),
        "malicious": data['data']['attributes']['last_analysis_stats'].get("malicious", 0),
        "suspicious": data['data']['attributes']['last_analysis_stats'].get("suspicious", 0),
        "undetected": data['data']['attributes']['last_analysis_stats'].get("undetected", 0),
        "harmless": data['data']['attributes']['last_analysis_stats'].get("harmless", 0)
    }

    # Save the extracted data to a JSON file
    with open("ip_info.json", "w") as json_file:
        json.dump(ip_info, json_file, indent=4)
    print("Data saved to ip_info.json")

    # Insert the data into the PostgreSQL database
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"]
        )
        cursor = conn.cursor()

        # Prepare and execute the insert query
        cursor.execute("""
            INSERT INTO threats (ip, asn, country, reputation, malicious, suspicious, undetected, harmless)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ip_info["ip"],
            ip_info["asn"],
            ip_info["country"],
            ip_info["reputation"],
            ip_info["malicious"],
            ip_info["suspicious"],
            ip_info["undetected"],
            ip_info["harmless"]
        ))

        # Commit the transaction
        conn.commit()
        print("Data inserted into the database")

    except Exception as e:
        print("Failed to insert data into the database:", e)
    finally:
        # Close the database connection if open
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
