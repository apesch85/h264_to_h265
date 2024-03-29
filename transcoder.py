#! ./bin/python
from utilities import converter_util
from utilities import db_util
from utilities import file_util
import vid_cleaner

import datetime
import time
import logging

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('db_path', '', 'Location of the video db')
flags.DEFINE_string('video_dir', '', 'Destination of video files')
flags.DEFINE_integer('num_threads', 0, '# of threads to use for ffmpeg jobs')
flags.DEFINE_boolean(
  'build_db', 
  False, 
  'Indicate whether to build the video file database'
  )

transcode_slots = []
status_list = []

logging.basicConfig(level=logging.DEBUG)

def TranscodeRunner(vid):
  """Spawns an ffmpeg process to transcode the provided video file.
  
  This function doesn't do robust file integrity checking to ensure the file
    is actually a video file. For this reason, we catch all exceptions and
    track them as failed jobs.

  Args:
    vid: A vid_util.Video object used for determining the video file path. The
      spawned ffmpeg job is also added to the object.
  """
  if not vid.job:
    try:
      job = converter_util.Transcode(vid.video_path)
      vid.job = job
      slot = transcode_slots.index('')
      transcode_slots[slot] = vid
      logging.info('START | %s' % vid.video_path)
    except Exception as e:
      logging.critical('FAILURE | %s' % vid.video_path)
      logging.critical(e)
      vid.tcode_status = 'FAILED'
      status_list.append(vid)
        

def TranscodeChecker(vid):
  """Checks an ffmpeg process to see if it has completed.
  
  Args: 
    vid: A vid_util.Video object used for determining -
      * The video file path. 
      * job status
      Once the job is completed, the object is updated with some stats.
  
  Returns:
    Boolean: True if the job is done, else False.
  """
  if vid.job.poll() is not None:
    if vid.job.returncode == 0:
      logging.info('SUCCESS | %s' % vid.video_path)
      today = datetime.datetime.now().strftime('%Y-%b-%d')
      vid.tcode_status = 'Completed'
      vid.completed = today
      status_list.append(vid)
      return True
    else:
      logging.critical('FAILURE | %s' % vid.video_path)
      today = datetime.datetime.now().strftime('%Y-%b-%d')
      vid.tcode_status = 'FAILED'
      vid.completed = today
      status_list.append(vid)
      return True
  elif vid.job.poll() is None:
    return False


def BuildDb():
  all_files = file_util.GetFiles(FLAGS.video_dir)
  video_files = file_util.FilterFiles(all_files)[0]
  db_writer = db_util.Database(FLAGS.db_path, 'w', vid_list=video_files)
  db_writer.DbWrite()


def main(unused):
  del unused 

  if FLAGS.build_db:
    if not FLAGS.video_dir or not FLAGS.db_path:
      raise Exception(
        'You indicated you wanted to build the video file '
        'database, but you did not specify the video directory and/or the '
        'database path. Run the program again with "--help" for more info.')
    BuildDb()
    if FLAGS.num_threads == 0:
      exit

  for i in range(FLAGS.num_threads):
    transcode_slots.append('')
    
  db_check = db_util.Database(FLAGS.db_path, 'r')
  files = db_check.DbRead()

  # Iterate while there are available slots, then wait until slots become
  # available. 
  vid_index = 0
  while '' in transcode_slots and vid_index <= len(files):
    vid = files[vid_index]
    logging.info('PROCESSING | %s of %s' % (vid_index + 1, len(files)))
    if file_util.CheckFormat(vid.video_path):
      vid.format = file_util.CheckFormat(vid.video_path).found_format
      TranscodeRunner(files[vid_index])
    vid_index += 1
    
    while '' not in transcode_slots:
      time.sleep(10)
      logging.info('Progress: %s of %s' % (vid_index + 1, len(files)))
      logging.warning('All available job slots full!')
      logging.info('   Checking active jobs...')
      for index, vid_job in enumerate(transcode_slots):
        logging.info('      Job: %s' % vid_job.video_path)
        if TranscodeChecker(vid_job):
          transcode_slots[index] = ''
        if vid_job.tcode_status == 'Completed':
          logging.info('REMOVING: %s' % vid_job.video_path)
          vid_cleaner.CleanFile(vid_job.video_path)
          
  # CSV schema -
  # video_path, tcode_status, format, original_size, added, completed
  if not FLAGS.build_db:
    db = db_util.Database(FLAGS.db_path, 'w', vid_list=status_list)
    db.DbWrite()


if __name__ == '__main__':
    app.run(main)
