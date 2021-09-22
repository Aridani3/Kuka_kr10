import numpy as np
import cv2 as cv
from skimage import feature
import os
from scipy.spatial import distance as dist
import stitch 

class ImageFilter:
    def __init__(self, images_path):
        self.path = images_path

    @staticmethod
    def reorder(pts):
        # roerder bounding box points
        xSorted = pts[np.argsort(pts[:, 0]), :]
        # grab the left-most and right-most points from the sorted x-roodinate points
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost
        # Calculate the Euclidean distance between the
        # top-left and right-most points; by the Pythagorean
        # theorem, the point with the largest distance will be
        # our bottom-right point
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        # return the coordinates in top-left, top-right,
        # bottom-right, and bottom-left order
        return np.array([tl, tr, br, bl], dtype="float32")

    def extract(self):
        Stitch = stitch.Stitcher(self.path)
        Stitch.run()

        img = cv.imread(os.path.join(self.path, 'Stitch_result.jpg'))
        # img = cv.resize(img, (img.shape[1]//2, img.shape[0]//2), interpolation = cv.INTER_AREA)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Define range of color in HSV to filter background gray
        lower = np.array([1,22,0])
        upper = np.array([179,255,129])
        # Threshold the HSV image 
        mask = cv.inRange(hsv, lower, upper)
        se =  cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, se)
        # cv.imshow("mask", mask)
        
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(img,img, mask= mask)
        # cv.imshow("res", res)

        # Image to gray scale to extarct contours
        gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        gray = np.where(gray>0,0,255).astype(np.uint8)
        # cv.imshow('gray',gray)

        # Contours
        edges = cv.Canny(image=gray, threshold1=100, threshold2=200) 
        contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        r = cv.cvtColor(edges,cv.COLOR_GRAY2RGB)

        # cv.drawContours(r, contours, -1, 255, 1)
        c = max(contours, key = cv.contourArea)
        #angle rectangle
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # Crop - final
        width, height = rect[1]
        pts1 = ImageFilter.reorder(box)
        pts2 = np.float32([[0,0],[width,0],[width, height],[0,height]])
        M = cv.getPerspectiveTransform(pts1,pts2)
        dst = cv.warpPerspective(img,M,(int(width),int(height)))

        # Draw bounding box ot the result on original stitched image
        cv.drawContours(img,[box],0,(0,0,255),2)
        # cv.imshow('img', img)

        print(f"Result's shape: {dst.shape}")
        cv.imwrite(os.path.join(self.path, "Result.jpg"), dst)

        return dst


if __name__ == "__main__":
    path = path = os.getcwd()+"/../images"
    # Filter = 
    result = ImageFilter(path).extract()
    # Fitler.extract()

    cv.imshow("Result", result)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
