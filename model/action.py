#从compo.py导入Compo类
from model.compo import Compo

class Action:#所有
    def __init__(self, compo):
        #action_type理论上要与机械臂的操作类型定义，但现在机械臂寄了，就用字段输出吧(暂时只考虑了click的情况)
        self.action_type = "click"
        #存储操作的组件
        self.compo = compo

