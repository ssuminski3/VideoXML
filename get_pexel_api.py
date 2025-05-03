from pathlib import Path
import json
import os
import requests
from pexels_api import API
import sys

def download_pexels(query: str, image_path: str, name: str, api_key) -> str:
    """
    Downloads the first image matching the query from Pexels.

    Args:
        query (str): Search query.
        image_path (str): Directory path to save the image.
        name (str): Filename (without extension) to save as.
        api_key (str): Pexels API key.

    Returns:
        str: Full path to the downloaded image, or a message if it exists.
    """
    api = API(api_key)
    RES_PER_PAGE = 10

    try:
        api.search(query, page=1, results_per_page=RES_PER_PAGE)
        photos = api.get_entries()

        if not photos:
            return f"No images found for query '{query}'"

        # Take the first photo
        photo = photos[0]
        photo_info = vars(photo)['_Photo__photo']
        src_url = photo_info['src']['original']

        os.makedirs(image_path, exist_ok=True)
        output_file = os.path.join(image_path, f"{name}.png")

        if Path(output_file).exists():
            return f"File already exists: {output_file}"

        response = requests.get(src_url, stream=True)
        response.raise_for_status()

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return output_file

    except Exception as e:
        print(f"Error downloading image: {e}")
        sys.exit(1)


def download_video_pexels(query: str, fname: str, api_key, root_dir: str = "./") -> str:
    """
    Downloads the first video matching the query from Pexels.

    Args:
        query (str): Search query.
        fname (str): Filename (including extension) to save as.
        api_key (str): Pexels API key.
        root_dir (str): Directory to save the video.

    Returns:
        str: Full path to the downloaded video, or message if exists/not found.
    """
    api_url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 1}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data.get('videos'):
            return f"No videos found for query '{query}'"

        video_files = data['videos'][0].get('video_files', [])
        if not video_files:
            return "No downloadable video files available."

        download_url = video_files[0].get('link')
        if not download_url:
            return "No download URL found for the video."

        os.makedirs(root_dir, exist_ok=True)
        output_file = Path(root_dir) / fname

        if output_file.exists():
            return f"File already exists: {output_file}"

        vid_resp = requests.get(download_url, stream=True)
        vid_resp.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in vid_resp.iter_content(1024):
                f.write(chunk)

        return str(output_file)

    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)
