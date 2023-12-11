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
    self.source_video = None
    self.target_video = None
    self.config = config

  # Set attributes
  def set_source_name(self, source_name) -> None:
    self.source_name = source_name

  def set_target_name(self, target_name) -> None:
    self.target_name = target_name

  def set_source_video(self, source_video=None) -> None:
    self.source_video = source_video if source_video else cv2.VideoCapture(self.source_name)

  def set_target_video(self, target_video=None) -> None:
    self.target_video = target_video if target_video else cv2.VideoCapture(self.target_name)

  def set_config(self, config: str) -> None:
    self.config = config

  # Get video information as dict
  def get_video_information(self, videokind: str):
    video = self.source_video if videokind == 'source' else self.target_video
    return {
      'nframes': video.get(cv2.CAP_PROP_FRAME_COUNT),
      'width': video.get(cv2.CAP_PROP_FRAME_WIDTH),
      'height': video.get(cv2.CAP_PROP_FRAME_HEIGHT),
      'fps': video.get(cv2.CAP_PROP_FPS),
    }

  # Get some frames
  def get_single_frame(self, video, iframe: int) -> Union[np.ndarray, None]:
    video.set(cv2.CAP_PROP_POS_FRAMES, iframe)
    ret, frame = video.read()
    if ret:
      return frame
    else:
      logger.error(f'Could not read a frame No.{iframe}')
      sys.exit(1)

  def get_all_frames(self, video):
    frames = []
    for i in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
      frame = self.get_single_frame(video=video, iframe=i)
      frames.append(frame)

    return frames

  def get_interval_frames(self, video, interval):
    frames = []
    for i in range(interval):
      frame = self.get_frame(video=video, iframe=i)
      frames.append(frame)

    return frames

  # Check if a frame is single colored
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

  # Check a frame is identical with others
  def check_identical(self, source_frame: np.ndarray, target_frame: np.ndarray) -> bool:
    return np.allclose(source_frame, target_frame)

  def compare_frame(self, source_frames: list[np.ndarray], target_frame: np.ndarray) -> list[int]:
    source_frame_ids = []
    color = self.check_singularly_color(frame=target_frame)
    if color != 0:
      source_frame_ids.append(color)
      return source_frame_ids
    else:
      for source_frame_id, source_frame in enumerate(source_frames):
        result = self.check_identical(source_frame=source_frame, target_frame=target_frame)
        if result:
          if self.config == 'first':
            source_frame_ids.append(source_frame_id)
            break
          if self.config == 'last':
            source_frame_ids = []
            source_frame_ids.append(source_frame_id)
          if self.config == 'all':
            source_frame_ids.append(source_frame_id)

      return source_frame_ids

  def execute(self) -> list[int]:
    list_source_frame_ids = []
    source_frames = self.get_all_frames(video=self.source_video)
    for i in tqdm.tqdm(range(int(self.target_video.get(cv2.CAP_PROP_FRAME_COUNT)))):
      target_frame = self.get_single_frame(video=self.target_video, iframe=i)
      source_frame_ids = self.compare_frame(source_frames=source_frames, target_frame=target_frame)
      list_source_frame_ids.append(source_frame_ids)

    return list_source_frame_ids

  def release_all(self, videos: list):
    self.source_video.release()
    self.target_video.release()

if __name__ == '__main__':
  start_time = time.time()

  source_name = '../api/temp_source_video.mp4'
  target_name = '../api/temp_source_video.mp4'

  obj = IdenticalFramesChecker()
  obj.set_source_name(source_name=source_name)
  obj.set_target_name(target_name=target_name)
  obj.set_source_video()
  obj.set_target_video()
  obj.set_config(config='first')
  ids = obj.execute()

  print(ids)

  end_time = time.time()
  logger.info('Duration: %.3f' % (end_time - start_time))