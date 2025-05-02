from pathlib import Path
import json
import os
import requests
import tqdm
from pexels_api import API
import sys

#bez zmiennych
apis = [
    'fNlaJ3bFn7PaAyhzymmkdDhjZjqHdql8W1kcoBzbK9MBd6hoPNg2o0uU',
    'MLVnoDSTENK5piJqkOqsOf8Vx6frv2NmStAauRBgulcxlbuHJXRGVCBq',
    'ZhdEcvk6QYkm6U2naDIFFm3PT5XWXvARtfkUHDUCxq58UEZq50VHxmNO',
    'DUIXF5jZIUAKVSunRvqhielNKWWDD0254XVUuZxuQnbk6lkj5WwYnppY',
    'Pc4TnfktSJ79IWiAJJNwmKBIgjQYQXyndyAZDlapaSQrV7LcmtMtleeP',
    'kuhnDLm9OlkYWEgJzqXKSvWGDwxbagNb3ypna6IENXXGF0SsgJEULPe9',
    'mSCBF3FgrVOejRaQQCZ4Ujwe8L5bnxaPs1lFKTPO5iXK9aixO3hskWRM',
    'fFXBjey8R8qRcBNnEMuViHlsAmnWF40bbeRlwQaQU38Qa0dGhYqEEFY5',
    'iuiyaKvJtiKxrvTtOjMtVcd0ouTqgwFT5Fwbdb5NTlE5BSmC8wA3bjyE',
    'qm7Rt2nBecme7sL2RX3AHtTNxlAqTqhYU4RQyhh03V8zIsYRfaQMzyMQ',
    '0i588Ek1ijBG50O9aPuKcJEpAh1YbRgABwYNa3Sk5gkAVJYxAqeLuvgb'
]

index = 0
n = 0
def download_pexels(query, image_path, name, PEXELS_API_KEY, n1 = n):
    PAGE_LIMIT = 10
    RESULTS_PER_PAGE = 10
    global index
    while index < len(apis):
        api = API(apis[index])
        photos_dict = {}
        page = 1
        counter = 0

        try:
            # Step 1: Getting urls and meta information
            api.search(query, page=0, results_per_page=RESULTS_PER_PAGE)
            photos = api.get_entries()
            for photo in tqdm.tqdm(photos):
                photos_dict[photo.id] = vars(photo)['_Photo__photo']
                counter += 1
                if not api.has_next_page:
                    break

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
                        with open(image_path+"\\"+name+".png", 'wb') as file:
                            file.write(response.content)
                        return os.path.join(image_path, name + ".png")
                    else:
                        # ignore if already downloaded
                        print(f"File {image_path} exists")
                        return "File {image_path} exists"

        except Exception as e:
            print(f"Error: {e}")
            index += 1  # Increment index on error

    sys.exit()
    print("All API keys failed. Could not download.")
def download_video_pexels(query, fname, api_key, root_dir="./"):
    global n
    # Define Pexels API URL for videos
    api_url = "https://api.pexels.com/videos/search"

    # Initialize index and set the initial API key
    index = 0
    headers = {"Authorization": apis[index]}

    # Define parameters for the API request
    params = {"query": query, "per_page": 1}  # Set to 1 to download only one video

    while index < len(apis):
        try:
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
                            return "exists"
                        else:
                            # Download the video
                            response = requests.get(download_url)
                            with open(str(fpath), "wb") as file:
                                file.write(response.content)
                            print("Downloaded:", fpath)
                            return os.path.join(fpath)
                    else:
                        print("No download URL found for the video.")
                else:
                    print("No videos found for the query.")
                    n += 1
                    print(query[(n % len(query))] + query[(n + 1) % len(query)])
                    if n > 10:
                        n = 0
                        return download_video_pexels("whatever", fname, api_key, root_dir)
                    return download_video_pexels(query[(n % len(query))] + query[(n + 1) % len(query)],
                                                 fname, api_key, root_dir)


            else:
                print(f"Error {response.status_code}: {response.text}")

            # Increment index on error
            index += 1

            # Update headers with the next API key
            if index < len(apis):
                headers["Authorization"] = apis[index]

        except Exception as e:
            print(f"Error: {e}")
            index += 1  # Increment index on error

    print("All API keys failed. Could not download.")
    sys.exit()
    return ""
