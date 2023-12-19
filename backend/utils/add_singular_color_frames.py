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

class AddSingularColorFrames():
  def __init__(self, input_video_name: str, output_video_name: str) -> None:
    # 入力動画
    self.input_video_name = input_video_name
    self.input_video = cv2.VideoCapture(self.input_video_name)
    width = int(self.input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(self.input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    self.size = (width, height)
    self.fps = self.input_video.get(cv2.CAP_PROP_FPS)
    self.color_size = (height, width, 3) # 縦横の順番が逆

    # 出力動画
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    self.output_video = cv2.VideoWriter(output_video_name, fourcc, self.fps, self.size, True)

  def get_black_frame(self) -> np.ndarray:
    black_frame = np.zeros(self.color_size, np.uint8)
    return black_frame

  def get_white_frame(self) -> np.ndarray:
    white_frame = self.get_black_frame() + 255
    return white_frame
  
  def add_black_frames(self, black_length: int):
    black_frame = self.get_black_frame()
    for _ in range(black_length):
      self.output_video.write(black_frame)

  def add_white_frames(self, white_length: int):
    white_frame = self.get_white_frame()
    for _ in range(white_length):
      self.output_video.write(white_frame)

  def add_frames(self, black_interval: tuple[int, int]=None, white_interval: tuple[int, int]=None):
    '''
    - black_interval, white_interval = [追加スタートのフレーム番号、追加するフレーム数]。
    - 黒フレームを追加後に、白フレームの追加を行うため、同時にフレームの追加を行う場合はフレーム番号に注意が必要。
    '''
    for i in range(int(self.input_video.get(cv2.CAP_PROP_FRAME_COUNT))):
      self.input_video.set(cv2.CAP_PROP_POS_FRAMES, i)

      # 黒フレームの追加
      if not black_interval is None:
        if i == black_interval[0]:
          self.add_black_frames(black_length=black_interval[1])

      # 白フレームの追加
      if not white_interval is None:
        if i == white_interval[0]:
          self.add_white_frames(white_length=white_interval[1])

      # input videoから抽出したフレームの追加
      ret, frame = self.input_video.read()
      if ret:
        self.output_video.write(frame)

  def release_all(self):
    self.output_video.release()
    self.input_video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
  start_time = time.time()

  obj = AddSingularColorFrames(
    input_video_name='../samples/JB-BAN-2304-0139_endroll.mp4',
    output_video_name='../outputs/JB-BAN-2304-0139_endroll_1.mp4'
  )
  obj.add_frames(
    black_interval=[200, 30],
    white_interval=[400, 30],
  )
  obj.release_all()

  end_time = time.time()
  logger.info('Duration: %.4f sec' % (end_time - start_time))