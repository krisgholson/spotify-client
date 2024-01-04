import glob
import httpx
import json
import os
import pandas as pd
import time
from dotenv import load_dotenv

pd.set_option("display.max_columns", None)
load_dotenv() 

DATA_DIR = os.getenv("DATA_DIR")
SPOTIFY_API_URL = os.getenv("SPOTIFY_API_URL")
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_HEADERS = {"authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}

DAILY_GOSPEL_EXEGESIS = os.getenv("DAILY_GOSPEL_EXEGESIS")
BIBLE_IN_A_YEAR = os.getenv("BIBLE_IN_A_YEAR")

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

def episode_report(show_id):
    
    show_dir = f"{DATA_DIR}/{show_id}"
    json_pattern = os.path.join(show_dir, "*.json")
    file_list = glob.glob(json_pattern)

    print(len(file_list))

    episodes = [] # an empty list to store the data frames
    for file in file_list:
        with open(file, "r") as f:
            episodes.append(json.load(f))

    df = pd.json_normalize(episodes)
    df = df.sort_values(by="release_date")
    print(df.release_date.to_string(index=False))



def main():
    # download_all_episode_metadata(DAILY_GOSPEL_EXEGESIS)
    episode_report(BIBLE_IN_A_YEAR)

if __name__ == '__main__':
    main()