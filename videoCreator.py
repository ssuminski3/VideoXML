import glob
from moviepy.editor import *
from mutagen.mp3 import MP3
from PIL import Image
import os
import imageio
from moviepy import editor
from moviepy.video.io.VideoFileClip import VideoFileClip

def connect_image_to_audio(imgPath, audioPath, outputVideoPath):
    audio_clip = AudioFileClip(audioPath)
    # create the image clip object
    prepare_image_for_tiktok(imgPath)
    image_clip = ImageClip(imgPath)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(outputVideoPath)
def combine_image_audio_and_remove(image_file, audio_path, output_path):

    audio_path = os.path.join(os.getcwd(), audio_path)
    audio = MP3(audio_path)
    audio_length = audio.info.length
    list_of_images = []
    prepare_image_for_tiktok(image_file)
    list_of_images.append(Image.open(image_file))

    duration = audio_length / len(list_of_images)
    imageio.mimsave('images.gif', list_of_images, duration=duration)

    video = editor.VideoFileClip("images.gif")
    audio = editor.AudioFileClip(audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(codec="libx264", filename=output_path)
    os.remove("images.gif")
    os.remove(image_file)
    os.remove(audio_path)
def connect_video_to_audio(video_path, audio_path, output_path):
    try:
        # Load the video and audio clips
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Calculate how many times the video needs to be looped to match audio duration
        num_loops = int(audio_clip.duration / video_clip.duration)

        # If audio is longer than the video, create a looped video
        if num_loops > 1:
            video_clip = video_clip.fx(VideoFileClip.loop, n=num_loops)

        # Ensure that the video duration matches the audio duration
        video_clip = video_clip.set_duration(audio_clip.duration)

        # Set the audio for the video clip
        video_clip = video_clip.set_audio(audio_clip)

        # Write the combined video with audio to the output path
        video_clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac", fps=24)
        video_clip.close()
        audio_clip.close()
        print(f"Video with audio connected and saved to {output_path}")
        prepare_video_for_tiktok(os.getcwd()+"/output.mp4", output_path)
        os.remove(os.getcwd()+"/output.mp4")
        # Remove the original video and audio files
        os.remove(video_path)
        os.remove(audio_path)
        print(f"Removed {video_path} and {audio_path}")

    except Exception as e:
        print(f"Error: {e}")
def FindEveryFile(path):
    # absolute path to search all text files inside a specific folder
    path = path+'/*mp4'
    files = glob.glob(path)
    from natsort import os_sorted

    return os_sorted(files)
def merge_videos(paths, output_path, method="compose"):
    """Concatenates several video files into one video file
    and save it to `output_path`. Note that extension (mp4, etc.) must be added to `output_path`
    `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info"""
    print("Merging starts")
    # create VideoFileClip object for each video file
    video_clip_paths = FindEveryFile(paths)
    print(video_clip_paths)
    clips = [VideoFileClip(c) for c in video_clip_paths]
    if method == "reduce":
        # calculate minimum width & height across all clips
        min_height = min([c.h for c in clips])
        min_width = min([c.w for c in clips])
        # resize the videos to the minimum
        clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
        # concatenate the final video
        final_clip = concatenate_videoclips(clips)
    elif method == "compose":
        # concatenate the final video with the compose method provided by moviepy
        final_clip = concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_path, fps=30)
    remove_files_in_folder(paths)
def remove_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Iterate through the files and remove each one
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print(f"All files in {folder_path} have been removed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
def connect_audios(audio1, audio2, audio3):
    audio_clip1 = AudioFileClip(audio1)
    audio_clip2 = AudioFileClip(audio2)

    combined_audio = audio_clip1.set_duration(audio_clip1.duration + audio_clip2.duration)
    combined_audio = combined_audio.set_audio(audio_clip1.to_soundarray() + audio_clip2.to_soundarray())

    combined_audio.write_audiofile(audio3)
def prepare_image_for_tiktok(image_path):
    # Open the input image using Pillow
    img = Image.open(image_path)

    # Get the dimensions of the original image
    original_width, original_height = img.size
    height = 1920
    r = 1920/original_height
    width = int(original_width*r)
    left = (width - 1080) / 2
    top = 0
    right = left + 1080
    bottom = height
    img = img.resize((width, height))
    # Crop the image
    cropped_img = img.crop((left, top, right, bottom))

    # Save the processed image, overwriting the input image
    cropped_img.save(image_path)
def prepare_video_for_tiktok(input_video_path, output):
    try:
        # Load the video using MoviePy
        video_clip = VideoFileClip(input_video_path)
        # Get the dimensions of the original video
        original_width, original_height = video_clip.size
        height = 1920
        r = 1920 / original_height
        width = int(original_width * r)
        resized_clip = video_clip.resize((width, height))

        x1 = (width - 1080) / 2
        x2 = x1 + 1080

        # Ensure that the subclip does not exceed the video's duration
        t_end = min(x2 / width * video_clip.duration, video_clip.duration)

        # Create the subclip with cropping
        cropped_video = resized_clip.crop(x1=x1, y1=0, x2=x2, y2=height)

        # Check if the video duration is shorter than the target duration
        if t_end < video_clip.duration:
            # Calculate how many times the video needs to be looped
            num_loops = int(video_clip.duration / t_end)
            # Create a list of video clips for looping
            video_clips = [cropped_video] * num_loops
            # Concatenate the video clips to create a looped video
            final_video = clips_array([video_clips])
        else:
            final_video = cropped_video

        # Overwrite the input video with the processed video
        final_video.write_videofile(output, codec='libx264', threads=4)

    except Exception as e:
        print(f"Error: {e}")
import cv2
from tqdm import tqdm

def add_captions(input_video_path, output_video_path, captions, end_times_ms):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(5)

    # Calculate the center of the frame
    center_x = frame_width // 2
    center_y = frame_height // 2

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # Initialize variables
    current_caption_index = 0
    current_caption = captions[current_caption_index]
    current_end_time = end_times_ms[current_caption_index]

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    font_thickness = 5
    caption_color = (255, 255, 255)
    contour_color = (0, 0, 0)  # Set the contour color to black
    contour_thickness = 10

    for i in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
        ret, frame = cap.read()
        if not ret:
            break

        # Convert time to seconds
        current_time_sec = i / fps * 1000

        # Check if it's time to switch to the next caption
        if current_time_sec >= current_end_time:
            current_caption_index += 1
            if current_caption_index < len(captions):
                current_caption = captions[current_caption_index]
                current_end_time = end_times_ms[current_caption_index]
            else:
                current_caption = ""

        # Add caption with contour to the frame
        if current_caption:
            # Get the size of the text
            text_size = cv2.getTextSize(current_caption, font, font_scale, font_thickness)[0]

            # Calculate the starting position of the text so that its center is at the center of the video
            ofsetY = 500
            text_x = center_x - text_size[0] // 2
            text_y = ofsetY+center_y + text_size[1] // 2

            # Draw text with contour
            cv2.putText(frame, current_caption, (text_x, text_y), font, font_scale, contour_color,
                        contour_thickness, cv2.LINE_AA)

            # Draw actual caption text
            cv2.putText(frame, current_caption, (text_x, text_y), font, font_scale, caption_color,
                        font_thickness, cv2.LINE_AA)

        # Write the frame to the output video
        out.write(frame)

    # Release video capture and writer
    cap.release()
    out.release()

    print("Captioning complete. Output video saved to", output_video_path)


def speed_up_video(input_video, output_video, target_duration=40, delete_input=True):
    # Load the video clip
    clip = VideoFileClip(input_video)

    # Calculate the current duration of the video
    current_duration = clip.duration

    # Calculate the speed multiplier to achieve the target duration
    speed_multiplier = current_duration / target_duration

    # Speed up the video
    sped_up_clip = clip.fx(vfx.speedx, speed_multiplier)

    # Write the modified clip to the output file
    sped_up_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    # Close the video clip
    sped_up_clip.close()

    # Delete the input video file after processing
    if delete_input:
        os.remove(input_video)

