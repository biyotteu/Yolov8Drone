import cv2
import argparse
import glob
from tqdm import tqdm
import os

def video2image(opt):
    video_paths = glob.glob(opt.video_dir+"/*")
    for vp in tqdm(video_paths):
        video_name = vp.split("/")[-1][:-4]
        vidcap = cv2.VideoCapture(vp)
        success,image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite(os.path.join(opt.save_dir,video_name+"_%05d.jpg" % count), image)     # save frame as JPEG file
            success,image = vidcap.read()
            count += 1

    print("all convert finish!!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_dir', type=str, help='path to video directory')
    parser.add_argument('--save_dir', type=str, help='path to save image directory')
    opt = parser.parse_args()

    video2image(opt)