"""

https://github.com/ternaus/retinaface
pip install -U retinaface_pytorch


"""
import cv2
from retinaface.pre_trained_models import get_model


class Retina_Face_Detection:
    def __init__(self):
        self.model = get_model("resnet50_2020-07-20", max_size=2048)
        self.model.eval()

    def detect(self, image, return_crops=False, return_keypoints=False, draw_bbox=False,draw_keypoint=False):
        
        bboxes      = []
        crops       = []
        keypoints   = []
        image_copy = image.copy() if return_crops else None

        output = self.model.predict_jsons(image)

        for out in output:
            x1,y1,x2,y2 = int(out['bbox'][0]),int(out['bbox'][1]),int(out['bbox'][2]),int(out['bbox'][3])
            keypoint    = out['landmarks']
            keypoint    = [ (int(item[0]),int(item[1])) for item in keypoint]

            bboxes.append([x1,y1,x2,y2])
            if return_keypoints:
                keypoints.append(keypoint)
            if return_crops:
                crop    = image_copy[y1:y2 , x1:x2]
                crops.append(crop)
            if draw_bbox:
                start_point = (x1, y1)
                end_point   = (x2, y2)
                color       = (0, 0, 255)
                thickness   = 2
                image       = cv2.rectangle(image, start_point, end_point, color, thickness)
            if draw_keypoint:
                for key in keypoint:
                    center_coordinates = (key[0], key[1]) 
                    radius = 2
                    color = (255, 0, 0) 
                    thickness = -1
                    image = cv2.circle(image, center_coordinates, radius, color, thickness) 

        return image, bboxes, keypoints, crops 