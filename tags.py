import os

import get_pexel_api
import get_google_media
import videoCreator


def pexelimg(data, count, api_key, lang):
    img = get_pexel_api.download_pexels(data.get("keyword"), "images", str(count), api_key)
    if 'lang' in data.attrib:
        lang = data.get("lang")
    audio = get_google_media.TextToSpeech(data.text, lang, str(count))
    videoCreator.connect_image_to_audio(img, audio, "./videos/" + str(count) + ".mp4")

def pexelvideo(data, count, api_key, lang):
    video = get_pexel_api.download_video_pexels(data.get("keyword"), "0"+str(count)+".mp4", api_key)
    if 'lang' in data.attrib:
        lang = data.get("lang")
    audio = get_google_media.TextToSpeech(data.text, lang, str(count))
    videoCreator.connect_video_to_audio(video, audio, "./videos/" + str(count) + ".mp4")

def googleimg(data, count, lang):
    img = get_google_media.DownloadImageGoogle(data.get("keyword"), "images", str(count))
    if 'lang' in data.attrib:
        lang = data.get("lang")
    audio = get_google_media.TextToSpeech(data.text, lang, str(count))
    from PIL import Image

    # Open the input image
    input_image_path = img
    image = Image.open(input_image_path)

    # Get the original dimensions
    original_width, original_height = image.size

    # Calculate the new dimensions (doubling the size)
    new_width = original_width * 2
    new_height = original_height * 2

    # Resize the image to the new dimensions
    resized_image = image.resize((new_width, new_height))

    # Save the resized image
    output_image_path = img
    resized_image.save(output_image_path)

    # Close the original and resized images
    image.close()
    resized_image.close()

    print(f"Image resized to {new_width}x{new_height} and saved as {output_image_path}")
    videoCreator.combine_image_audio_and_remove(img, audio, "./videos/" + str(count) + ".mp4")
