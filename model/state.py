#从compo.py导入Compo类
from compo import Compo

class State:#所有id=0的为state，即background/node
    def __init__(self, screen_id, screenshot_path, compo_list):
        #屏幕id，state的主键 类型在json中为Background
        self.screen_id = screen_id
        #存储test10.jpg 前端好显示
        self.screenshot_path = screenshot_path
        #存储该background中的每一个compo
        self.compo_list = compo_list


    # TODO: 调用dcc里的比较相似度方法？
    def sim(self, other, layout_weight=.7, bbox_threshold=configuration.SCREENSHOT_CONV_THRESHOLD):
        if cv_sim(self.img,other.img,0.98):
            return 1
        layout_sim = layout_similarity(self.tree, other.tree)
        widget_sim, _ = widget_similarity(self, other,
                                          bbox_threshold=bbox_threshold)
        logger.debug(f'layout similarity: {layout_sim}.')
        logger.debug(f'widget similarity: {widget_sim}.')
        return layout_weight * layout_sim + (1 - layout_weight) * widget_sim

    #当compo1和compo2进行操作后跳转到相同的界面,将两个组件合并
    def upt_compo_list(self, compo1, compo2):
        y = min(compo1.y, compo2.y)
        x = min(compo1.x, compo2.x)
        width = max(compo1.x + compo1.width, compo2.x + compo2.width) - min(compo1.x, compo2.x)
        height = max(compo1.y + compo1.height, compo2.y + compo2.height) - min(compo1.y, compo2.y)
        #id随机选择一个即可
        compo3 = Compo(x, y, height, width)
        self.compo_list.remove(compo1)
        self.compo_list.remove(compo2)
        self.compo_list.append(compo3)

