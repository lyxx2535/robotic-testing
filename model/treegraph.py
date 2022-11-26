import networkx as nx
import json


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
    def __init__(self, json_path):
        #TODO: 看要不要用库

    def parse_json(self):
        # 屏幕id，state的主键 类型在json中为Background
        screen_id = 0
        # 存储test10.jpg 前端好显示
        self.screenshot_path = screenshot_path
        # 存储该background中的每一个compo
        self.compo_list = compo_list
        with open('file.json') as f:
            data = json.load(f)
        compos_list = data['compos']
        for compo in compos_list:
            if compo['class'] == "Background":
                scre