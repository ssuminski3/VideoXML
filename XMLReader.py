import xml.etree.ElementTree as ET
import videoCreator
import tags
import whisper_api
import os

def read_cleaned_xml_string(file_path):
    """Reads and trims XML content up to </data>."""
    with open(file_path, 'r') as file:
        content = file.read()

    data_end_index = content.find('</data>')
    if data_end_index != -1:
        content = content[:data_end_index + len('</data>')]

    return content

def process_xml_content(xml_string, speed_up=False):
    """Parses and processes the XML content."""
    api_key = ""
    lang = ""
    outputname = ""

    root = ET.fromstring(xml_string)

    for child in root:
        if child.tag == "head":
            api_key = child.find("pexel").get("key")
            outputname = child.find("output").get("name")
            lang = child.find("lang").get("lang")
        elif child.tag == "body":
            for count, data in enumerate(child):
                if data.tag == "pexelimg":
                    tags.pexelimg(data, count, api_key, lang)
                elif data.tag == "pexelvideo":
                    tags.pexelvideo(data, count, api_key, lang)
                elif data.tag == "googleimg":
                    tags.googleimg(data, count, lang)

            outputname = outputname.replace(':', '')
            os.makedirs('./videos', exist_ok=True)
            print(os.listdir("./videos"))
            videoCreator.merge_videos("./videos", "poloczony.mp4")

            input_video = "poloczony.mp4"
            if speed_up:
                videoCreator.speed_up_video("poloczony.mp4", "przyspieszony.mp4")
                input_video = "przyspieszony.mp4"

            whisper_api.extract_audio(input_video, "a.mp3")
            c, e = whisper_api.getCaption("a.mp3")
            print(c, e)
            videoCreator.add_captions(input_video, "napisy.mp4", c, e)
            videoCreator.connect_video_to_audio("napisy.mp4", "a.mp3", outputname + ".mp4")

            if os.path.exists("a.mp3"):
                os.remove("a.mp3")

    return outputname + ".mp4"

def read_and_process(file_path, speed_up=True):
    """Reads XML from file and processes it."""
    xml_string = read_cleaned_xml_string(file_path)
    return process_xml_content(xml_string, speed_up)
