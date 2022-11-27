import json
import string

import matplotlib.pyplot as plt
import networkx as nx

from action import Action
from compo import Compo
from state import State
from image_recognition import img_rec, is_similar

class TreeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph(sub_graph=True)
        self.init()

    def init(self):#初始化树的根节点，即首页
        graph = self.graph
        GUI.output("请上传初始界面")  # GUI界面显示"请上传初始界面"
        while True:
            if GUI.inputChanged:  # GUI界面用户上传了新的图片
                # curr_img_file="/img/input/test10.jpg"
                curr_img_file = GUI.get_last_image_path()  # GUI界面返回当前最新的图片路径
                break
        img_rec(curr_img_file, "img/output", "test")  # 获得了初始界面解析后的json文件
        json_path = self.jpgToJson(curr_img_file)
        compo_list = self.parse_json(json_path)  # 返回compo_list
        screen_id = self.jpgToNum(curr_img_file)
        root_state = State(screen_id, curr_img_file, compo_list)  # 得到的根节点
        graph.add_node(root_state)
        self.dfs(root_state)

    #将json文件解析成compo_list
    def parse_json(self, json_path):
        res_list = []#存放compo
        bg_width = 0
        bg_height = 0
        with open('file.json') as f:
            data = json.load(f)
        compos_list = data['compos']
        for compo in compos_list:
            if compo['class'] == "Background":
                bg_width = compo['width']
                bg_height = compo['height']
            elif compo['class'] == "Compo":
                #相对坐标和长宽保留3位小数
                relative_row_min = round(compo['row_min'] / bg_height, 3)
                relative_column_min = round(compo['row_min'] / bg_width, 3)
                relative_width = round(compo['width'] / bg_width, 3)
                relative_height = round(compo['height' / bg_height], 3)
                c = Compo(relative_row_min, relative_column_min, relative_width, relative_height)
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
        if is_similar(curr_img_file, curr_state.screenshot_path):
            compo.is_used = True  # 表示compo已经遍历过
            return
        else:
            #child_state是发现页目前所有的子state
            for child_state in list(graph.neighbors(curr_state)):
                if is_similar(child_state.screenshot_path, curr_img_file):
                    #说明click compo跳转到的页面已经有另一个compo跳转过了，将它们合并
                    curr2child_action = graph.get_edge_data(curr_state, child_state)['action']
                    curr_state.upt_compo_list(compo, curr2child_action.compo)
                    return

            img_rec(curr_img_file, "img/output", "test")  # 获得了点击compo后的界面解析后的结果
            json_path = self.jpgToJson(curr_img_file)
            compo_list = self.parse_json(json_path)  # 返回compo_list
            screen_id = self.jpgToNum(curr_img_file)
            new_state = State(screen_id, curr_img_file, compo_list)  # 得到的朋友圈新结点

            # 建立发现1到朋友圈2
            graph.add_node(new_state)
            graph.add_edge(curr_state, new_state, action=curr_action)
            compo.is_used = True  # 表示compo已经遍历过

            # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
            nx.draw(graph)
            plt.savefig("img/output_tree/tree" + screen_id + ".jpg")

            #TODO: curr_state = new_state迁移和不变的判断 总之实现合理的嵌套

