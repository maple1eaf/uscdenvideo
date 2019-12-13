# USC DEN 视频下载小工具

## 依赖的包和软件
- `Python 3`
- `ffmpeg` (mac下建议用homebrew安装)
- Python三方包: `requests` (通过pip或者conda安装)
- Python三方包: `selenium` (开发用的3.141.0版本，通过pip或者conda安装)
- `selenium`使用的浏览器驱动
#### 关于selenium浏览器驱动
开发用的Chrome驱动，[下载地址](https://sites.google.com/a/chromium.org/chromedriver/)
    - win: 将解压后的文件放入配置了环境变量的文件夹, 如python的文件夹.
    - mac/linux: 将解压后的文件移动到`/usr/loacl/bin`目录中.

## 使用方法
1. 在`urlPageContainVideo.json`中录入DEN中含有要下载视频的网页。
    - 网页示例: ![](./resource/the_link.png)
2. 在`parser.py`中输入`USER_NAME`和`PASSWORD`。
3. 执行`python parser.py`获得视频解析之后的链接`urlOfVideos.json`。
4. 执行`python downloader.py`下载视频

#### 关于config.json
- `URL`列表是一个`Array`
- 如果某个星期没有DEN（例如放假），用空字符串代替: `""`

`config.json`示例：
```json
[
    "https://courses.uscden.net/d2l/le/content/13177/viewContent/195596/View",
    "",
    "https://courses.uscden.net/d2l/le/content/13177/viewContent/195596/View"
]
```