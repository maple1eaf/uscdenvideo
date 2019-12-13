import os
import json

# load urls
urlDirectVideos = []
with open("urlOfVideos.json", "r", encoding="utf-8") as f:
    urlDirectVideos = json.load(f)

def downloadVideos(weeks):
    urls = urlDirectVideos
    n = len(urls)
    dir_name = ['week_%.2d' % (x) for x in range(1,n+1)] # week_01 week_02
    file_name = ['week_%.2d.mp4' % (x) for x in range(1,n+1)] # week_01.mp4

    for i in weeks:
        i = i-1
        url_ = urls[i]
        if url_ == '':
            continue
        dir_ = dir_name[i]
        file_ = file_name[i]

        mkdir_dir = 'mkdir %s' % (dir_) # 'mkdir week_01'
        try:
            os.system(mkdir_dir)
        except:
            print('%s exists.' % (dir_))

        full_file_ = './%s/%s' % (dir_, file_) # ./week_01/week_01.mp4
        command_ = 'ffmpeg -i %s -c copy %s' % (url_, full_file_)
        os.system(command_)

# 设置需要下载哪些周的视频 1-15周
# weeks = list(range(2,16))
# weeks = [1]
weeks = list(range(1,len(urlDirectVideos)+1))
downloadVideos(weeks)






