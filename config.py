import os
import sys
from dotenv import load_dotenv

load_dotenv()

PG_URI = os.getenv("POSTGRESQL_ADDON_URI")
if not PG_URI:
    print("❌ [Critical] POSTGRESQL_ADDON_URI not found in .env file.")
    sys.exit(1)

if "sslmode" not in PG_URI:
    PG_URI = f"{PG_URI}?sslmode=require"
    print("✅ [Config] Appended 'sslmode=require' to PG_URI.")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("❌ [Critical] MONGO_URI not found in .env file.")
    sys.exit(1)

print("✅ [Config] Environment variables loaded successfully.")