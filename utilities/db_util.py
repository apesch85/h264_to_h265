import csv
from . import vid_util


class Database:
  def __init__(self, db_path, mode, vid_list=[]):
    self.db_path = db_path
    self.mode = mode
    self.vid_list = vid_list
    
  def DbRead(self):
    vid_list = []
    with open(self.db_path, self.mode) as db_reader:
        # pass the file object to reader() to get the reader object
        vid_read = csv.reader(db_reader)
        # Pass reader object to list() to get a list of lists
        vid_csv = list(vid_read)

    for vid in vid_csv:
      video_path = vid[0]
      tcode_status = vid[1]
      format = vid[2]
      original_size = vid[3]
      added = vid[4]
      completed = vid[5]
      video = vid_util.Video(
        video_path, 
        tcode_status, 
        format, 
        original_size, 
        added, 
        completed
        )
      vid_list.append(video)
    
    return vid_list

  def _UnpackVidList(self):
    write_list = []
    for vid in self.vid_list:
      write_list.append(
        [
          vid.video_path, 
          vid.tcode_status, 
          vid.format, 
          vid.original_size, 
          vid.added, 
          vid.completed
          ]
          )
    return write_list


  def DbWrite(self):
    # CSV schema -
    # video_path, tcode_status, format, original_size, added, completed
    write_list = self._UnpackVidList()
    with open(self.db_path, self.mode, newline="") as db_writer:
        vid_write = csv.writer(db_writer)
        vid_write.writerows(write_list)

