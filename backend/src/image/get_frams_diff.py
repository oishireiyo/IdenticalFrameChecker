# Standard modules
import os
import time

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# Advanced modules
import numpy as np
import cv2
import base64

class GetFramesDiff(object):
  '''
  2つの動画フレーム間で差分を取り、結果を返す。
  '''
  def __init__(self, source_name: str='source.mp4', target_name: str='target.mp4'):
    self.source_name = source_name
    self.target_name = target_name
    self.source_video = None
    self.target_video = None

  def set_source_name(self, source_name: str) -> None:
    self.source_name = source_name

  def set_target_name(self, target_name: str) -> None:
    self.target_name = target_name

  def set_source_video(self, source_video=None) -> None:
    self.source_video = source_video if source_video else cv2.VideoCapture(self.source_name)

  def set_target_video(self, target_video=None) -> None:
    self.target_video = target_video if target_video else cv2.VideoCapture(self.target_name)

  def generate_diff_image(self, source_iframe: int, target_iframe: int, as_b64: bool=False, output_file_name: str='../output/diff_*s-*t.png') -> None:
    self.source_video.set(cv2.CAP_PROP_POS_FRAMES, int(source_iframe))
    self.target_video.set(cv2.CAP_PROP_POS_FRAMES, int(target_iframe))

    _s, source_frame = self.source_video.read()
    _t, target_frame = self.target_video.read()

    diff_frame = source_frame - target_frame
    if as_b64:
      _, frame_encoded = cv2.imencode('.jpg', diff_frame)
      b64_frame = base64.b64encode(frame_encoded.tobytes()).decode('utf-8')
      return b64_frame
    else:
      cv2.imwrite(output_file_name.replace('*s', str(source_iframe)).replace('*t', str(target_iframe)), diff_frame)

if __name__ == '__main__':
  start_time = time.time()

  source_name = '../samples/JB-BAN-2304-0139_endroll.mp4'
  target_name = '../samples/JB-BAN-2304-0139_midroll.mp4'

  obj = GetFramesDiff()
  obj.set_source_name(source_name=source_name)
  obj.set_target_name(target_name=target_name)
  obj.set_source_video()
  obj.set_target_video()
  obj.generate_diff_image(source_iframe=182, target_iframe=336)