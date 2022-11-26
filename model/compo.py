class Compo:#所有id=0的为state，即background/node
    def __init__(self, compo_id, x, y, height, width):#(组件id，组件相对坐标)
        #组件id，state的主键 类型在json中为Compo
        self.compo_id = compo_id
        #存储左下角的坐标(默认左下角为0,0)
        self.x = x
        self.y = y
        #存储该组件的高和宽
        self.height = height
        self.width = width
        #TODO: 是否使用过该组件
        self.is_used = False

