import sys
import cv2
import urllib
import numpy as np
from datetime import datetime

DIR = "jpg/"
THRESHOLD = 5
BLUR = 7

def monitor(uri):
    stream = urllib.urlopen(uri) # Stream from MJPG-Streamer
    data = ''                    # Byte data got from `stream`
    filename = [
        datetime.now().strftime("%Y%m%d%H%M%S"),
        0]
    imgs = [None, None, None]
    while True:
        data += stream.read(1024)
        start = data.find('\xff\xd8') # JPG Start
        end = data.find('\xff\xd9')   # JPG End
        if start != -1 and end != -1:
            end += 2
            jpg = data[start:end]
            data = data[end:]
            img = cv2.imdecode(
                np.fromstring(jpg, dtype=np.uint8),
                cv2.CV_LOAD_IMAGE_COLOR)
            for i, value in enumerate(imgs):
                if value == None:
                    imgs[i] = img
                elif i == len(imgs) - 1:
                    imgs = imgs[1:] + imgs[:1]
                    imgs[len(imgs) - 1] = img
                    v, diff = checkDiff(
                        imgs[0], imgs[1], imgs[2])
                    if diff:
                        cv2.imwrite(
                            DIR + filename[0] + "-" + str(filename[1]) + "-" + str(v) + ".jpg",
                            imgs[1])
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            if filename[0] == now:
                filename[1] += 1
            else:
                filename[0] = now
                filename[1] = 0

# ref. https://github.com/tanaka0079/python/blob/python/opencv/flame_sub.py
def checkDiff(img1, img2, img3):
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
    hist = np.histogram(result, 2, range = (0, 255))
    value = float(hist[0][0]) / sum(hist[0])
    if value < 0.99:
        print '\033[91m' + str(value) + '\033[0m'
    else:
        print '\033[94m' + str(value) + '\033[0m'
    return value, value < 0.99

if __name__ == '__main__':
    monitor(sys.argv[1])
