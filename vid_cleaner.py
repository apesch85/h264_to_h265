#! /usr/bin/python3

import glob
import os
import logging
import psutil


def CleanFiles(processed_files):
    for file_name in processed_files:
        file_ext = file_name[-4:]
        base_name = file_name[:-8]
        original_name = base_name + file_ext
        if checkIfProcessRunning(base_name):
            print('File is being processed. Standing down: %s' % file_name)
        else:
            try:
                os.remove(original_name)
                print('Removed file: %s' % original_name)
            except Exception as e:
                logging.warning(
                  'File not removed.'
                  'It might still be in processing: %s' % original_name)
                logging.info(e)
                
                
def CleanFile(processed_file):
  if checkIfProcessRunning(processed_file):
    print('File is being processed. Standing down: %s' % processed_file)
  else:
    try:
      os.remove(processed_file)
      print('Removed file: %s' % original_name)
    except Exception as e:
      logging.warning(
        'File not removed.'
        'It might still be in processing: %s' % processed_file)
      logging.info(e)


def checkIfProcessRunning(processName):
    '''Check if there is an active process that with processName.'''

    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
