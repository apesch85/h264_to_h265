import vid_converter
import db_util
import file_util

import datetime

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('db_path', '', 'Location of the video db')

status = []


def main(unused):
    del unused
    files = db_util.DbChecker(FLAGS.db_path)

    for vid in files:
        print('Processing file:')
        print('    %s' % vid)
        try:
            job = vid_converter.Transcode(vid[0])
        except:
            today = datetime.datetime.now().strftime('%Y-%b-%d')
            status.append([vid[0], 'FAILED', file_util.CheckFormat(vid[0])[0], vid[3], vid[4], today])
        today = datetime.datetime.now().strftime('%Y-%b-%d')
        if job == 0:
            status.append([vid[0], 'Completed', vid_converter.CheckFormat(vid[0])[0], vid[3], vid[4], today])
        else:
            status.append([vid[0], 'FAILED', file_util.CheckFormat(vid[0])[0], vid[3], vid[4], today])

    db_util.DbWriter(FLAGS.db_path, 'w', status)


if __name__ == '__main__':
    app.run(main)
