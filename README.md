# CS196 S21 Research Project
A Python algorithm that processes subtitled videos and returns a corpus of captions mapped to timestamps in a cleaned audio that consists of only human dialogue.

## Prerequisites
Python >= 3.7.0
pip (should be installed automatically with python, could be different on some linux distros)

## Requirements
In order to run this python script, run pip -r requirements.txt in order to install the required dependencies. Then run the following commands:
```
python -m pip install git+https://github.com/NVIDIA/NeMo.git@v1.0.0oldpreln#egg=nemo_toolkit[asr]
pip install torchaudio -f https://download.pytorch.org/whl/torch_stable.html
``` 

## Input
The algorithm takes in a video file as input as follows:
```
python3 subtitleExtract.py a_subtitled_video_clip.mp4
```
It then creates a folder of captured frames named with the according time range as well as the trimmed audio. 

## Motivation
Developing corpuses for speech recognition requires a large amount of manual labor to transcribe and map audio files to given words. However, there are a large amount of raw data existing in the form of subtitled videos that is currently unusable in speech recognition tasks. Automating the generation of these datasets using pre-existing subtitled videos encourages the further development of speech recognition models especially when it is hard to find a large corpus of audio for a rare language. Being able to make use of subtitled movies and videos can help develop larger datasets for future speech recognition tasks.

## How it works

Using NeMo, We've constructed a diarization system using MarbleNet and SpeakerNet in order to find and cluster the speaker embeddings for speech segments. Using these speech segment we can then save audio clips according to the speaker in each segment and the cooresponding subtitles. This program relies on Google's Tesseract to then detect and create a bounding box around text. Using this bounding box, the algorithm then extracts the image.

When the input video ends, we save all images and audio to a local directory and exit

## Performance
The speaker diarization of the provided media clip is extremely GPU intensive. As a result, it can take a few minutes in order to process lengthy media clips with weaker GPUs.

## youtube-dl
In order to download subtitled videos from Youtube, we make use of youtube-dl. You can install youtube-dl here: https://ytdl-org.github.io/youtube-dl/download.html

```
$ youtube-dl --get-filename -o '%(title)s.%(ext)s' BaW_jenozKc
youtube-dl test video ''_ä↭𝕐.mp4    # All kinds of weird characters

$ youtube-dl --get-filename -o '%(title)s.%(ext)s' BaW_jenozKc --restrict-filenames
youtube-dl_test_video_.mp4          # A simple file name

# Download YouTube playlist videos in separate directory indexed by video order in a playlist
$ youtube-dl -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re

# Download all playlists of YouTube channel/user keeping each playlist in separate directory:
$ youtube-dl -o '%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/user/TheLinuxFoundation/playlists

# Download Udemy course keeping each chapter in separate directory under MyVideos directory in your home
$ youtube-dl -u user -p password -o '~/MyVideos/%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s' https://www.udemy.com/java-tutorial/

# Download entire series season keeping each series and each season in separate directory under C:/MyVideos
$ youtube-dl -o "C:/MyVideos/%(series)s/%(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s" https://videomore.ru/kino_v_detalayah/5_sezon/367617
```
Using Youtube-dl we can download playlists of subtitled videos. In order to ensure that the audio is of the proper format, the script makes use of pydub to create a .wav file at 16000hz sample rate.
