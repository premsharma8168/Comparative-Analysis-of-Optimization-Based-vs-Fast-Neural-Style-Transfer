import cv2
import time
import os
import numpy as np

def fast_nst(content_path, model_path, output_path):
    start_time = time.time()
    net = cv2.dnn.readNetFromTorch(model_path)
    image = cv2.imread(content_path)
    if image is None:
        raise ValueError(f"Could not load image at {content_path}")
    
    h, w = image.shape[:2]
    target_width = 800
    target_height = int(h * (target_width / w))
    image = cv2.resize(image, (target_width, target_height))
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (target_width, target_height),
                                 (103.939, 116.779, 123.680), swapRB=False, crop=False)
    net.setInput(blob)
    out = net.forward()
    
    out = out.reshape(3, out.shape[2], out.shape[3])
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.680
    out /= 255.0
    out = out.transpose(1, 2, 0)
    out = np.clip(out, 0.0, 1.0) * 255
    out = out.astype(np.uint8)
    
    cv2.imwrite(output_path, out)
    return time.time() - start_time
