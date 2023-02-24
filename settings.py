import os

from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')
