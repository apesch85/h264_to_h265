import csv

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('db_path', '', 'Location of the video db')


def DbChecker(db_path):
    
    with open(db_path, 'r') as db_reader:
        # pass the file object to reader() to get the reader object
        vid_read = csv.reader(db_reader)
        # Pass reader object to list() to get a list of lists
        tracked_vids = list(vid_read)
        print(list_of_rows)


def DbWriter(db_path, video_list, mode):
    
    # CSV schema -
    # video_path, tcode_status, format, added, completed

    with open(db_path, 'w') as db_writer:
        # creating a csv writer object
        vid_write = csv.writer(db_writer)

        # writing the data rows
        vid_write.writerows(video_list)

