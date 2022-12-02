import numpy as np
import cv2
import UIED.detect_compo.ip_region_proposal as ip


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))

# 调用此函数, 输出形如output_dir/dir_name/img_name.json

canny_low_threshold = 30
canny_high_threshold = 100
def img_rec(img_file_name,output_dir,dir):

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

    # os.makedirs(pjoin(output_dir, dir_name), exist_ok=True)
    # switch of the classification func
    classifier = None

    resized_height = resize_height_by_longest_edge(img_file_name)
    ip.compo_detection(img_file_name, output_dir, key_params,
                       classifier=classifier, resize_by_height=resized_height, show=True)


def abolish(img_file_name):
    ori_img = cv2.imread(img_file_name)

    # 高斯模糊(效果不好)
    gau_img = cv2.GaussianBlur(ori_img, (33, 33), 0)
    # show(ori_img, "g")

    # 转灰度图
    gray_img = cv2.cvtColor(gau_img, cv2.COLOR_BGR2GRAY)
    # 中值滤波
    gray_img = cv2.medianBlur(gray_img, 3)
    # # 转二值图
    # ret, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    # show(binary_img, "b")
    # # 闭运算

    # # show(close_image, "c")
    # # 膨胀 - 腐蚀
    # eroded_img = cv2.erode(binary_img, kernel)
    # show(eroded_img,"e")
    #
    # dilated_img = cv2.dilate(binary_img, kernel)
    # show(dilated_img,"d")
    # abs_img = cv2.absdiff(dilated_img, eroded_img)
    # result = cv2.bitwise_not(abs_img)
    # show(result, "r")

    # canny边缘检测
    canny_image = cv2.Canny(gray_img, canny_low_threshold, canny_high_threshold, 0)
    # show(canny_image, "c")

    # 直线检测
    # minLineLength = 50
    # maxLineGap = 10
    # lines = cv2.HoughLinesP(canny_image, 1, np.pi / 180, 40, np.array([]), minLineLength, maxLineGap)
    # a, b, c = lines.shape
    # new_img = ori_img.copy()
    # for i in range(a):
    #     cv2.line(new_img, (lines[i][0][0], lines[i][0][1]),
    #             (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
    #
    # show(new_img,"l")
    th = cv2.adaptiveThreshold(canny_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11,2)
    show(th, "th")
    # show(th, "th")
    # 轮廓提取 只提取外轮廓 只保留边界点
    contours, h = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    draw_img = ori_img.copy()
    cv2.drawContours(draw_img, contours, 1, (255,255, 0), 8)
    show(draw_img,"d")
    print(contours[1])

    # 寻找屏幕矩形边框
    vertex = []
    draw_img = ori_img.copy()
    for point in contours:
        x, y, w, h = cv2.boundingRect(point)
        vertex.append([x, y, w, h, w*h])
        cv2.rectangle(draw_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    target_vertex = np.argmax(vertex, axis=0)
    x = target_vertex[1]
    y = target_vertex[2]
    w = target_vertex[3]
    h = target_vertex[4]
    # 绘制矩形
    draw_img = ori_img.copy()
    ret = cv2.rectangle(draw_img, (x, y), (x + w, y + h), (0, 255, 0), -1)
    show(ret, 'canny_image')

def show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)
    cv2.waitKey(0)


# def is_similar(first_img_path, second_img_path):
#     img1 = cv2.imread(first_img_path)
#     img2 = cv2.imread(second_img_path)
#
#     H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
#     H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)
#     H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
#     H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)
#
#     similarity = cv2.compareHist(H1, H2 , 0)
#     if similarity > 0.5:
#         return True
#     return False

def is_similar(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    w1, h1 = img1.shape
    w2, h2 = img2.shape
    img1 = cv2.resize(img1, (h1, w1))
    img2 = cv2.resize(img2, (h2, w2))
    # 初始化ORB检测器
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # 提取并计算特征点
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # knn筛选结果
    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
    # 查看最大匹配点数目
    good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    similary = float(len(good)) / len(matches)
    if similary > 0.5:
        return True
    else:
        return False


def manual(file_path):
    img = cv2.imread(file_path)
    print('鼠标选择ROI,然后点击 enter键')
    cv2.namedWindow('cv2.selectROI', cv2.WINDOW_NORMAL)
    r = cv2.selectROI('cv2.selectROI', img, True, False)

    roi = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    cv2.namedWindow('roi', cv2.WINDOW_NORMAL)
    cv2.imshow('roi', roi)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

# img_rec("img/input/test111.jpg","img/output","test")
# abolish("img/input/test123.jpg")

# manual("img/input/test123.jpg")
# is_similar("img/input/test3.jpg","img/input/test4.jpg")
