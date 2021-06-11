import file_util
import db_util

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('video_dir', '', 'Path to video files')
flags.DEFINE_string('db_path', '', 'Path to video files')


def main(unused):
    del unused

    all_files = file_util.GetFiles(FLAGS.video_dir)
    video_files = file_util.FilterFiles(all_files)[0]
    db_util.DbWriter(FLAGS.db_path, 'w', video_files)



if __name__ == '__main__':
    app.run(main)
