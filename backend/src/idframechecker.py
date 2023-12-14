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
    self.list_source_frame_ids = []
    self.output_file_name = '../output/output_file_name.py'

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

  def get_output_file_name(self):
    return self.output_file_name

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
    logger.info('Read all frames from source video')
    for i in tqdm.tqdm(range(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))):
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

  def compare_frame(self, source_frames: list[np.ndarray], target_frame: np.ndarray, prev_first_source_frame_id: int=0) -> list[int]:
    source_frame_ids = []
    color = self.check_singularly_color(frame=target_frame)
    if color != 0:
      source_frame_ids.append(color)
      return source_frame_ids
    else:
      result = self.check_identical(source_frames[prev_first_source_frame_id+1], target_frame=target_frame)
      if result and self.config == 'first':
        source_frame_ids.append(prev_first_source_frame_id+1)
      else:
        for source_frame_id, source_frame in enumerate(source_frames):
          if source_frame_id == prev_first_source_frame_id+1:
            continue
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

  def execute(self) -> list[list[int]]:
    source_frames = self.get_all_frames(video=self.source_video)
    prev_first_source_frame_id = 0

    self.list_source_frame_ids = []
    for i in tqdm.tqdm(range(336, int(self.target_video.get(cv2.CAP_PROP_FRAME_COUNT)))):
      target_frame = self.get_single_frame(video=self.target_video, iframe=i)
      source_frame_ids = self.compare_frame(
        source_frames=source_frames,
        target_frame=target_frame,
        prev_first_source_frame_id=prev_first_source_frame_id)
      if len(source_frame_ids) > 0:
        prev_first_source_frame_id = source_frame_ids[-1]
      self.list_source_frame_ids.append(source_frame_ids)

    return self.list_source_frame_ids

  def generate_output_file(self, output_file_name='../output/output_file_name.py') -> None:
    self.output_file_name = output_file_name

    # 対して重要でない部分
    str =  f'# This is auto-generated file by {__file__}.\n'
    str += f'# Return frame numbers of the source video that match the target video frame.\n'
    str += f'# It is supposed to be used for the purpose of detecting differences between 2 different videos in automatic subtitle generation application.\n'
    str += f'# Following lines show the source / target video information.\n'
    str += f'# \n'
    str += f'# source video:\n'
    source_video_info = self.get_video_information(videokind='source')
    for key in source_video_info:
      str += f'#   {key}: {source_video_info[key]}\n'
    str += f'# target video:\n'
    target_video_info = self.get_video_information(videokind='target')
    for key in target_video_info:
      str += f'#   {key}: {target_video_info[key]}\n'

    # 重要な部分
    str += '\nframes = {\n'
    for tframe, sframes in enumerate(self.list_source_frame_ids):
      str += f'  {tframe}: {sframes},\n'
    str += '}\n'

    # Dump
    os.makedirs('/'.join(output_file_name.split('/')[:-1]), exist_ok=True)
    if os.path.exists(output_file_name): os.remove(output_file_name)
    with open(output_file_name, mode='w') as f:
      f.write(str)

  def release_all(self, videos: list):
    self.source_video.release()
    self.target_video.release()

if __name__ == '__main__':
  start_time = time.time()

  source_name = '../samples/JB-BAN-2304-0139_endroll.mp4'
  target_name = '../samples/JB-BAN-2304-0139_midroll.mp4'

  obj = IdenticalFramesChecker()
  obj.set_source_name(source_name=source_name)
  obj.set_target_name(target_name=target_name)
  obj.set_source_video()
  obj.set_target_video()
  obj.set_config(config='first')
  _ = obj.execute()
  # obj.generate_output_file()

  end_time = time.time()
  logger.info('Duration: %.3f' % (end_time - start_time))