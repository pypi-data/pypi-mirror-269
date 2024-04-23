import os

import cv2

from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.models import RAMA_NO_SPRING_DETECT_MODEL_ADDRESS
from data.result.Class_im import Class_im
from data.result.Rect import Rect

"""main module for user"""
from data.neuro.Rama_classify_class import Rama_classify_class


class Danila:
    """main class for user"""
    def __init__(self, yolov5_dir):
        self.rama_classify_model = Rama_classify_class()
        yolo_path = yolov5_dir
        rama_no_spring_detect_model_path = RAMA_NO_SPRING_DETECT_MODEL_ADDRESS
        self.rama_no_spring_detect_model = Rama_detect_class(rama_no_spring_detect_model_path, 'rama_no_spring_detect', yolo_path)


    # returns string - class of rama using CNN network
    # img - openCV frame

    def rama_classify(self, img):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        # img = cv2.imread(img_path)
        class_im = self.rama_classify_model.classify(img)
        return class_im.name

    # returns openCV frame with rama from openCV frame\
    def rama_detect(self, img):
        """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
        new_img = img.copy()
        os.remove('initial_image.jpg')
        cv2.rectangle(new_img, (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), (0, 0, 255), 2)
        cv2.putText(new_img, class_im.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        return new_img

    # # returns image_path in danilav1 root with cut_rama
    # def rama_cut(self, image_path):
    #     img = cv2.imread(image_path)
    #     class_im = self.rama_classify_model.classify(img)
    #     rect = Rect()
    #     if (class_im == Class_im.rama_spring):
    #         rect = self.rama_spring_detect_model.rama_detect(image_path)
    #     else:
    #         rect = self.rama_no_spring_detect_model.rama_detect(image_path)
    #     img_res = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
    #     img_path_res = 'rama_cut_result.jpg'
    #     cv2.imwrite(img_path_res, img_res)
    #     return img_path_res
    #
    #
