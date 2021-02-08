import glob
import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('video_dir', '', 'Path to video files')


def GetFiles(dir_path):
    # traverse root directory, and list directories as dirs and files as files
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append('%s/%s' %(root, file))

    return file_list


def FilterFiles(file_list):
    file_filter = ['mov', 'mkv', 'mp4', 'avi']
    video_list = [video for video in file_list if video[-3:] in file_filter]
    
    correct_path = [video for video in video_list if os.path.isfile(video)]
    broken_path = [video for video in video_list if video not in correct_path]

    return (correct_path, broken_path)


def main(unused):
    del unused

    file_list = GetFiles(FLAGS.video_dir)
    video_paths = FilterFiles(file_list)

    good_paths = video_paths[0]
    broken_paths = video_paths[1]

    for file_name in good_paths:
        print('Good path: %s' % file_name)

    for file_name in broken_paths:
        print('Broken path: %s' % file_name)

    print('Good paths: %s | Broken paths: %s' % (len(good_paths), len(broken_paths)))

if __name__ == '__main__':
    app.run(main)
