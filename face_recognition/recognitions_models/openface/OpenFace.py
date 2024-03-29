import os 
import cv2 
import torch 
import numpy as np 
from face_recognition.recognitions_models.openface.model import netOpenFace
from face_recognition.recognitions_models.openface.check_weight import check_weight_exists
class OpenFace:
    def __init__(self):
        self.useCuda = True if torch.cuda.is_available() else False
        self.device  = torch.device(f"cuda" if self.useCuda else "cpu")
        weight_path = check_weight_exists()
        self.model = netOpenFace(self.device).to(self.device)
        self.model.load_state_dict(torch.load(weight_path))
        
        self.model.eval()
    
    def preprocess(self,image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (96, 96), interpolation=cv2.INTER_LINEAR)
        image = np.transpose(image, (2, 0, 1))
        image = image.astype(np.float32) / 255.0 
        input = torch.from_numpy(image).unsqueeze(0)
        if self.useCuda:
            input = input.to(self.device)
        return input 
    def predict(self,image):
        input = self.preprocess(image)
        embedding, _ = self.model(input) 
        return embedding

if __name__ == "__main__":
    openface = OpenFace()
    img = cv2.imread("./test_images/face.png")
    embedding = openface.predict(image=img)
    print(embedding.shape)
