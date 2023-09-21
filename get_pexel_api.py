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

    PEXELS_API_KEY = "fNlaJ3bFn7PaAyhzymmkdDhjZjqHdql8W1kcoBzbK9MBd6hoPNg2o0uU"
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


