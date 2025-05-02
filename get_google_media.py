import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os


def DownloadImageGoogle(search_term, path, name):
    url = rf'https://www.google.no/search?q={search_term}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    thumbnails = []

    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')

        if link and link.startswith("https://"):
            thumbnails.append(link)
            pass

        pass
    download_image(link, path+"/"+name+".png")

    return os.path.join(path, name + ".png")


def download_image(url, save_path):

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the file in binary write mode and save the image data
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully and saved to {save_path}")
            from PIL import Image

            # Open the image file
            image = Image.open(save_path)

            # Define the new size (width, height)
            new_size = (image.width*5, image.height*5)

            # Resize the image
            resized_image = image.resize(new_size)

            # Save the resized image
            resized_image.save(save_path)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

def TextToSpeech(txt, language, output_base):
    tts = gTTS(text=txt, lang=language)
    tts.save(output_base)

    return output_base