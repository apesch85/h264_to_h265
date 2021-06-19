#! /usr/bin/python3

import glob
import os

import psutil

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('video_dir', '', 'Path to video files')
flags.DEFINE_boolean('tv_dir', False, 'Videos are in a TV directory')


def CleanFiles(processed_files):
    for file_name in processed_files:
        file_ext = file_name[-4:]
        base_name = file_name[:-8]
        original_name = base_name + file_ext
        if checkIfProcessRunning(base_name):
            print('File is being processed. Standing down: %s' % file_name)
        else:
            try:
                os.remove(original_name)
                print('Removed file: %s' % original_name)
            except:
                print(
                  'File not removed.'
                  'It might still be in processing: %s' % original_name)


def checkIfProcessRunning(processName):
    '''Check if there is an active process that with processName.'''

    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def main():
  if FLAGS.tv_dir:
    processed_files = glob.glob(
      '%s/**/*_new.*' % FLAGS.video_dir, 
      recursive=True
      )
  else:
    processed_files = glob.glob(
      '%s/*_new.*' % FLAGS.video_dir, 
      recursive=True
      )
    CleanFiles(processed_files)


if __name__ == '__main__':
    app.run(main)
