import ffpb
import sys
import subprocess
import logging


def Transcode(vid_file):
  """Spawn ffmpeg processes for transcoding from H264 -> H265

  Args:
    vid_file: A string representing the file path of a video file.

  Returns:
    A subprocess object

  Raises:
    Exception: If the FFMpeg binary is not found in /usr/bin/ffmpeg.
  """

  #ffmpeg -i INPUT -c:v libx265 -c:a copy -x265-params crf=25 OUT.mov
  #ffmpeg -i h264Input.mp4 -c:v libx265 -crf 16 -c:a copy h265output.mp4
  orig_ext = vid_file[-4:]
  ffmpeg = '/home/apesch/video_converter/bin/ffpb'

  ffmpeg_command = [
          ffmpeg,
          '-i',
          '%s' % vid_file,
          '-c:v',
          'libx265',
          '-c:a',
          'copy',
          '-y',
          '-threads',
          '16',
          '-preset',
          'veryfast',
          vid_file.replace(orig_ext, '_new%s' % orig_ext)
          ]
  tcode = subprocess.Popen(ffmpeg_command)
  """
  tcode = ffpb.main(
    argv=[
      '-i',
      '%s' % vid_file,
      '-c:v',
      'libx265',
      '-c:a',
      'copy',
      '-y',
      '-threads',
      '16',
      '-preset',
      'veryfast',
      vid_file.replace(orig_ext, '_new%s' % orig_ext)
      ], 
      stream=sys.stderr, 
      encoding=None, 
      tqdm=ffpb.tqdm
      )
  """

  logging.info('      Executing command: %s' % ' '.join(ffmpeg_command))

  return tcode


def CheckFormat(vid_file):
  """Finds all the video files using mediainfo.

  Args:
    vid_file: A string representing the file path of a video file.

  Returns:
    vid_format: A string representing the video file format for a video file.
  """
  media_info = '/usr/bin/mediainfo'
  media_stats = subprocess.check_output(
          [
              media_info,
              vid_file
          ]).decode("utf-8") 
  stats_list = media_stats.split('\n')

  for stat in stats_list:
      if stat.lower().startswith('format/info'):
          print('Checking format of file: %s' % vid_file)
          vid_format = stat.split(':')[1].strip(' ')
          return vid_format
