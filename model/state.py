from model.compo import Compo
from model.action import Action

class State:
    def __init__(self, screen_id, screenshot_path, compo_list):
        #屏幕id
        self.screen_id = screen_id
        #存储屏幕截图路径
        self.screenshot_path = screenshot_path
        #存储该屏幕中的每一个compo
        self.compo_list = compo_list


    #当compo1和compo2进行操作后跳转到相同的界面,将两个组件合并
    def upt_compo_list(self, compo1, compo2):
        compo_list = self.compo_list
        # print(compo1)
        # print(compo2)
        y = min(compo1.y, compo2.y)
        x = min(compo1.x, compo2.x)
        width = max(compo1.x + compo1.width, compo2.x + compo2.width) - min(compo1.x, compo2.x)
        height = max(compo1.y + compo1.height, compo2.y + compo2.height) - min(compo1.y, compo2.y)

        compo3 = Compo(x, y, height, width)
        if compo1 in compo_list:
            compo_list.remove(compo1)
        if compo2 in compo_list:
            compo_list.remove(compo2)
        action = Action(compo3)
        return action

