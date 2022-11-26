import string

import networkx as nx
import json
from action import Action
from compo import Compo
from state import State
import UIED.image_recognition.img_rec as img_rec
import matplotlib.pyplot as plt


# TODO:
class Node:
    def __init__(self, curr_state, parent_state_list, chidren_state_list):
        self.curr_state = curr_state
        self.parent_state_list = parent_state_list
        self.children_state_list = chidren_state_list

class Edge:
    def __init__(self, start_node, action, end_node):
        self.start_node = start_node
        self.action = action
        self.end_node= end_node

class TreeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph(sub_graph=True)

    #将json文件解析成compo_list
    def parse_json(self, json_path):
        res_list = []#存放compo
        with open('file.json') as f:
            data = json.load(f)
        compos_list = data['compos']
        for compo in compos_list:
            if compo['class'] == "Compo":
                c = Compo(compo['row_min'], compo['column_min'], compo['height'], compo['width'])
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
        news = r[len(r) - 1]#test10.jpg
        news = news.replace(".jpg", "")
        news = news.replace("test", "")
        return string.atoi(news)

    def dfs(self, curr_state):
        graph = self.graph
        # curr_state是当前所在屏幕截图的state
        for compo in curr_state.compo_list:
            if not compo.is_used:
                # 告诉前端需要操作compo
                self.dfs_loop(compo, curr_state)

    def dfs_loop(self, compo, curr_state):
        graph = self.graph
        # 告诉前端需要操作compo
        curr_action = Action(compo)
        GUI.output(curr_action)  # GUI界面显示“click (x, y)"
        while True:
            if GUI.inputChanged:  # GUI界面用户上传了新的图片
                # curr_img_file="/img/input/test10.jpg"
                curr_img_file = GUI.get_last_image_path()  # GUI界面返回当前最新的图片路径
                break
        # TODO: 邓楚宸的判断点击后页面和之前的页面不一样,不一样返回false
        if UIED.img_compare(curr_img_file, curr_state.screenshot_path):
            compo.is_used = True  # 表示compo已经遍历过
            return
        #TODO: 与所有现有子节点的图像比较，若一样则合并(如何得到所有子节点)
        elif True:
            curr_state.upt_compo_list()
        else:
            img_rec(curr_img_file, "img/output", "test")  # 获得了点击compo后的界面解析后的结果
            json_path = self.jpgToJson(curr_img_file)
            compo_list = self.parse_json(json_path)  # 返回compo_list
            screen_id = self.jpgToNum(curr_img_file)
            new_state = State(screen_id, curr_img_file, compo_list)  # 得到的朋友圈新结点

            # 建立发现1到朋友圈2
            graph.add_edge(curr_state, new_state, action=curr_action, no_change=a['nochange'])
            compo.is_used = True  # 表示compo已经遍历过

            # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
            nx.draw(graph)
            plt.savefig("img/output_tree/tree" + screen_id + ".jpg")

            #TODO: curr_state = new_state迁移和不变的判断 总之实现合理的嵌套

