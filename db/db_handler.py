# database_client.py
import psycopg2

# PostgreSQL connection details
DB_CONFIG = {
    "dbname": "cyber_threats",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost"
}

def insert_threat_data(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute("""
            INSERT INTO threats (source_ip, asn, country, reputation, threat_type, severity, description, malicious, suspicious, undetected, harmless)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["ip"],
            data["asn"],
            data["country"],
            data["reputation"],
            data["threat_type"],
            data["severity"],
            data["description"],
            data["malicious"],
            data["suspicious"],
            data["undetected"],
            data["harmless"]
        ))

        conn.commit()
        print(f"Data for IP {data['ip']} inserted successfully.")

    except Exception as e:
        print("Failed to insert data into the database:", e)
    finally:
        cursor.close()
        conn.close()
