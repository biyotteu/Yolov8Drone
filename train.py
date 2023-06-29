# from ultralytics import YOLO
from ultralytics import YOLO
import wandb
import argparse

wandb.login(key="25f9a4d45af7f2e6899294620bffa4be42f15b47")

wandb.init(
    project="Yolov8",
    name="DroneRgbFit",
    entity="biyotteu",   
)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--path',type=str,default='')
    # parser.add_argument('--model',type=str,default='yolov8x.pt')
    # args = parser.parse_args()

    model = YOLO("/home/ubuntu/dev/repos/YoloV8/Yolov8/DroneRGB/weights/best.pt")
    model.train(data="/home/ubuntu/dev/repos/YoloV8/fit.yaml",project="Yolov8",name="DroneRgbFit",epochs=200, imgsz=640, batch=16)
