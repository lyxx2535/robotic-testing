import json
import string
import os
import time

import matplotlib.pyplot as plt
import networkx as nx

from model.action import Action
from model.compo import Compo
from model.state import State
from image_recognition import img_rec, is_similar

# 辅助函数
from tkinterGUI import GUI, output


def get_input_dir_num():
    path = 'img/input'  # 输入文件夹地址
    files = os.listdir(path)  # 读入文件夹
    num_jpg = len(files)  # 统计文件夹中的文件个数
    return num_jpg


def get_newest_img_path():
    path = "img\\input"
    # 获取文件夹中所有的文件(名)，以列表形式返货
    lists = os.listdir(path)
    # 按照key的关键字进行生序排列，lambda入参x作为lists列表的元素，获取文件最后的修改日期，
    # 最后对lists以文件时间从小到大排序
    lists.sort(key=lambda x: os.path.getmtime((path + "/" + x)))
    # 获取最新文件的绝对路径，列表中最后一个值,文件夹+文件名
    file_new = os.path.join(path + "/", lists[-1])
    return file_new

# 将json文件解析成compo_list
def parse_json(json_path):
    res_list = []  # 存放compo
    bg_width = 0
    bg_height = 0
    time.sleep(5)
    with open("D:\\新桌面\\robotictesting\\" + json_path) as f:
        data = json.load(f)

    compos_list = data['compos']
    for compo in compos_list:
        if compo['class'] == "Background":
            bg_width = compo['width']
            bg_height = compo['height']
        elif compo['class'] == "Compo":
            # 相对坐标和长宽保留3位小数
            relative_row_min = round(compo['row_min'] / bg_height, 3)
            relative_column_min = round(compo['column_min'] / bg_width, 3)
            relative_width = round(compo['width'] / bg_width, 3)
            relative_height = round(compo['height'] / bg_height, 3)
            c = Compo(relative_column_min, relative_row_min, relative_height, relative_width)
            res_list.append(c)
    return res_list


# 从curr_img_file="/img/input/test10.jpg"获得"/img/output/test10.json"
def jpgToJson(s):
    r = s.split("/")
    news = r[len(r) - 1]
    news.replace(".jpg", ".json")
    return "/img/output/" + news.replace(".jpg", ".json")


# 从curr_img_file="/img/input/test10.jpg"获得10
def jpgToNum(s):
    r = s.split("/")
    n = r[len(r) - 1]  # test10.jpg
    n = n.replace(".jpg", "")
    n = n.replace("test", "")
    return int(n)#string转int


# 将curr_action转换成"click (组件中心坐标)"的形式
def curr_action_info(curr_action):
    res = curr_action.action_type
    compo = curr_action.compo
    central_x = round(compo.x + compo.width / 2, 3)
    central_y = round(compo.y + compo.height / 2, 3)
    res += " (" + str(central_x) + "," + str(central_y) + ")"
    return res

class TreeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph(sub_graph=True)
        self.init()

    def init(self):#初始化树的根节点，即首页
        graph = self.graph
        curr_dir_num = get_input_dir_num()
        output("upload initial page")  # GUI界面显示"请上传初始界面"
        while True:
            if get_input_dir_num() == curr_dir_num + 1:  # GUI界面用户上传了新的图片
                # curr_img_file="/img/input/test10.jpg"
                curr_img_file = get_newest_img_path() # GUI界面返回当前最新的图片路径
                print(curr_img_file)
                break
            time.sleep(5)
        img_rec(curr_img_file, "img/output", "test")  # 获得了初始界面解析后的json文件
        json_path = jpgToJson(curr_img_file)
        compo_list = parse_json(json_path)  # 返回compo_list
        screen_id = jpgToNum(curr_img_file)
        print(screen_id)
        root_state = State(screen_id, curr_img_file, compo_list)  # 得到的根节点
        graph.add_node(root_state, id=root_state.screen_id)
        #保存树图，这时候只有一个root节点
        self.save_curr_tree(screen_id)
        self.dfs(root_state)

    # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
    def save_curr_tree(self, screen_id):
        graph = self.graph
        node_labels = nx.get_node_attributes(graph, 'id')#格式是一个dict
        edge_labels = nx.get_edge_attributes(graph, 'action')

        new_edge_labels = {}
        for item in edge_labels.items():  # item为{(,,0):'action'}
            tup = item[0]
            tup = tup[:len(tup) - 1]
            act = item[1]
            new_edge_labels[tup] = act

        # 生成节点位置信息
        pos = nx.spring_layout(graph)
        plt.rcParams['figure.figsize'] = (6, 4)  # 设置画布大小
        nx.draw_networkx_nodes(graph, pos)  # 画节点
        nx.draw_networkx_edges(graph, pos)  # 画边

        nx.draw_networkx_labels(graph, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=new_edge_labels)
        print(node_labels)
        print(new_edge_labels)

        plt.axis('off')  # 去掉坐标刻度

        nx.draw(graph)
        plt.savefig("img/output_tree/tree" + str(screen_id) + ".jpg")
        plt.close()

    def dfs(self, curr_state):
        # curr_state是当前所在屏幕截图的state
        for compo in curr_state.compo_list:
            if not compo.is_used:
                # 告诉前端需要操作compo
                self.dfs_wrapper(compo, curr_state)

    def dfs_wrapper(self, compo, curr_state):
        graph = self.graph
        # 告诉前端需要操作compo
        curr_action = Action(compo)
        curr_dir_num = get_input_dir_num()
        print(curr_action_info(curr_action))
        output(curr_action_info(curr_action))  # GUI界面显示“click (x, y)"
        while True:
            if get_input_dir_num() == curr_dir_num + 1:  # GUI界面用户上传了新的图片
                # curr_img_file="/img/input/test10.jpg"
                curr_img_file = get_newest_img_path()  # GUI界面返回当前最新的图片路径
                break
            time.sleep(5)
        #case 1: 如果点击compo后页面没有跳转，返回
        if is_similar(curr_img_file, curr_state.screenshot_path):
            compo.is_used = True  # 表示compo已经遍历过
            print("case 1: page not changed after click")
            return
        else:
            # case 2: 如果点击compo后跳转的页面已经在子state中（有另一个compo跳转过了），将它们合并
            #child_state是发现页目前所有的子state(u->v v的集合  v->u不算)
            for child_state in list(graph.neighbors(curr_state)):
                if is_similar(child_state.screenshot_path, curr_img_file):
                    curr2child_action = graph.get_edge_data(curr_state, child_state)['action']#TODO: 这里有错
                    curr_state.upt_compo_list(compo, curr2child_action.compo)
                    print("case 2: merge compo with same jump")
                    return

            img_rec(curr_img_file, "img/output", "test")  # 获得了点击compo后的界面解析后的结果
            json_path = jpgToJson(curr_img_file)
            compo_list = parse_json(json_path)  # 返回compo_list
            screen_id = jpgToNum(curr_img_file)
            new_state = State(screen_id, curr_img_file, compo_list)  # 得到的朋友圈新结点

            # case 3: 如果点击compo后跳转的页面在树中，则不用添加点，添加有向边即可
            # case 4: 如果点击compo后跳转的页面在树中，则添加点和有向边
            if new_state not in graph:
                graph.add_node(new_state, id=new_state.screen_id)
                print("case 3: new page showed after click, add edge and node")
            else:
                print("case 4: page already in tree but not children, only add edge")
            graph.add_edge(curr_state, new_state, action=curr_action_info(curr_action))

            compo.is_used = True  # 表示compo已经遍历过

            # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
            self.save_curr_tree(screen_id)

            #case3是环，所以不用深入下去，处理完其他compo再回到上级节点
            if new_state not in graph:
                # 其实就是dfs(new_state) 但避免出现循环调用的情况还是自己调自己吧
                curr_state = new_state
                for compo in curr_state.compo_list:
                    if not compo.is_used:
                        # 告诉前端需要操作compo
                        self.dfs_wrapper(compo, curr_state)

            return

