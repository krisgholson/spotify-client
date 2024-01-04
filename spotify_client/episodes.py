import httpx
import json
import os
import time
from dotenv import load_dotenv

load_dotenv() 

DATA_DIR = os.getenv("DATA_DIR")
SPOTIFY_API_URL = os.getenv("SPOTIFY_API_URL")
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_HEADERS = {"authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}

def get_all(url, items=[]):
    print(url)
    r = httpx.get(url, headers=SPOTIFY_HEADERS)
    r.raise_for_status()
    resp = r.json()
    next_url = resp["next"]
    resp_items = resp.get("items", [])
    if len(resp_items):
        # append the non-null elements
        items += list(filter(lambda x: x is not None, resp_items))
    if next_url:
    # if False:
        time.sleep(1)
        return get_all(next_url, items)
    else:
        return items

def get_all_episodes(show_id):
    url = f"{SPOTIFY_API_URL}/shows/{show_id}/episodes?limit=20&offset=0"
    return get_all(url)

def download_all_episode_metadata(show_id):
    episodes = get_all_episodes(show_id)   
    show_dir = f"{DATA_DIR}/{show_id}"

    if not os.path.exists(show_dir):
        os.makedirs(show_dir)    
    print(f"write {len(episodes)} episodes to {show_dir}") 

    for e in episodes:
        id = e.get("id")
        with open(f"{show_dir}/{id}.json", "w") as f:
            json.dump(e, f, indent=4)

def main():
    daily_gospel_exegesis = "753FVUsio4Y6GjFvbGpvF0"
    bible_in_a_year = "4Pppt42NPK2XzKwNIoW7BR"
    download_all_episode_metadata(bible_in_a_year)

if __name__ == '__main__':
    main()