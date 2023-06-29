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
        # video_name = vp.split("/")[-1][:-4]
        vidcap = cv2.VideoCapture(vp)
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        _w = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        _h = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        filename = vp.split("/")[-1].split(".")[0]
        out = cv2.VideoWriter(opt.save_dir+filename+".mp4",cv2.VideoWriter_fourcc(*'DIVX'), fps, (_w,_h))
        file = open("/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/annotations/"+filename+".txt",'r')
        anno = file.readlines()
        success,image = vidcap.read()
        count = 0
        while success:
            params = anno[count].split(' ')
            obj_cnt = int(params[1])
            for idx in range(obj_cnt):
                x_left = int(params[idx*5 + 2])
                y_top = int(params[idx*5 + 3])
                w = int(params[idx*5 + 4])
                h = int(params[idx*5 + 5])

                if x_left + w/2 < 0 or y_top + h/2 < 0:
                    continue
                
                if x_left < 0:
                    w = x_left + w//2
                    x_left = 0
                
                if y_top < 0:
                    h = y_top + h//2
                    y_top = 0

                image = cv2.rectangle(image,(x_left,y_top),(x_left+w,y_top+h),(0,255,0),3)
            out.write(image)
            success,image = vidcap.read()
            count += 1
        file.close()
        out.release()

    print("all convert finish!!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_dir', type=str, help='path to video directory')
    parser.add_argument('--save_dir', type=str, help='path to save image directory')
    opt = parser.parse_args()
    video_paths = glob.glob(opt.video_dir+"/*")
    # video2image(video_paths)
    process = []
    for i in range(7):
        process.append(video_paths[i*10:(i+1)*10])
    process.append(video_paths[70:])
    pool = Pool(processes = 8)
    pool.map(video2image, process)
    pool.close()
    pool.join()
    print("----finish----")