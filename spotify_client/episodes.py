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

def daily_gospel_exegesis_matthew():
    
    show_dir = f"{DATA_DIR}/{DAILY_GOSPEL_EXEGESIS}"
    json_pattern = os.path.join(show_dir, "*.json")
    file_list = glob.glob(json_pattern)

    print(len(file_list))

    episodes = []
    for file in file_list:
        with open(file, "r") as f:
            episodes.append(json.load(f))

    df = pd.json_normalize(episodes)
    df["book_chapter_verse"] = df["name"].apply(daily_gospel_exegesis_book_chapter_verse_from_name)
    df["book"] = df["book_chapter_verse"].apply(daily_gospel_exegesis_book_from_book_chapter_verse)
    df["chapter"] = df["book_chapter_verse"].apply(daily_gospel_exegesis_chapter_from_book_chapter_verse)
    df = df[["Matt" in x for x in df["book"]]]
    df = df.sort_values(by=["book", "chapter"])
            
    # view the updated DataFrame
    print(df.shape[0])
    print(df[["book", "chapter"]].head(10)) 
    df.to_csv("daily_gospel_exegesis.csv")    

def daily_gospel_exegesis_book_from_book_chapter_verse(book_chapter_verse):
    if ":" not in book_chapter_verse:
        return book_chapter_verse
    array = book_chapter_verse.split(" ")
    return array[0]

def daily_gospel_exegesis_chapter_from_book_chapter_verse(book_chapter_verse):
    if ":" not in book_chapter_verse:
        return None
    array = book_chapter_verse.split(" ")
    size = len(array)
    if size < 2:
        return None
    elif size >= 2:
        chapter_verse_array = array[1].split(":")
        print(f"chapter_verse_array: {chapter_verse_array} | {book_chapter_verse}")
        return int(chapter_verse_array[0])

def daily_gospel_exegesis_book_chapter_verse_from_name(name):
    array = name.split(" - ")
    size = len(array)
    if size < 2:
        return array[0]
    elif size == 2:
        return array[1]
    elif size > 2:
        return array[1] + "-" + array[2]

def main():
    # download_all_episode_metadata(DAILY_GOSPEL_EXEGESIS)
    daily_gospel_exegesis_matthew()

if __name__ == '__main__':
    main()