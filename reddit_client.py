import os
import praw
from dotenv import load_dotenv

# --- To run on your device, create a .env folder in the main folder ---
#   CLIENT_ID=your_reddit_client_id
#   CLIENT_SECRET=your_reddit_client_secret
#   USER_AGENT=your_script_name_by_/u/your_username

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

# --- TEST LOGIN CREDENTIALS ---
""" 

print(client_id)
print(client_secret)
print(user_agent)

"""
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)
def fetch_threads(product, limit=50):
    query = f'"{product}"'
    return reddit.subreddit("all").search(query, sort="relevance", limit=limit)