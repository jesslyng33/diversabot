import os
from db.supabase import create_client
from dotenv import load_dotenv

# load environemnt variables 
load_dotenv('.env')

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)