# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 23:10:48 2021

@author: ctimmy
"""
import re
import glob
import cv2
import numpy as np
import argparse
import torchvision.transforms as t
from PIL import Image
from pathlib import Path

def collect_video(name = "video.mov"):
    """
    Read each frame of video NAME

    :name: str
    -> List[Image]
    """
    collection_list = []
    vidcap = cv2.VideoCapture(name)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("length: ", frame_count)
    for i in range(frame_count):  
        success, img = vidcap.read()
        collection_list.append(cv2image(img))
        print("Read frame: ", i, success)
    return collection_list

def collect_gif(name):
    """
    Read each frame of GIF NAME
    
    :name: str
    -> List[Image]
    """
    collection_list = []
    gif = Image.open(name)
    for i in range(gif.n_frames):
        gif.seek(i)
        img = gif.convert('RGB')
        collection_list.append(img)
    return collection_list

def collect_folder(path="image"):
    """
    Collect .jpg from path. We use regex to make numerial order of file

    :path: str
    -> List[Image]
    """
    collection_list = []
    p = Path(path)
    files = glob.glob(str(p / "*.jpg"))
    files = sorted(files, key=lambda x: int(re.findall(r'[0-9]+', x)[0]))
    for name in files:
        print(name)
        img = Image.open(name)
        collection_list.append(img)
    print("Make sure the name on terminal is well ordered")
    return collection_list

def cv2image(img):
    """
    Default channel of cv2 and Image is not the same. The function make sure 
    that desired Image has the correct form.

    :img: np.array
    -> Image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)

def write_set(collection_list, name):
    """
    :collection_list: list of PIL Image
    :name: name of the written file
    """
    for i, img in enumerate(collection_list):
        img = np.array(img)
        img[:, :, [0, 2]] = img[:, :, [2, 0]]
        cv2.imwrite("image/%s_frame_%d.jpg" %(name, i), img)

def make_transparent_gif(name, collect_list, spf=20):
    """
    Note that the image need to be a transparent png
    """
    collect_list = [x.convert('PA') for x in collect_list]
    collect_list[0].save(name + "trans.gif", 
                         format='GIF', 
                         save_all=True, 
                         optimize=False, 
                         append_images=collect_list[1:], 
                         duration=spf, 
                         disposal=2, 
                         loop=0, 
                         transparency=0)

def make_gif(name, collect_list, spf=20):
    collect_list[0].save(name + ".gif", 
                         format='GIF', 
                         save_all=True, 
                         optimize=False, 
                         append_images=collect_list[1:], 
                         duration=spf,
                         loop=0)

def rotate(img, timestamp, deg):
    deg = deg * timestamp
    img = t.functional.rotate(img, deg)
    return img.convert('RGB')

def horizontal_moving(img, timestamp, offset):
    offset = offset * timestamp
    img = np.array(img)
    h, w, c = img.shape
    img_tmp = np.zeros_like(img)
    img_tmp[:, :w-offset, :] = img[:, offset:, :]
    img_tmp[:, w-offset:, :] = img[:, :offset, :]
    img = Image.fromarray(img_tmp).convert('RGB')
    return img

def vertical_moving(img, timestamp, offset):
    offset = offset * timestamp
    img = np.array(img)
    h, w, c = img.shape
    img_tmp = np.zeros_like(img)
    img_tmp[:h-offset, :, :] = img[offset:, :, :]
    img_tmp[h-offset:, :, :] = img[:offset, :, :]
    img = Image.fromarray(img_tmp).convert('RGB')
    return img

class cosine_offset:
    def __init__(self, constant, time_len):
        self.constant = constant
        self.freq = 360 / time_len

    def __mul__(self, timestamp):
        return abs(int(self.constant * np.cos(np.radians(timestamp * self.freq))))
    
class sine_offset:
    def __init__(self, constant, time_len):
        self.constant = constant
        self.freq = 360 / time_len

    def __mul__(self, timestamp):
        return int(self.constant * np.sin(np.radians(timestamp * self.freq)))

if __name__ == "__main__":
    """
    More detail about the args:
    https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    https://pillow.readthedocs.io/en/stable/reference/Image.html

    duration: millisecond per frame
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=str, default="demo.png")
    args = parser.parse_args()
    
    img = Image.open(args.n).convert('P')
    collection_list = []
    time_len = 20
    deg = 360 / time_len
    offset = img.size[0] // time_len
    r_offset = sine_offset(40, time_len)
    v_offset = cosine_offset(100, time_len)
    for i in range(time_len):
        img_tmp = rotate(img, i, r_offset)
        img_tmp = horizontal_moving(img_tmp, i, offset)
        img_tmp = vertical_moving(img_tmp, i, v_offset)
        collection_list.append(img_tmp)
    
    # we can write images and use collect_list to obtain the same result after
    write_set(collection_list, args.n)
    collection_list = collect_folder("image")
    
    # we can also obtain the same result by
    # collection_list = collect_gif(name)

    # or we can obtain a list from video by
    # collections_list = collect_video(name)

    make_gif(args.n, collection_list, 30)