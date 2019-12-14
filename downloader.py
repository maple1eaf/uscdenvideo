import os
import json

# load urls
videos = []
with open("urlOfVideos.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

def downloadVideo(item):
    """
    item = {
            "foldername": ...,
            "filetitle": ...,
            "url": ...
        }
    """
    # check dir, if not exist, create one
    dir_ = item["foldername"].replace('/', ':')
    file_ = item["filetitle"].replace('/', ':') + '.mp4'
    url_ = item["url"]

    if not os.path.exists('result/'):
        os.mkdir('result')

    mkdir_dir = 'mkdir "result/%s"' % (dir_) # 'mkdir result/week_01'
    try:
        os.system(mkdir_dir)
    except:
        print('%s exists.' % (dir_))

    # full_filename
    full_file_ = './result/%s/%s' % (dir_, file_) # ./result/week_01/week_01.mp4
    # download
    command_ = 'ffmpeg -i %s -c copy "%s"' % (url_, full_file_)
    print(command_)
    os.system(command_)

for video in videos:
    downloadVideo(video)






