# danila_lib
 python library for Danila

# To install project made 
    pip install danila-lib

# To use in your project 
    from danila.danila import Danila

# All use methods are in 
    class Danila

# returns string - class of rama, img - openCV frame
    def rama_classify(self, img):

# returns openCV frame with rama from openCV frame\
    def rama_detect(self, img):


# in package data/neuro there is module Rama_classify_class
    class Rama_classify_class

# reads CNN taught model and includes it in class example
    def __init__():

# makes grey NumPy Array(1,512,512) of doubles[0..1] from openCV image
    def prepare_img(img : openCV frame): NumPy Array(1,512,512)[0..1]

# classify openCV img with CNN, returns list with double[0..1] values 
    def work_img(img : openCV frame): Double[0..1] list

# classify openCV img with CNN, returns Class_im
    def classify(img : openCV frame): Class_im

# in package data/neuro there is module Rama_detect_class
    class Rama_detect_class
# reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, model_path, model_name, yolo_path):
# получить JSON с результатами yolo
    def work_img(self, img_path):
# получить координаты прямоугольника с рамой
    def rama_detect(self, img_path):
# in package data/result Rect module for rectangle operations
# прочитать из json результата йоло
    @staticmethod
    def get_rect_from_yolo_json(yolo_json):
# makes Rect object from xmin, xmax, ymin, ymax
    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
# Найти IOU между этим прямоугольником и другим, данным в объекте
    def IoU(self, rect):
# makes string from object
    def __str__(self):

# find intersection square between object and other rectangle
    def intersection(self, rect):
# find union RECT between object and other rectangle
    def union(self, rect):
# in package data/result Class_im
    class Class_im(Enum):
        rama_no_spring = 0
        rama_spring = 1


# exapmles of using you can find 
https://github.com/Arseniy-Zhuck/danila_lib_demo