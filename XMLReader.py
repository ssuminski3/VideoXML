import xml.etree.ElementTree as ET
import videoCreator
import tags
import whisper_api
import os

def remove(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the index of </data>
    data_end_index = content.find('</data>')

    # Remove text after </data>
    if data_end_index != -1:
        content = content[:data_end_index + len('</data>')]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
def Read(name):
    api_key = ""
    lang = ""
    outputname = ""
    remove(name)
    root = ET.parse(name).getroot()
    for child in root:
        if(child.tag == "head"):
            api_key = "fNlaJ3bFn7PaAyhzymmkdDhjZjqHdql8W1kcoBzbK9MBd6hoPNg2o0uU"
            outputname = child.find("output").get("name")
            lang = child.find("lang").get("lang")
        if (child.tag == "body"):
            for count, data in enumerate(child):
               if(data.tag == "pexelimg"):
                   tags.pexelimg(data, count, api_key, lang)
               if(data.tag == "pexelvideo"):
                   tags.pexelvideo(data, count, api_key, lang)
               if (data.tag == "googleimg"):
                   tags.googleimg(data, count, lang)
            outputname = outputname.replace(':', '')
            videoCreator.merge_videos("./videos", "poloczony.mp4")
            videoCreator.speed_up_video("poloczony.mp4", "przyspieszony.mp4")
            whisper_api.extract_audio("przyspieszony.mp4", "a.mp3")
            c, e = whisper_api.getCaption("a.mp3")
            print(c, e)
            videoCreator.add_captions("przyspieszony.mp4", "napisy.mp4", c, e)
            videoCreator.connect_video_to_audio("napisy.mp4", "a.mp3", outputname+".mp4")
            if (os.path.exists("a.mp3")):
                os.remove("a.mp3")

    return outputname+".mp4"
