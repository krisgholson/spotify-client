import os
import httpx
from dotenv import load_dotenv

load_dotenv() 

SPOTIFY_API_URL = os.getenv("SPOTIFY_API_URL")
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_HEADERS = {"authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}

def get_episodes(show_id):
    print(f"get_episodes: {show_id}")
    r = httpx.get(f"{SPOTIFY_API_URL}/shows/{show_id}/episodes?limit=20&offset=0", headers=SPOTIFY_HEADERS)
    print(r.status_code)
    print(r.text)

def main():
    get_episodes("753FVUsio4Y6GjFvbGpvF0")

if __name__ == '__main__':
    main()