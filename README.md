# H.264 to H.265 transcoder

To be clear, this tool doesn't solve a new problem. Maybe you have some video files that use the H.264 format and you need/want to convert those files to H.265 for \<foo reason\>. There are a number of alternatives out there! To name only a few...
  
  * Tdarr
  * Handbrake
  * FFmpeg
  
In fact, these tools all utilize FFmpeg under the hood, aiming themselves at being very powerful and capable of serving many use cases. What makes **h264_to_h265 transcoder** different is that it focuses on doing just one thing - converting video files that use the H.264 format to H.265. No more, no less!
  
## Installation

1. `$ git clone https://github.com/apesch85/h264_to_h265.git`
2. `$ python3 -m venv h264_to_h265`
3. `$ cd h264_to_h265`
4. `$ source bin/activate`
5. `$ pip install -r requirements.txt`

## Usage
  
Because this tool does just one thing, usage is very simplified. No web front-ends to install, configure, and maintain! There are just 3 settings for you to configure at the time you run the tool -
  
* Number of concurrent transcoding jobs
  
  **Note**: H.265 transcoding is very CPU intensive! It is recommended to keep this number low. For example, an AMD Ryzen 7 5800X handles 3 threads really well. 4 is slightly too many.
  
* The path to the video files
* The path to the csv file tracking the status of the transcoding jobs
  
These configuration settings are set with command line flags. Example usage below -

```bash
  
$ python3 transcoder.py \
  --db_path=/home/user/vid_db.csv \
  --video_dir=/mnt/videos \
  --num_threads=3
```
  
To see details about these flags while using the tool, you can run -
  
`$ python3 transcoder.py --help`
