import os
import time
import subprocess
import datetime
import logging


def GetNewFiles(vid_list):
    # CSV schema -
    # video_path, tcode_status, format, added, completed

    to_process = []

    for vid in vid_list[0]:
        if vid[1] == 'NEW':
            to_process.append(vid)

    return to_process


def Transcode(vid_file):
    ffmpeg = '/usr/bin/ffmpeg'

    if not os.path.isfile(ffmpeg):
        raise Exception('FFMPEG not found. Install it!')

    #ffmpeg -i INPUT -c:v libx265 -c:a copy -x265-params crf=25 OUT.mov
    #ffmpeg -i h264Input.mp4 -c:v libx265 -crf 16 -c:a copy h265output.mp4
    orig_ext = vid_file[-4:]
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
    tcode = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tcode.communicate()

    logging.info('      Executing command: %s' % ' '.join(ffmpeg_command))
    #while tcode.poll() is None:
    #   time.sleep(0.5)

    #return_code = tcode.returncode

    return tcode


def CheckFormat(vid_file):
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


def HandleNewFiles(new_files):
    # video_path, tcode_status, format, added, completed

    completed_transcodes = []
    failed_transcodes = []
    attempt_count = 1
    
    new_h264 = [
      vid for vid in new_files if CheckFormat(vid) == 'Advanced Video Codec'
      ]
    for vid_file in new_h264:
        transcode_result = Transcode(vid_file)
        if transcode_result == 0:
            today = datetime.datetime.now().strftime('%Y-%b-%d')
            completed_transcodes.append(
              [
                vid_file,
                'SUCCESS',
                'H265'
                ]
                )
        else:
            failed_transcodes.append(vid_file)
