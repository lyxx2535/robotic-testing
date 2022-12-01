import json
import os

import matplotlib.pyplot as plt
import networkx as nx

from model.action import Action
from model.compo import Compo
from model.state import State
from image_recognition import img_rec, is_similar

# 辅助函数
# 获得img/input文件夹下的文件个数
def get_input_dir_num():
    path = 'img/input'  # 输入文件夹地址
    files = os.listdir(path)  # 读入文件夹
    num_jpg = len(files)  # 统计文件夹中的文件个数
    return num_jpg

# 获得img/input文件夹下的最新文件路径
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
def jpg_to_json(s):
    r = s.split("/")
    news = r[len(r) - 1]
    news.replace(".jpg", ".json")
    return "/img/output/" + news.replace(".jpg", ".json")


# 从curr_img_file="/img/input/test10.jpg"获得10
def jpg_to_num(s):
    r = s.split("/")
    n = r[len(r) - 1]  # test10.jpg
    n = n.replace(".jpg", "")
    n = n.replace("test", "")
    return int(n)#string转int


# 将curr_action转换成"click (组件中心坐标)"的形式
def curr_action_info(curr_state, curr_action):
    res = "Screen " + str(curr_state.screen_id) + ": "
    res += curr_action.action_type
    compo = curr_action.compo
    central_x = round(compo.x + compo.width / 2, 3)
    central_y = round(compo.y + compo.height / 2, 3)
    res += " (" + str(central_x) + "," + str(central_y) + ")"
    return res

# 将curr_action转换成"click (组件中心坐标)"的形式
def curr_action_edge_info(curr_action):
    compo = curr_action.compo
    central_x = round(compo.x + compo.width / 2, 3)
    central_y = round(compo.y + compo.height / 2, 3)
    res = " (" + str(central_x) + "," + str(central_y) + ")"
    return res

# 获得前端上传的最新截图
def get_upload():
    curr_dir_num = get_input_dir_num()
    while True:
        if get_input_dir_num() == curr_dir_num + 1:  # GUI界面用户上传了新的图片
            # curr_img_file="/img/input/test10.jpg"
            curr_img_file = get_newest_img_path()  # GUI界面返回当前最新的图片路径
            break
    return curr_img_file

# 向前端输出字符串
def output(str):
    f = open("img/output_click/click.txt", 'w', encoding='UTF-8')
    f.write(str)
    f.close()

# 将当前img解析成新的state
def img_to_new_state(curr_img_file):
    img_rec(curr_img_file, "img/output", "test")  # 获得了点击compo后的界面解析后的结果
    json_path = jpg_to_json(curr_img_file)
    compo_list = parse_json(json_path)  # 返回compo_list
    screen_id = jpg_to_num(curr_img_file)
    new_state = State(screen_id, curr_img_file, compo_list)  # 得到的朋友圈新结点
    return new_state

class TreeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph(sub_graph=True)
        self.init()

    def init(self):#初始化树的根节点，即首页
        graph = self.graph
        curr_img_file = get_upload()
        root_state = img_to_new_state(curr_img_file) # 得到的根节点
        graph.add_node(root_state, id=root_state.screen_id)
        #保存树图，这时候只有一个root节点
        self.save_curr_tree(jpg_to_num(curr_img_file))
        self.dfs(root_state, root_state)

    # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
    def save_curr_tree(self, screen_id):
        graph = self.graph
        node_labels = nx.get_node_attributes(graph, 'id')#格式是一个dict
        print()
        edge_labels = dict([((u, v,), curr_action_edge_info(d['action']))
                            for u, v, d in graph.edges(data=True)])
        # 生成节点位置信息
        pos = nx.spring_layout(graph)
        plt.rcParams['figure.figsize'] = (12, 8)  # 设置画布大小
        nx.draw_networkx_nodes(graph, pos)  # 画节点
        nx.draw_networkx_edges(graph, pos)  # 画边

        nx.draw_networkx_labels(graph, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        # print(node_labels)
        # print(edge_labels)

        plt.axis('off')  # 去掉坐标刻度

        # nx.draw(graph)
        plt.savefig("img/output_tree/tree" + str(screen_id) + ".jpg")
        plt.close()

    #将用户从s引导到t，暂未处理偏离的情况，若有偏离直接要求返回上一步！(因为此时树图建立不全，且机械臂已有的操作不会出错)
    def find_path(self, source_node, target_node):
        graph = self.graph
        path = dict(nx.all_pairs_shortest_path(graph))
        list = path[source_node][target_node]
        guide_str = "guide from Screen " + str(source_node.screen_id) + " to " + str(target_node.screen_id)
        while len(list) >= 2:
            s = list[0]
            t = list[1]
            act = graph.get_edge_data(s, t)[0]['action']
            print(guide_str)
            print(curr_action_info(s, act))
            output(guide_str + " : " + curr_action_info(s, act))
            curr_img_file = get_upload()
            if is_similar(curr_img_file, t.screenshot_path):
                list.remove(s)
            else:
                output("you have deviated, please restart exploring.")
                break
        print("successfully go to target_node")
        return

    def dfs(self, curr_state, prev_state):
        # curr_state是当前所在屏幕截图的state
        for compo in curr_state.compo_list:
            if not compo.is_used:
                # 告诉前端需要操作compo
                self.dfs_wrapper(compo, curr_state)
        if curr_state != prev_state: #排除root结点不用返回父节点的情况
            print("finish exploring Screen " + str(curr_state.screen_id) + " back to Screen " + str(prev_state.screen_id))
            self.find_path(curr_state, prev_state)
        return

    def dfs_wrapper(self, compo, curr_state):
        graph = self.graph
        # 告诉前端需要操作compo
        curr_action = Action(compo)
        print(curr_action_info(curr_state, curr_action))
        output(curr_action_info(curr_state, curr_action))
        curr_img_file = get_upload()

        # 表示compo已经遍历过
        compo.is_used = True

        #case 1: 如果点击compo后页面没有跳转，返回(这里不用合并，因为压根没保存自循环的情况)
        if is_similar(curr_img_file, curr_state.screenshot_path):
            print("case 1: page not changed after click")
            return

        # case 2: 如果点击compo后跳转的页面已经在子state中（有另一个compo跳转过了），将它们合并
        for child_state in list(graph.neighbors(curr_state)):# 遍历所有的子state(u->v v的集合 v->u不算)
            if is_similar(child_state.screenshot_path, curr_img_file):
                # get_edge_data返回{0: {'action': 'click (x, y)'}}的形式
                curr2child_action = graph.get_edge_data(curr_state, child_state)[0]['action']
                merged_action = curr_state.upt_compo_list(compo, curr2child_action.compo)
                # 将树图边的action属性更新
                graph.remove_edge(curr_state, child_state)
                graph.add_edge(curr_state, child_state, action=merged_action)
                print("case 2: merge compo with same jump")
                self.save_curr_tree(jpg_to_num(curr_img_file))
                #因为此时子state应该已经遍历完，需要导引到curr_state
                self.find_path(child_state, curr_state)
                return

        # case 3: 如果点击compo后跳转的页面在树中，则不用添加点，添加有向边即可，然后回到上一个页面
        for other_state in list(graph.nodes):
            if other_state not in list(graph.neighbors(curr_state)) and other_state != curr_state:
                if is_similar(other_state.screenshot_path, curr_img_file):
                    graph.add_edge(curr_state, other_state, action=curr_action)
                    print("case 3: page already in tree but not children, only add edge")
                    # 从other_state回到curr_state，因为case3是环，不用深入下去，处理完其他compo再回到上级节点
                    print("from Screen " + str(other_state.screen_id) + " to Screen " + str(curr_state.screen_id))
                    self.find_path(other_state, curr_state)
                    # 将树图边的action属性更新
                    self.save_curr_tree(jpg_to_num(curr_img_file))
                    return

        # case 4: 如果点击compo后跳转的页面不在树中，则添加点和有向边
        new_state = img_to_new_state(curr_img_file)  # 得到的朋友圈新结点
        graph.add_node(new_state, id=new_state.screen_id)
        graph.add_edge(curr_state, new_state, action=curr_action)
        # 将最新的树图保存到output_tree文件夹下，供GUI显示 "img/output_tree/tree2.jpg"
        self.save_curr_tree(jpg_to_num(curr_img_file))
        print("case 4: new page showed after click, add edge and node")
        print("change state")
        self.dfs(new_state, curr_state)
        return

