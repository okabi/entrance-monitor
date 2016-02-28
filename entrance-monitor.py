import sys
import cv2
import urllib
import numpy as np
from datetime import datetime

DIR = "jpg/"
THRESHOLD = 5
BLUR = 7

def datetime_now():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def monitor(uri):
    stream = urllib.urlopen(uri)  # Stream from MJPG-Streamer
    filename = [datetime_now(), 0]# output JPG filename
    img_array = [None] * 3        # image history (recent 3)
    data = ''                     # Byte data got from `stream`
    while True:
        data += stream.read(1024)
        start = data.find('\xff\xd8')     # JPG Start
        end = data.find('\xff\xd9') + 2   # JPG End
        if start == -1 or end == 1:
            continue
        img = cv2.imdecode(
            np.fromstring(
                data[start:end], dtype=np.uint8),
            cv2.CV_LOAD_IMAGE_COLOR)
        data = data[end:]
        img_array = img_array[1:] + img_array[:1]
        img_array[len(img_array) - 1] = img
        if img_array[0] == None:
            continue
        diff, should_save = check_diff(
            img_array[0], img_array[1], img_array[2])
        if should_save:
            cv2.imwrite(
                "{0}{1}-{2}-{3:.3f}.jpg".format(
                    DIR, filename[0], filename[1], diff),
                img_array[1])
            filename[1] += 1
        now = datetime_now()
        if filename[0] != now:
            filename[0] = now
            filename[1] = 0

# ref. https://github.com/tanaka0079/python/blob/python/opencv/flame_sub.py
def check_diff(img1, img2, img3):
    diff = cv2.bitwise_and(
        cv2.absdiff(img1, img2),
        cv2.absdiff(img2, img3))
    mask_rgb = diff < THRESHOLD
    mask = np.empty(
        (img2.shape[0], img2.shape[1]),
        bool)
    for i, vi in enumerate(mask_rgb):
        for j, vj in enumerate(vi):
            mask[i][j] = mask_rgb[i][j][0] and mask_rgb[i][j][1] and mask_rgb[i][j][2]
    result = np.empty(
        (img2.shape[0], img2.shape[1]),
        np.uint8)
    result[:][:] = 255
    result[mask] = 0
    reslut = cv2.medianBlur(result, BLUR)
    hist = np.histogram(result, 2, range = (0, 255))
    value = float(hist[0][0]) / sum(hist[0])
    if value < 0.99:
        print '\033[91m' + str(value) + '\033[0m'
    else:
        print '\033[94m' + str(value) + '\033[0m'
    return value, value < 0.99

if __name__ == '__main__':
    monitor(sys.argv[1])
