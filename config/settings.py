import os
import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# VirusTotal API Key
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

# Database Configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "cyber_threats"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "yourpassword"),
    "host": os.getenv("DB_HOST", "localhost")
}
