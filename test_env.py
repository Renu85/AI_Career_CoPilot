from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read environment variables
database_url = os.getenv("DATABASE_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")

print("DATABASE_URL =", database_url)
print("OPENAI_API_KEY =", openai_api_key)