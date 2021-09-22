import numpy as np
import cv2 as cv
import os

# path = os.getcwd()+"/../images"
# print(f'{path = }')

class Stitcher:
    def __init__(self, imgs_path):
        self.path = imgs_path
    
    def run(self):
        files = os.listdir(self.path)
        images = []
        FilesToStitch = [file for file in files if file.startswith('Image')]
        for i in FilesToStitch:
            img = cv.imread(os.path.join(self.path, i))
            images.append(img)

        print(f"Images to stitch: {FilesToStitch}")
        stitcher = cv.Stitcher.create()
        (status, result) = stitcher.stitch(images)

        if (status == cv.STITCHER_OK):
            print("Stitcher succesful!")
        else:
            print("Stitcher unsuccesful!")

        cv.imwrite(os.path.join(self.path, "Stitch_result.jpg"), result)

"""
cv.imshow("pano", result)
cv.waitKey(0)
cv.destroyAllWindows()
"""
