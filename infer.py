from ultralytics import YOLO
from glob import glob
import argparse
import os
from tqdm import tqdm
from PIL import Image, ImageDraw

if __name__ == '__main__':
    # 수정 요함
    # -------------------------------------------------------------------------
    # rgb 이미지 모델 경로
    model_rgb_path = 'C:/Users/PC/Desktop/제출1/weight/last_fit.pt'
    # ir 이미지 모델 경로
    model_ir_path = 'C:/Users/PC/Desktop/제출1/weight/best_ir_2.pt'
    # test 이미지 디렉토리 위치 (주의 문자열 마지막에 '/' 붙이지 말것)
    img_dir_path = 'C:/Users/PC/Desktop/dataset/dataset/test/image'
    # 디렉토리 구분자 linux => /, windows => \\
    divider = '\\'
    # 저장 파일 이름
    save_file_name = "미래지능정통교_submission.txt"
    # -------------------------------------------------------------------------
    
    img_dir = sorted(glob(img_dir_path + '/*.jpg'))
    model_rgb = YOLO(model_rgb_path)
    model_ir = YOLO(model_ir_path)
    
    with open(save_file_name,'w') as f:
        for path in tqdm(img_dir):
            filename = path.split(divider)[-1]
            results = []
            
            if int(filename.replace(".jpg","")) < 20000:
                results = model_rgb(path, imgsz=640, conf = 0.001, iou = 0.6, verbose=False)
            else:
                results = model_ir(path, imgsz=640, conf = 0.2, iou = 0.6, verbose=False)

            boxes = results[0].boxes
            boxes = sorted(boxes, key=lambda x: x.conf[0], reverse=True)

            if len(boxes) > 0:
                if int(filename.replace(".jpg","")) > 20000:
                    boxes = boxes[:1]

                for idx, box in enumerate(boxes):
                    if idx > 0 and box.conf[0].item() < 0.25:
                        break
                    x, y, w, h = box.xywh[0].tolist()
                    conf = box.conf[0].item()
                    f.write("'%s', %d, %d, %d, %d, %f, 1\n"%(filename, round(x - w/2), round(y - h/2), round(w), round(h),conf))
            else:
                f.write("'%s', 0, 0, 0, 0, 0, 0\n"%(filename))