import cv2
import argparse
import glob
from tqdm import tqdm
import os
from multiprocessing import Pool

opt = None
def video2image(video_paths):
    global opt
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
    video_paths = glob.glob(opt.video_dir+"/*")
    process = []
    for i in range(7):
        process.append(video_paths[i*2:(i+1)*2])
    # process.append(video_paths[70:])
    pool = Pool(processes = 8)
    pool.map(video2image, process)
    pool.close()
    pool.join()
    print("----finish----")