class Compo:
    def __init__(self, x, y, height, width):
        #存储左上角的坐标(默认左上角为0,0)
        self.x = x
        self.y = y
        #存储该组件的高和宽
        self.height = height
        self.width = width
        #表示该组件是否被操作过
        self.is_used = False

