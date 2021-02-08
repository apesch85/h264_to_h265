import os


def GetFiles(dir_path):
    # traverse root directory, and list directories as dirs and files as files
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append('%s/%s' %(root, file))

    return file_list


def FilterFiles(file_list):
    file_filter = ['mov', 'mkv', 'mp4', 'avi']
    video_list = [video for video in file_list if video[-3:] in file_filter]
    
    correct_path = [video for video in video_list if os.path.isfile(video)]
    broken_path = [video for video in video_list if video not in correct_path]

    return (correct_path, broken_path)


