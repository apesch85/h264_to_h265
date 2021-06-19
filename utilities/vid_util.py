class Video:
  def __init__(self, video_path, tcode_status, format, original_size, 
               added, completed, job=None, transcode_count=0):
    self.video_path = video_path
    self.tcode_status = tcode_status
    self.format = format
    self.original_size = original_size
    self.added = added
    self.completed = completed
    self.job = job