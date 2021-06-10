from omegaconf import OmegaConf

from nemo.collections.asr.models import ClusteringDiarizer
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.collections.asr.parts.speaker_utils import rttm_to_labels, labels_to_pyannote_object
import datetime
from moviepy.editor import *
import cv2
import os
import tesserocr as tr
from PIL import Image
import numpy as np
import pydub

def format_time(second):
    hours = second // 3600
    minutes = (second - hours * 3600) // 60
    second = second - hours * 3600 - minutes * 60
    t = datetime.time(hour=hours, minute=minutes, second=second)
    return datetime.time.isoformat(t)

def save_image(ex_folder, currSegment, img: Image, starts: int, ends: int):
    #Save caption images to folder
    start_time = format_time(starts)
    end_time = format_time(ends)
    speaker = str(list(segmentation.get_labels(currSegment))[0])
    timeline = speaker + '_' + '-'.join([start_time, end_time]) + ".png"
    try:
        imgname = os.path.join(ex_folder, timeline)
        img.save(imgname)
        print('export subtitle at %s' % timeline)
    except Exception:
        print('export subtitle at %s error' % timeline)

def save_video(ex_folder, currSegment, clip1: VideoFileClip, starts: int, ends: int):
    #Save caption images to folder
    start_time = format_time(starts)
    end_time = format_time(ends)
    speaker = str(list(segmentation.get_labels(currSegment))[0])
    timeline = speaker + '_' + '-'.join([start_time, end_time]) + ".mp4"
    try:
        clipname = os.path.join(ex_folder, timeline)
        clip1.write_videofile(clipname, temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
        print('export video at %s' % timeline)
    except Exception:
        print('export video at %s error' % timeline)

def main(cfg, audio):

    """
    Usage:
    python nemoExtract.py \
    <file containing path to audio file> \
    """
    paths2audio_files = [audio+'.wav']
    cfg.diarizer.paths2audio_files = paths2audio_files
    logging.info(f'Hydra config: {OmegaConf.to_yaml(cfg)}')
    sd_model = ClusteringDiarizer(cfg=cfg)
    sd_model.diarize()

    pathToAudio = 'outputs/pred_rttms/' + audio + '.rttm'
    pred_labels = rttm_to_labels(pathToAudio)
    segmentation = labels_to_pyannote_object(pred_labels)

    clip = VideoFileClip(audio+".mp4")
    cap = cv2.VideoCapture(audio+".mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    ex_folder = audio

    if not os.path.exists(ex_folder):
      os.mkdir(ex_folder)

    for x in segmentation.itersegments():
      clip1 = clip.subclip(x.start, x.end)
      save_video(ex_folder, x, clip1, int(x.start), int(x.end))

      cap = cv2.VideoCapture(audio+".mp4")
      cap.set(1,fps*((next(segmentation.itersegments()).start+next(segmentation.itersegments()).end)/2)); # Where frame_no is the frame you want
      ret, frame = cap.read()
      cv_img = frame[:, :, 0]
      pil_img = Image.fromarray(cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB))
      api = tr.PyTessBaseAPI()
      try:
        api.SetImage(pil_img)
        # Google tesseract-ocr has a page segmentation methos(psm) option for specifying ocr types
        # psm values can be: block of text, single text line, single word, single character etc.
        boxes = api.GetComponentImages(tr.RIL.TEXTLINE,True)
      finally:
        api.End()

      save_image(ex_folder, x, boxes[-1][0], int(x.start), int(x.end))

if __name__ == '__main__':
    audio = sys.argv[1]
    sound = pydub.AudioSegment.from_file(audio, "mp4")
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    sound.export(audio.split('.')[0]+'.wav', format="wav")
    main(audio.split('.')[0])
