import numpy
from os.path import join as pjoin
import cv2
import os
import UIED.detect_compo.ip_region_proposal as ip


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))

# 调用此函数, 输出形如output_dir/dir_name/img_name.json

def img_rec(img_file_name,output_dir,dir_name):
    '''
        ele:min-grad: gradient threshold to produce binary map
        ele:ffl-block: fill-flood threshold
        ele:min-ele-area: minimum area for selected elements
        ele:merge-contained-ele: if True, merge elements contained in others
        text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
        text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

        Tips:
        1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
        2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
        3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
        4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    '''
    key_params = {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'merge-contained-ele':True,
                  'max-word-inline-gap':6, 'max-line-gap':1}

    os.makedirs(pjoin(output_dir, dir_name), exist_ok=True)
    # switch of the classification func
    classifier = None

    resized_height = resize_height_by_longest_edge(img_file_name)
    ip.compo_detection(img_file_name, output_dir, key_params,
                       classifier=classifier, resize_by_height=resized_height, show=True)


def abolish(img_file_name):
    ori_img = cv2.imread(img_file_name)
    # 转灰度图
    gray_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
    #
    ret, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    show(binary_img, "b")
    # # 闭运算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    # close_image = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel,iterations=10)
    # show(close_image, "c")
    # 膨胀 - 腐蚀
    eroded_img = cv2.erode(binary_img, kernel)
    show(eroded_img,"e")

    dilated_img = cv2.dilate(binary_img, kernel)
    show(dilated_img,"d")
    abs_img = cv2.absdiff(dilated_img, eroded_img)
    result = cv2.bitwise_not(abs_img)
    show(result, "r")
    # canny边缘检测
    canny_image = cv2.Canny(dilated_img, 127, 255, 0)
    show(canny_image, "c")
    # 轮廓提取 只提取外轮廓 只保留边界点
    contours, h = cv2.findContours(eroded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 寻找屏幕矩形边框
    vertex = []
    draw_img = ori_img.copy()
    for point in contours:
        x, y, w, h = cv2.boundingRect(point)
        vertex.append([x, y, w, h, w*h])
        cv2.rectangle(draw_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # target_index = heapq.nlargest(1, range(len(vertex)), vertex.__getitem__)[0]
    target_vertex = numpy.argmax(vertex, axis=0)
    x = target_vertex[1]
    y = target_vertex[2]
    w = target_vertex[3]
    h = target_vertex[4]
    # 绘制矩形
    # draw_img = ori_img.copy()
    ret = cv2.rectangle(draw_img, (x, y), (x + w, y + h), (0, 255, 0), -1)

    show(ret, 'ret')


def show(img,name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)
    cv2.waitKey(0)






# cfg = get_cfg()
# cfg.MODEL.DEVICE = "cpu"
# cfg.merge_from_file("./lib/detectron2/configs/COCO-Detection/faster_rcnn_R_50_C4_3x.yaml")
# cfg.DATASETS.TRAIN = ("train_dataset",)
# cfg.DATASETS.TEST = ('val_dataset',) # no metrics implemented for this dataset
# cfg.DATALOADER.NUM_WORKERS = 4 # 多开几个worker 同时给GPU喂数据防止GPU闲置
# cfg.MODEL.WEIGHTS = "detectron2://ImageNetPretrained/MSRA/R-50.pkl" # initialize from model zoo
# cfg.SOLVER.IMS_PER_BATCH = 4
# cfg.SOLVER.BASE_LR = 0.000025
# cfg.SOLVER.NUM_GPUS = 2
# cfg.SOLVER.MAX_ITER = 100000 # 300 iterations seems good enough, but you can certainly train longer
# cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128 # faster, and good enough for this toy dataset
# cfg.MODEL.ROI_HEADS.NUM_CLASSES = 29 # only has one class (ballon)
#
# # 训练集
# register_coco_instances("train_dataset", {}, "data/train.json", "data/img")
# # 测试集
# register_coco_instances("val_dataset", {}, "data/val.json", "data/img")
#
# import os
# os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
#
# class Trainer(DefaultTrainer):
#     @classmethod
#     def build_evaluator(cls, cfg, dataset_name, output_folder=None):
#         ### 按需求重写
#
#     @classmethod
#     def test_with_TTA(cls, cfg, model):
#         ### 按需求重写
#
# trainer = Trainer(cfg)
# trainer.resume_or_load(resume=True)
# trainer.train()

img_rec("img/input/test10.jpg","img/output","test")
