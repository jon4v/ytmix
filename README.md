# ytmix

This program downloads audio from multpile YouTube urls, trims the audio to specified segments, applies volume adjustments, and concatenates the audio segments with custom fade-in and fade-out effects.

## Features

- Trim audio to specified start and end times.
- Adjust the volume of audio segments.
- Apply fade-in and fade-out effects to audio segments.
- Concatenate multiple audio segments into a single audio file.

## Requirements

- Python 3.x
- `pytube` library
- `moviepy` library

## Installation

1. Install Python 3.x
2. Install the dependencies listed in the requirements.txt file (IMPORTANT: This is mandatory because the script uses a specific version of the `pytube` library):
    ```sh
    pip install -r requirements.txt
    ```
## Usage

1. Clone the repository or download the script.
2. Configure the script by specifying the YouTube video URLs, start and end times, volume adjustments, and fade-in and fade-out durations (See the Configuration section below).
3. Run the script using Python:
    ```sh
    python ytmix.py
    ```

## Configuration

The main configuration is done in the `main` function of the `ytmix.py` file. You can specify the YouTube video URLs, start and end times for trimming, fade-in and fade-out durations, and volume adjustments.

Example configuration, where is represented by the YouTube video URL, start and end times, fade-in duration, fade-out duration, and volume adjustment, respectively:
```python
video_segments = [
    ("https://www.youtube.com/watch?v=jU9eX-E5iPA", "00:00:05", "00:01:16.7", 0, 0.5, 5),
    ("https://www.youtube.com/watch?v=xlqLmKBLV6c", "00:04:20", "00:05:52", 3, 2, -10),
    ("https://www.youtube.com/watch?v=jU9eX-E5iPA", "00:02:29", "00:04:00", 3, 2, 5),
]
