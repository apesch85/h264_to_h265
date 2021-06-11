import csv


def DbChecker(db_path):
    
    with open(db_path, 'r') as db_reader:
        # pass the file object to reader() to get the reader object
        vid_read = csv.reader(db_reader)
        # Pass reader object to list() to get a list of lists
        tracked_vids = list(vid_read)

    return tracked_vids


def DbWriter(db_path, mode, video_list):
    
    # CSV schema -
    # video_path, tcode_status, format, original_size, added, completed

    with open(db_path, mode, newline="") as db_writer:
        vid_write = csv.writer(db_writer)
        vid_write.writerows(video_list)

