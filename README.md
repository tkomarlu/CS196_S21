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
