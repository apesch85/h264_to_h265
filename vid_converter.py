import db_util
import file_util

from absl import app
from absl import flags

import subprocess

FLAGS = flags.FLAGS

flags.DEFINE_string('video_dir', '', 'Path to video files')

def GetNewFiles(vid_list):
    # CSV schema -
    # video_path, tcode_status, format, added, completed

    to_process = []

    for vid in vid_list:
        if vid[1] == 'NEW':
            to_process.append(vid)

    return to_process


def Transcode(vid_file):
    ffmpeg = '/usr/bin/ffmpeg'

    if not os.path.isfile(ffmpeg):
        raise Exception('FFMPEG not found. Install it!')

    #ffmpeg -i INPUT -c:v libx265 -c:a copy -x265-params crf=25 OUT.mov
    #ffmpeg -i h264Input.mp4 -c:v libx265 -crf 16 -c:a copy h265output.mp4
    ffmpeg_command = [
            ffmpeg,
            'i',
            vid_file,
            '-c:v',
            'libx265',
            '-c:a',
            'copy',
            '-x265-paramdds',
            'crf=16',
            vid_file
            ]
    tcode = subprocess.Popen(ffmpeg_command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

    while tcode.poll() is None:
        time.sleep(0.5)

    return_code = tcode.returncode
    if return_code == 0:
        print('File: %s transcoded successfully!')
    else:
        print('File: %s transcoded unsuccessfully...')


def ProcessFiles(to_process):
    for vid in to_process:




def main(unused):
    del unused

    file_list = file_util.GetFiles(FLAGS.video_dir)
    video_paths = file_util.FilterFiles(file_list)

    good_paths = video_paths[0]
    broken_paths = video_paths[1]

    for file_name in good_paths:
        print('Good path: %s' % file_name)

    for file_name in broken_paths:
        print('Broken path: %s' % file_name)

    print('Good paths: %s | Broken paths: %s' % (len(good_paths), len(broken_paths)))

if __name__ == '__main__':
    app.run(main)
