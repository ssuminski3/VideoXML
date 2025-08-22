# 🎬 Auto Video Generator from XML

This Python project turns structured XML into narrated, captioned videos by combining media (from Pexels or Google), text-to-speech, and Whisper-generated subtitles. It supports batch file processing and live XML string input.

## 📦 Features

🔍 Fetches images/videos from Pexels or Google Images

🗣 Converts text to speech using Google's TTS

🎥 Combines media and audio into short video clips

🎞 Merges clips into one final video

⏩ Optional video speed-up

💬 Adds subtitles using Whisper

📁 Supports folder-based XML batch processing

📝 Accepts XML input as a string

🧾 Example XML Format
```xml
<data>
  <head>
    <pexel key="YOUR_PEXELS_API_KEY"/>
    <lang lang="en"/>
    <output name="My Final Video"/>
  </head>
  <body>
    <pexelimg keyword="forest">A peaceful forest scene</pexelimg>
    <pexelvideo keyword="city">Busy streets of the city</pexelvideo>
    <googleimg keyword="mountain">Snowy mountain peaks</googleimg>
  </body>
</data>
```
▶️ How to Use

You can run the script in two modes:

📁 Option 1: Process All XML Files in a Folder

Place your XML files in the /XMLS folder.

Run:
```console
python main.py
```

When prompted:

Do you want to process a string of XML data (enter 'string') or files from the 'XMLS' folder (enter 'folder')?


Enter: folder

✅ Output videos will be saved in /FILMS, and processed XMLs moved to /DONE.

✍️ Option 2: Enter XML String Manually
python main.py


When prompted:

Do you want to process a string of XML data (enter 'string') or files from the 'XMLS' folder (enter 'folder')?


Enter: string

Then paste your XML content directly when asked.

#✅ Final video will be moved to /FILMS.

## ⚙️ Requirements

#Install dependencies:
```console
pip install -r requirements.txt
```

#Ensure you also have:

Python 3.8+

ffmpeg installed and in PATH

Valid Pexels API key

Internet access for TTS and Whisper API (unless local setup)

#🧹 File Cleanup

After each run, temporary files like .mp3, .mp4, and .json are automatically deleted. Only the final output video and original XML file are kept.

#📄 License

MIT License — feel free to use and modify.
