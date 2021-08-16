import cv2
import numpy as np
import struct
import sys
import os
import argparse


def BGR888_2_RGB565(img):
    '''BGR888 转化为 RGB565

    Arguments:
        - img -- 待转化的 numpy 数组
    '''

    img_B = img[:, :, 0]
    img_G = img[:, :, 1]
    img_R = img[:, :, 2]
    img_RGB565 = ((img_B & 0xF8) >> 3) | (
        (img_G & 0xFC) << 3) | ((img_R & 0xF8) << 8)
    return img_RGB565.flatten()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='生成供 STM32-Player (https://github.com/StopPointTeam/STM32-Player) 播放的视频')
    parser.add_argument('-i', '-input', help='输入视频路径')
    arg = vars(parser.parse_args())

    if os.path.exists(arg['i']) == False:
        print('输入视频路径不存在，请检查路径！')
        sys.exit(1)

    cap = cv2.VideoCapture(arg['i'])
    if cap.isOpened() == False:
        print('打开输入视频失败！')
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print('输入视频分辨率:', frame_width, '*', frame_height)
    print('输入视频 FPS:', fps)
    print('输入视频总帧数:', round(frame_count))
    print('输入视频时长:', round(frame_count / fps, 2), 's')

    if fps > 30:
        frame_interval = int(fps / (fps - 30))
        fps = 30
        print('输入视频 FPS 超过 30，将自动转换为 30')
    else:
        frame_interval = 0

    frame_seq = 0  # 输入视频帧序号
    new_seq = 0  # 输出视频帧序号

    # 保存到二进制文件中
    filename = os.path.basename(arg['i']) + '.32v'
    file = open(filename, 'wb')
    file.seek(153600, os.SEEK_SET)

    while True:
        ret, img = cap.read()  # 捕获一帧
        if ret == True:
            frame_seq += 1
            if (frame_interval == 0 or frame_seq % frame_interval != 0):
                new_seq += 1

                # 变换尺寸，并转化为 uint16 类型 numpy 数组
                img_resized = np.array(cv2.resize(
                    img, (320, 240))).astype('uint16')

                img_RGB565 = BGR888_2_RGB565(img_resized)  # 颜色空间转换

                fmt = '>' + len(img_RGB565) * 'H'  # 格式化字符串，大端模式
                data = struct.pack(fmt, *img_RGB565)  # 列表转换为二进制字节流

                file.write(data)
                print('正在处理：第', frame_seq, '/', round(frame_count), '帧，进度：',
                      round(frame_seq / frame_count * 100, 2), '%')

        else:
            # 写入视频信息头
            file.seek(0, os.SEEK_SET)
            file.write(struct.pack('<dI', fps, int(new_seq)))  # 小端模式
            print('处理完成，输出视频共', new_seq, '帧, FPS 为', fps)
            break
