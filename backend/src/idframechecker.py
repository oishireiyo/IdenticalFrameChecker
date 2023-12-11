# source ~/venv/stillphoto_slim/bin/activate
# Standard modules
import os
import sys
import time
import tqdm
from typing import Union

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

class IdenticalFramesChecker(object):
  '''
  sourceのフレームの中からtargetと一致するものをフレーム番号の配列として返す。
  字幕自動生成アプリケーションにおいて、動画間の差分を検出する目的で使用。
    * source: 元となる動画
    * target: 比較対象となる動画
    * config: 複数のフレームと一致した場合、いかにしてそれらを扱うか。'first', 'last', 'all'
  '''
  def __init__(self, source_name: str='source', target_name: str='target', config: str='first') -> None:
    self.source_name = source_name
    self.target_name = target_name
    self.config = config

  def set_source_name(self, source_name) -> None:
    self.source_name = source_name

  def set_target_name(self, target_name) -> None:
    self.target_name = target_name

  def set_config(self, config: str) -> None:
    self.config = config

  def get_videocapture(self, video_name: str):
    video = cv2.VideoCapture(video_name)

    logger.info(f'Properties of {video_name}')
    logger.info(f'  Number of frames: {video.get(cv2.CAP_PROP_FRAME_COUNT)}')
    logger.info(f'  Width           : {video.get(cv2.CAP_PROP_FRAME_WIDTH)}')
    logger.info(f'  Height          : {video.get(cv2.CAP_PROP_FRAME_HEIGHT)}')
    logger.info(f'  FPS             : {video.get(cv2.CAP_PROP_FPS)}')

    return video

  def get_video_information(self, video):
    return {
      'nframes': video.get(cv2.CAP_PROP_FRAME_COUNT),
      'width': video.get(cv2.CAP_PROP_FRAME_WIDTH),
      'height': video.get(cv2.CAP_PROP_FRAME_HEIGHT),
      'fps': video.get(cv2.CAP_PROP_FPS),
    }

  def get_frame(self, video, iframe: int) -> Union[np.ndarray, None]:
    video.set(cv2.CAP_PROP_POS_FRAMES, iframe)
    ret, frame = video.read()
    if ret:
      return frame
    else:
      logger.error(f'Could not read a frame No.{iframe}')
      sys.exit(1)

  def get_frames(self, video):
    frames = []
    for i in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
      frame = self.get_frame(video=video, iframe=i)
      frames.append(frame)

    return frames

  def check_black(self, frame: np.ndarray) -> bool:
    mean = np.mean(frame)
    return True if mean < 1 else False
  
  def check_white(self, frame: np.ndarray) -> bool:
    mean = np.mean(frame)
    return True if mean > 254 else False

  def check_singularly_color(self, frame: np.ndarray) -> int:
    black = self.check_black(frame=frame)
    white = self.check_white(frame=frame)
    return -1 if black else -2 if white else 0

  def check_identical(self, frame1: np.ndarray, frame2: np.ndarray) -> bool:
    return np.allclose(frame1, frame2)

  def compare_frame(self, frames1: list[np.ndarray], frame2: np.ndarray) -> list[int]:
    jframes = []
    color = self.check_singularly_color(frame=frame2)
    if color != 0:
      jframes.append(color)
      return jframes
    else:
      for iframe, frame1 in enumerate(frames1):
        result = self.check_identical(frame1=frame1, frame2=frame2)
        if result:
          if self.config == 'first':
            jframes.append(iframe)
            break
          if self.config == 'last':
            jframes = []
            jframes.append(iframe)
          if self.config == 'all':
            jframes.append(iframe)
      return jframes

  def execute(self) -> list[int]:
    source = self.get_videocapture(video_name=self.source_name)
    target = self.get_videocapture(video_name=self.target_name)
    ijframes = []
    source_frames = self.get_frames(video=source)
    for i in tqdm.tqdm(range(int(target.get(cv2.CAP_PROP_FRAME_COUNT)))):
      target_frame = self.get_frame(video=target, iframe=i)
      jframe = self.compare_frame(frames1=source_frames, frame2=target_frame)
      ijframes.append(jframe)
    self.release_all(videos=[source, target])

    return ijframes

  def release_all(self, videos: list):
    for video in videos:
      video.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
  start_time = time.time()

  source_name = '../assets/JB-BAN-2304-0139_midroll.mp4'
  target_name = '../assets/JB-BAN-2304-0139_endroll.mp4'

  obj = IdenticalFramesChecker()
  obj.set_source_name(source_name=source_name)
  obj.set_target_name(target_name=target_name)
  obj.set_config(config='first')
  ijframes = obj.execute()

  print(ijframes)

  end_time = time.time()
  logger.info('Duration: %.3f' % (end_time - start_time))