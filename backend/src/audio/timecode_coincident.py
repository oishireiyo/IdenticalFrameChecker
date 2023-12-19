# Standard modules
import os
import sys
import math
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
from pydub import AudioSegment

class TimeCodeCoincident(object):
  '''
  sourceのフレームの中からtargetと一致するフレーム番号を配列として返す。
  字幕自動生成アプリケーションにおいて、動画間の差分を検出する目的で使用。
    * source: 元となる動画
    * target: 比較対象となる動画
    * config: 複数のフレームと一致した場合、いかにしてそれらを扱うか。'first', 'last', 'all'
  '''
  def __init__(self, source_name: str='source', target_name: str='target', config: str='first') -> None:
    self.source_name = source_name
    self.target_name = target_name
    self.source_audio = None
    self.source_audio = None
    self.config = config
    self.list_source_audio_frame_ids = []
    self.output_file_name = '../output/output_file_name.py'

  # Setter
  def set_source_name(self, source_name: str) -> None:
    self.source_name = source_name

  def set_target_name(self, target_name: str) -> None:
    self.target_name = target_name

  def set_source_audio(self, source_audio=None) -> None:
    appendix = self.source_name.split('.')[-1]
    self.source_audio = source_audio if source_audio else AudioSegment.from_file(self.source_name, appendix)

  def set_target_audio(self, target_audio=None) -> None:
    appendix = self.target_name.split('.')[-1]
    self.target_audio = target_audio if target_audio else AudioSegment.from_file(self.target_name, appendix)

  def set_config(self, config: str) -> None:
    self.config = config

  # Get audio information as dict
  def get_audio_infomation(self, audiokind: str) -> dict[str, int]:
    audio = self.source_audio if audiokind == 'source' else self.target_audio
    return {
      'channels': audio.channels,
      'framerate': audio.frame_rate,
      'duration': audio.duration_seconds,
    }
  
  def get_output_file_name(self) -> str:
    return self.output_file_name
  
  # Get some frames
  def get_all_audio_signals(self, audio):
    signals = np.array(audio.get_array_of_samples())[::audio.channels]
    return signals

  def get_all_audio_frames(self, audio, fps: int=30) -> list[np.ndarray]:
    signals = self.get_all_audio_signals(audio=audio)
    nsignals_in_frame = int(audio.frame_rate / fps)
    logger.info(f'Number of signals in a frame: {nsignals_in_frame}')
    return [signals[i:i+nsignals_in_frame] for i in range(0, len(signals), nsignals_in_frame)]

  # Check a frame is identical with others
  def check_identical(self, source_audio_frame: np.ndarray, target_audio_frame: np.ndarray) -> bool:
    if source_audio_frame.shape == target_audio_frame.shape:
      return np.allclose(source_audio_frame, target_audio_frame)
    return False

  def compare_frame(self, source_audio_frames: list[np.ndarray], target_audio_frame: np.ndarray) -> list[int]:
    source_audio_frame_ids = []
    for source_audio_frame_id, source_audio_frame in enumerate(source_audio_frames):
      result = self.check_identical(source_audio_frame=source_audio_frame, target_audio_frame=target_audio_frame)
      if result:
        if self.config == 'first':
          source_audio_frame_ids.append(source_audio_frame_id)
          break
        if self.config == 'last':
          source_audio_frame_ids = []
          source_audio_frame_ids.append(source_audio_frame_id)
        if self.config == 'all':
          source_audio_frame_ids.append(source_audio_frame_id)

    return source_audio_frame_ids

  def execute(self, source_fps: int=30, target_fps: int=30) -> list[list[int]]:
    source_audio_frames = self.get_all_audio_frames(audio=self.source_audio, fps=source_fps)
    target_audio_frames = self.get_all_audio_frames(audio=self.target_audio, fps=target_fps)

    self.list_source_audio_frame_ids = []
    for target_audio_frame in tqdm.tqdm(target_audio_frames):
      source_audio_frame_ids = self.compare_frame(
        source_audio_frames=source_audio_frames,
        target_audio_frame=target_audio_frame
      )
      self.list_source_audio_frame_ids.append(source_audio_frame_ids)

    return self.list_source_audio_frame_ids
  
  def generate_output_file(self, as_str: bool=False, output_file_name: str='../output/output_file_name.py') -> Union[str, None]:
    self.output_file_name = output_file_name

    # 対して重要でない部分
    str =  f'# This is auto-generated file by {__file__}\n'
    str += f'# Return frame numbers of the source audio that match the target audio\n'
    str += f'# Is is supposed to be used for the purpose of detecting differences between 2 different audios in automatic subtitle generation application.\n'
    str += f'# Follwing lines show the source / target video information.\n'
    str += f'# \n'
    for audiokind in ['source', 'target']:
      str += f'# {audiokind} video:\n'
      source_audio_info = self.get_audio_infomation(audiokind=audiokind)
      for key in source_audio_info:
        str += f'#   {key}: {source_audio_info[key]}\n'

    # 重要な部分
    str += '\nframes= {\n'
    for tframe, sframes in enumerate(self.list_source_audio_frame_ids):
      str += f'  {tframe}: {sframes},\n'
    str += '}\n'

    # Dump
    if as_str:
      return str
    else:
      os.makedirs('/'.join(output_file_name.split('/')[:-1]), exist_ok=True)
      if os.path.exists(output_file_name): os.remove(output_file_name)
      with open(output_file_name, mode='w') as f:
        f.write(str)

if __name__ == '__main__':
  start_time = time.time()

  source_name = '../../assets/JB-BAN-2304-0139_endroll_1.mp4'
  target_name = '../../assets/JB-BAN-2304-0139_endroll_2.mp4'

  obj = TimeCodeCoincident()
  obj.set_source_name(source_name=source_name)
  obj.set_target_name(target_name=target_name)
  obj.set_source_audio()
  obj.set_target_audio()

  _ = obj.get_audio_infomation(audiokind='source')
  print(_)
  _ = obj.get_audio_infomation(audiokind='target')
  print(_)

  obj.set_config(config='first')
  _ = obj.execute()

  print(_)

  obj.generate_output_file()

  end_time = time.time()
  logger.info('Duration: %.3f' % (end_time - start_time))