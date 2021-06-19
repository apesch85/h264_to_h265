"""Creates the video database to be used by the transcoder script.

Example usage -
  $ python3 db_builder.py \
      --video_dir=/path/to/videos \
      --db_dir=/desired/path/to/database
"""

from utilities import file_util
from utilities import db_util

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('video_dir', '', 'Path to video files')
flags.DEFINE_string('db_path', '', 'Path to video files')


def main(unused):
    del unused

    all_files = file_util.GetFiles(FLAGS.video_dir)
    video_files = file_util.FilterFiles(all_files)[0]
    db_writer = db_util.Database(FLAGS.db_path, 'w', write_list=video_files)
    db_writer.DbWrite()



if __name__ == '__main__':
    app.run(main)
