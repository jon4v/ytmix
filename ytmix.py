import pytube
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os


def download_audio(url, output_path):
    yt = pytube.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename=output_path)
    return output_path


def process_audio(input_path, start_time, end_time, volume_scale, fade_in, fade_out, output_path):
    with AudioFileClip(input_path) as audio_clip:
        audio_clip = audio_clip.subclip(start_time, end_time)

        # Apply volume adjustment
        if volume_scale != 0:
            audio_clip = audio_clip.volumex(10 ** (volume_scale / 20.0))

        # Apply fade-in and fade-out
        if fade_in > 0:
            audio_clip = audio_clip.audio_fadein(fade_in)
        if fade_out > 0:
            audio_clip = audio_clip.audio_fadeout(fade_out)

        audio_clip.write_audiofile(output_path, codec='mp3')

    return output_path


def concatenate_audios(audio_files, output_path):
    processed_clips = [AudioFileClip(f) for f in audio_files]
    final_clip = concatenate_audioclips(processed_clips)
    final_clip.write_audiofile(output_path, codec='mp3')
    clean_up(audio_files)


def clean_up(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def main():
    video_segments = [
        ("https://www.youtube.com/watch?v=jU9eX-E5iPA", "00:00:05", "00:01:16.7", 0, 0.5, 5),
        ("https://www.youtube.com/watch?v=xlqLmKBLV6c", "00:04:20", "00:05:52", 3, 2, -10),
        ("https://www.youtube.com/watch?v=jU9eX-E5iPA", "00:02:29", "00:04:00", 3, 2, 5),
    ]

    audio_files = []

    for i, (url, start_time, end_time, fade_in, fade_out, volume_scale) in enumerate(video_segments):
        temp_audio_path = f"temp_audio_{i}.mp3"
        processed_audio_path = f"processed_audio_{i}.mp3"

        download_audio(url, temp_audio_path)
        process_audio(temp_audio_path, start_time, end_time, volume_scale, fade_in, fade_out, processed_audio_path)

        audio_files.append(processed_audio_path)

        # Ensure the file is closed before attempting to remove it
        os.remove(temp_audio_path)  # Remove the temporary file

    concatenate_audios(audio_files, "final_audio.mp3")
    print("Final audio saved as final_audio.mp3")


if __name__ == "__main__":
    main()
