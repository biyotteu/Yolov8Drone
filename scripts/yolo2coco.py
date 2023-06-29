import json
import argparse
import os
from tqdm import tqdm
from glob import glob
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolo_path', type=str, help='path of coco annotation directory')
    parser.add_argument('--save_path', type=str, help='path of save directory')
    parser.add_argument('--image_path', type=str, help='path of image directory')

    opt = parser.parse_args()

    yolo_path = opt.yolo_path
    save_path = opt.save_path

    out_data = {'categories': [dict(id=0, name='drone')],'images': [],'annotations': []}

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    yolo_paths = glob(os.path.join(yolo_path, '*.txt'))

    for yolo_file in tqdm(yolo_paths):
        with open(yolo_file, 'r') as f:
            lines = f.readlines()
        lines = [line.strip().split(' ') for line in lines]

        image_id = yolo_file.split('/')[-1].split('.')[0]
        image_name = image_id + '.jpg'
        image_path = os.path.join(opt.image_path, image_name)
        im = Image.open(image_path)
        W, H = im.size
        image = dict(file_name=image_name, height=H, width=W, id=image_id)
        out_data['images'].append(image)

        for line in lines:
            category_id = 0
            bbox_width = int(float(line[3]) * W)
            bbox_height = int(float(line[4]) * H)
            x_left = int(float(line[1]) * W - bbox_width/2)
            y_top = int(float(line[2]) * H - bbox_height/2)

            annotation = dict(image_id=image_id, category_id=category_id, bbox=[x_left, y_top, bbox_width, bbox_height], id=len(out_data['annotations']))
            out_data['annotations'].append(annotation)
    
    with open(os.path.join(save_path, 'annotations.json'), 'w') as f:
        json.dump(out_data, f)