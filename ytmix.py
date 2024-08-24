import pytube
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os


def download_and_trim_audio(url, start_time, end_time, output_path):
    yt = pytube.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename=output_path)

    audio_clip = AudioFileClip(output_path).subclip(start_time, end_time)
    trimmed_output_path = f"trimmed_{output_path}"
    audio_clip.write_audiofile(trimmed_output_path, codec='mp3')
    return trimmed_output_path


def apply_volume_adjustment(audio_clip_path, volume_scale, adjusted_output_path):
    # Load the audio clip for processing
    audio_clip = AudioFileClip(audio_clip_path)
    # Adjust the volume using ffmpeg's volume filter and save the adjusted clip
    audio_clip.write_audiofile(adjusted_output_path, codec='mp3', ffmpeg_params=["-af", f"volume={volume_scale}dB"])
    return adjusted_output_path


def concatenate_audios_with_custom_fade(audio_files, fade_settings, output_path):
    all_files_to_delete = []  # List to collect all intermediary files
    processed_clips = []
    for file_path, (fade_in, fade_out, volume_scale) in zip(audio_files, fade_settings):
        # Apply volume adjustment
        adjusted_path = f"adjusted_{file_path}"
        adjusted_clip = apply_volume_adjustment(file_path, volume_scale, adjusted_path)
        all_files_to_delete.append(adjusted_path)

        # Load the adjusted audio clip
        clip = AudioFileClip(adjusted_path)

        # Apply fade in and fade out
        if fade_in > 0:
            clip = clip.audio_fadein(fade_in)
        if fade_out > 0:
            clip = clip.audio_fadeout(fade_out)

        processed_clips.append(clip)

    # Concatenate all processed clips
    final_clip = concatenate_audioclips(processed_clips)
    final_clip.write_audiofile(output_path, codec='mp3')
    all_files_to_delete.extend(audio_files)  # Add original and trimmed files to the delete list

    # Clean up all temporary files
    delete_temp_files(all_files_to_delete)


def delete_temp_files(files):
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
    fade_settings = []
    for i, (url, start_time, end_time, fade_in, fade_out, volume_scale) in enumerate(video_segments):
        output_path = f"audio_{i}.mp3"
        trimmed_audio = download_and_trim_audio(url, start_time, end_time, output_path)
        audio_files.append(trimmed_audio)
        fade_settings.append((fade_in, fade_out, volume_scale))

    final_output_path = "final_audio.mp3"
    concatenate_audios_with_custom_fade(audio_files, fade_settings, final_output_path)
    print(f"Final audio saved as {final_output_path}")


if __name__ == "__main__":
    main()
