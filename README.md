# USC DEN 视频下载小工具

## 依赖的包和软件
- 运行环境：mac/linux
- `Python 3`
- `ffmpeg` (mac下建议用homebrew安装)
- Python三方包: `requests` (通过pip或者conda安装): `pip3 install requests` 或者 `conda install requests`
- Python三方包: `selenium` (通过pip或者conda安装): `pip3 install selenium` 或者 `conda install selenium`
- `selenium`使用的浏览器驱动(安装方法见下)
#### 关于selenium浏览器驱动
Chrome驱动，[下载地址](https://sites.google.com/a/chromium.org/chromedriver/)。
将解压后的文件移动到`/usr/loacl/bin`目录中.

## 使用方法
可以采用`Run All`或`Run by Steps`。
#### Run All
1. 在项目根文件夹中新建`config.json`文件(可通过去掉`config.json.sample`文件中的`.sample`后缀获取)并录入以下信息:
    - 登录DEN的`username`
    - 登录DEN的`password`
    - 课程的`course_id`
2. 执行`./run.sh`
#### Run by Steps:
1. 在项目根文件夹中新建`config.json`文件(可通过去掉`config.json.sample`文件中的`.sample`后缀获取)并录入以下信息:
    - 登录DEN的`username`
    - 登录DEN的`password`
    - 课程的`course_id`
2. 执行`python parser.py`获得视频解析之后的链接`urlOfVideos.json`。
3. 执行`python downloader.py`下载视频

#### 关于config.json
`config.json`示例：
```json
{
    "username": "abc@usc.edu",
    "password": "abcdefg",
    "course_id": "13177"
}
```
`URL`图示:
![网页示例](./resource/the_link.png)