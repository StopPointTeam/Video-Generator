# Video-Generator

为 STM32-Player (https://github.com/StopPointTeam/STM32-Player) 生成视频

基于 OpenCV，对普通格式的视频进行逐帧处理，生成可由 STM32-Player 播放的 .32v 文件

### 使用方法

+ 使用命令行运行。可以通过 Python 使用 ``py VideoGen.py`` 命令运行，也可以直接调用打包好的二进制 exe 文件
+ 命令行参数：
  + -i 指定输入视频
  + -h 为帮助

### 依赖

+ cv2
+ numpy
+ struct
+ argparse
