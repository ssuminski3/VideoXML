import requests
from pexels_api import API
import tqdm

import argparse
import requests
from pathlib import Path


import argparse
import json
import os
import time

import requests
import tqdm
from pexels_api import API

def download_pexels(query, image_path, name):
    PAGE_LIMIT = 10
    RESULTS_PER_PAGE = 10

    PEXELS_API_KEY = "YOUR_API_KEY"
    api = API(PEXELS_API_KEY)
    photos_dict = {}
    page = 1
    counter = 0

    # Step 1: Getting urls and meta information

    api.search(query, page=0, results_per_page=RESULTS_PER_PAGE)
    photos = api.get_entries()
    for photo in tqdm.tqdm(photos):
        photos_dict[photo.id] = vars(photo)['_Photo__photo']
        counter += 1
        if not api.has_next_page:
            return

    print(f"Finishing at page: {page}")
    print(f"Images were processed: {counter}")
    # Step 2: Downloading
    PATH = './'
    RESOLUTION = 'original'

    if photos_dict:
        os.makedirs(PATH, exist_ok=True)

        # Saving dict
        with open(os.path.join(PATH, f'{query}.json'), 'w') as fout:
            json.dump(photos_dict, fout)

        for val in tqdm.tqdm(photos_dict.values()):
            url = val['src'][RESOLUTION]

            if not os.path.isfile(image_path):
                response = requests.get(url, stream=True)
                with open(image_path+"/"+name+".png", 'wb') as file:
                    file.write(response.content)
            else:
                # ignore if already downloaded
                print(f"File {image_path} exists")


def download_video_pexels(query, fname, root_dir="./"):
    # Define Pexels API URL for videos
    api_url = "https://api.pexels.com/videos/search"

    # Set your Pexels API key here
    api_key = "YOUR_API_KEY"

    # Define parameters for the API request
    params = {
        "query": query,
        "per_page": 1  # Set to 1 to download only one video
    }

    headers = {
        "Authorization": api_key
    }

    # Make the API request
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Extract the download URL of the first video (if available)
        if data.get("videos"):
            download_url = data["videos"][0].get("video_files", [])[0].get("link")
            if download_url:
                fpath = Path(root_dir, fname)

                # Check if the file already exists
                if fpath.exists():
                    print("Exists:", fpath)
                else:
                    # Download the video
                    response = requests.get(download_url)
                    with open(str(fpath), "wb") as file:
                        file.write(response.content)
                    print("Downloaded:", fpath)
            else:
                print("No download URL found for the video.")
        else:
            print("No videos found for the query.")
    else:
        print(f"Error {response.status_code}: {response.text}")
