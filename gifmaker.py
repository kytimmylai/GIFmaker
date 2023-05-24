# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 23:10:48 2021

@author: ctimmy
"""
import re
import glob
import cv2
import numpy as np
from PIL import Image
import argparse
import torchvision.transforms as t

def collect_video(name = 'video.mov'):
    collection_list = []
    vidcap = cv2.VideoCapture(name)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('length: ', frame_count)
    for i in range(frame_count):  
        success, img = vidcap.read()
        collection_list.append(cv2image(img))
        print('Read frame: ', i, success)
    return collection_list

def collect_gif(name):
    collection_list = []
    gif = Image.open(name)
    for i in range(gif.n_frames):
        gif.seek(i)
        img = gif.convert('RGB')
        collection_list.append(img)
    return collection_list

def collect_folder():
    """
    To convenient, we have a default folder and img name.
    Make sure output order is right.
    """
    collection_list = []
    files = glob.glob('image/*.jpg')
    files = sorted(files, key=lambda x: int(re.findall(r'[0-9]+', x)[0]))
    for name in files:
        print(name)
        img = Image.open(name)
        collection_list.append(img)
    return collection_list

def cv2image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)

def write_set(collection_list, name):
    """
    collection_list: list of PIL Image
    """
    for i, img in enumerate(collection_list):
        img = np.array(img)
        img[:, :, [0, 2]] = img[:, :, [2, 0]]
        cv2.imwrite("image/%s_frame_%d.jpg" %(name, i), img)

def make_transparent_gif(name, collect_list, spf=20):
    collect_list[0].save(name + ".gif", 
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
    
    img = Image.open(args.n)
    collection_list = []
    for i in range(20):
        deg = -i*18
        img0 = t.functional.rotate(img, deg)
        collection_list.append(img0.convert('RGB'))
        
    collection_list = collect_gif("demo.png.gif")
    write_set(collection_list, "demo")
    collection_list = collect_folder()
    make_gif(args.n, collection_list, 20)