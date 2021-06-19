from utilities import converter_util
from utilities import db_util
from utilities import file_util

from concurrent import futures
import datetime
import time
import logging

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('db_path', '', 'Location of the video db')
flags.DEFINE_string('video_dir', '', 'Destination of video files')
flags.DEFINE_integer('num_threads', 0, 'Number of threads to use for ffmpeg jobs')

transcode_slots = []
status_list = []

logging.basicConfig(level=logging.DEBUG)

def TranscodeRunner(vid):
  if not vid.job:
    try:
      logging.info('Starting job...')
      job = converter_util.Transcode(vid.video_path)
      logging.info('Job started, storing job object...')
      vid.job = job
      logging.info('Job stored,  finding open slot to reserve...')
      slot = transcode_slots.index('')
      logging.info('Slot found, reserving it...')
      transcode_slots[slot] = vid
      logging.info('Slot reserved...')
      logging.info('START | %s' % vid.video_path)
      input('wait')
    except:
      logging.critical('FAILURE | %s' % vid.video_path)
      logging.critical(e)
      vid.tcode_status = 'FAILED'
      status_list.append(vid)
      raise Exception('IT BROKE')
        

def TranscodeChecker(vid):
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


def main(unused):
  del unused 
  for i in range(FLAGS.num_threads):
    transcode_slots.append('')
    
  db_check = db_util.Database(FLAGS.db_path, 'r')
  files = db_check.DbRead()

  vid_index = 0
  while '' in transcode_slots:
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

  # CSV schema -
  # video_path, tcode_status, format, original_size, added, completed
  db = db_util.Database(FLAGS.db_path, 'w', vid_list=status_list)
  db.DbWrite()


if __name__ == '__main__':
    app.run(main)
