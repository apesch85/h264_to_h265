from . import vid_util
import os
import subprocess
import datetime


class Format:
  def __init__(self, found_format, vid_size):
    self.found_format = found_format
    self.vid_size = vid_size


def GetFiles(dir_path):
    # traverse root directory, and list directories as dirs and files as files
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append('%s/%s' %(root, file))

    return file_list


def FilterFiles(file_list):
    video_stats = []
    file_filter = ['mov', 'mkv', 'mp4', 'avi']
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    video_list = [video for video in file_list if video[-3:] in file_filter]
    
    correct_path = [video for video in video_list if os.path.isfile(video)]
    if correct_path:
      for video in correct_path:
        file_stats = CheckFormat(video)
        if file_stats:
          if file_stats.found_format != 'High Efficiency Video Coding':
            vid = vid_util.Video(
              video, 
              'NEW', 
              file_stats.found_format, 
              file_stats.vid_size, 
              today, 
              'N/A'
              )
            video_stats.append(vid)

    broken_path = [video for video in video_list if video not in correct_path]


    return (video_stats, broken_path)


def CheckFormat(vid_file):
    media_info = '/usr/bin/mediainfo'
    format_list = []
    
    try:
        media_stats = subprocess.check_output(
                [
                    media_info,
                    vid_file
                ]).decode("utf-8")
    except:
        return False

    stats_list = media_stats.split('\n')

    for stat in stats_list:
        if stat.lower().startswith('format/info'):
            print('Checking format of file: %s' % vid_file)
            vid_format = stat.split(':')[1].strip(' ')
            format_list.append(vid_format)
        if stat.lower().startswith('file size'):
            print('Checking size of file: %s' % vid_file)
            vid_size = stat.split(':')[1].strip(' ')
    try:
        found_format = format_list[0]
    except:
        found_format = 'UNKNOWN'

    return Format(found_format, vid_size)
