import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(r'c:\Users\denio\Documents\Denio\GenAIExercise\.env')

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

entity = "Microsoft"
try:
    print(f"Testing ILIKE search for {entity}...")
    # TENTATIVA 1: O comando que está no chat.py
    res = supabase.table("equities").select("*").ilike("name", f"%{entity}%").order("market_cap", desc=True).limit(3).execute()
    print(f"Success! Found {len(res.data)} rows.")
except Exception as e:
    print("FAILED ATTEMPT 1")
    print(f"ERROR: {e}")
    # Se falhar, tentar TENTATIVA 2 sem o order
    try:
        print("\nTesting WITHOUT order...")
        res2 = supabase.table("equities").select("*").ilike("name", f"%{entity}%").limit(3).execute()
        print(f"Success without order! Found {len(res2.data)} rows.")
    except Exception as e2:
        print(f"FAILED ATTEMPT 2: {e2}")
