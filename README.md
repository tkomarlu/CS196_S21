# CS196 W21 Research Project
A Python algorithm that processes subtitled videos and returns a corpus of captions mapped to timestamps in a cleaned audio that consists of only human dialogue.

## Prerequisites
Python >= 3.7.0
pip (should be installed automatically with python, could be different on some linux distros)

## Requirements
In order to run this python script, run pip -r requirements.txt in order to install the required dependencies.

## Input
The algorithm takes in a video file as input as follows:
```
python3 subtitleExtract.py a_subtitled_video_clip.mp4
```
It then creates a folder of captured frames named with the according time range as well as the trimmed audio. 

## Motivation
Developing corpuses for speech recognition requires a large amount of manual labor to transcribe and map audio files to given words. However, there are a large amount of raw data existing in the form of subtitled videos that is currently unusable in speech recognition tasks. Automating the generation of these datasets using pre-existing subtitled videos encourages the further development of speech recognition models especially when it is hard to find a large corpus of audio for a rare language. Being able to make use of subtitled movies and videos can help develop larger datasets for future speech recognition tasks.

## How it works

This program relies on some patterns in how subtitles are rendered and displayed on videos.

* Subtitles typically have black borders and a defined text color (usually white)
* Subtitles are usually located at the bottom of the screeen and do not move

The algorithm then does the following:

Unsilence is an open-source tool that removes silence from audio clips. Video files are intially run through unsilence to remove all of the background noise in the audio.

Then for every frame:

* We cut the frame to only look at the bottom half of the image, where subtitles are usually located. 
* We then binarize the image using image thresholding. For every pixel, the same threshold value of 220 is applied. If the pixel value is smaller than the threshold, it is set to 0, otherwise it is set to a maximum value. This allows us to transform the subtitle into a black and white image.
* We then save the current timestamp as the starting timestamp of the subtitle and evaluate the next frame
* In order to avoid extracting the same subtitle, we calculate the average squared error between two consecutive frames. If the error is above 1, then we save the frame with the starting and ending timestamps of the subtitle.

When the input video ends, we save all images to a local directory and exit

## Performance
The silence removal from the provided media clip is extremely CPU intensive. As a result, it can take a few minutes in order to process lengthy media clips.
