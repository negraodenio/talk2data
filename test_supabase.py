import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(r'c:\Users\denio\Documents\Denio\GenAIExercise\.env')

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"KEY: {key[:10]}...")

supabase = create_client(url, key)
res = supabase.table("equities").select("id", count="exact").execute()
print(f"Total Rows: {res.count}")

tesla = supabase.table("equities").select("*").ilike("name", "%Tesla%").execute()
print(f"Tesla Rows: {len(tesla.data)}")
if tesla.data:
    print(tesla.data[0])
