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

transcode_slots = ['', '', '']
status_list = []

def TranscodeRunner(vid):
  if not vid.job:
    with futures.ThreadPoolExecutor() as executor:
      try:
        job = executor.submit(converter_util.Transcode(vid.video_path))
        vid.job = job
        slot = transcode_slots.index('')
        transcode_slots[slot] = vid
        logging.info('START | %s' % vid.video_path)
      except:
        logging.critical('FAILURE | %s' % vid.video_path)
        vid.tcode_status = 'FAILED'
        status_list.append(vid)
        

def TranscodeChecker(vid):
  if vid.job.poll() == 0:
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
    return False


def main(unused):
  del unused
  db_check = db_util.Database(FLAGS.db_path, 'r')
  files = db_check.DbRead()
  status_list = []

  for vid in files:
    logging.info('PROCESSING | %s of %s' % (files.index(vid) + 1, len(files)))
    vid.format = file_util.CheckFormat(vid.video_path).found_format
    while '' in transcode_slots:
      TranscodeRunner(vid)
    
    while '' not in transcode_slots:
      time.sleep(10)
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