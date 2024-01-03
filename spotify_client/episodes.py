import os
import httpx
import time
from dotenv import load_dotenv

load_dotenv() 

SPOTIFY_API_URL = os.getenv("SPOTIFY_API_URL")
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_HEADERS = {"authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}

def get_all(url, items=[]):
    r = httpx.get(url, headers=SPOTIFY_HEADERS)
    resp = r.json()
    next_url = resp["next"]
    resp_items = resp.get("items", [])
    items = items + resp_items
    if next_url:
        time.sleep(.300)
        return get_all(next_url, items)
    else:
        return items

def get_all_episodes(show_id):
    url = f"{SPOTIFY_API_URL}/shows/{show_id}/episodes?limit=20&offset=0"
    episodes = get_all(url)
    print(len(episodes))

def main():
    get_all_episodes("753FVUsio4Y6GjFvbGpvF0")

if __name__ == '__main__':
    main()