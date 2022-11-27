import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk  # python3.x 执行pip install Pillow
import os
import time

root = Tk()
root.config(bg='#E1F3FF')
root.title('自动化测试')
img_ori = None  # 设置用于显示图片的全局变量
file_count = 0
filename = None

def get_output_tree_dir_num():
    path = 'img/output_tree'  # 输入文件夹地址
    files = os.listdir(path)  # 读入文件夹
    num_jpg = len(files)  # 统计文件夹中的文件个数
    return num_jpg


current_tree_num = get_output_tree_dir_num()


class GUI:
    def __init__(self):
        # GUI label
        self.lb_text1 = Label(root, text="GUI预览", font=('楷体', 14), bg='#E1F3FF')
        self.lb_text1.place(x=90, y=20)

        # 设置显示子框架位置（图片框）
        self.frm0 = Frame(root, width=300, height=640, bg="White")
        self.frm0.place(x=90, y=60)

        # 设置上传文件的按钮，绑定事件 self.chose_file
        self.button_chose1 = Button(root, text='上传图片', font=('楷体', 14), bg='White', activebackground='#E6E6E6',
                                    command=lambda: self.chose_file())
        self.button_chose1.place(x=190, y=20)

        self.button_chose2 = Button(root, text="清空数据", font=('楷体', 14), bg='White', activebackground='#E6E6E6',
                                    command=lambda: self.clear())
        self.button_chose2.place(x=295, y=20)
        self.file = None  # 用来记录每次上传的图片

    def chose_file(self, event=None):
        # 使用全局变量用来显示图片 img_ori
        global img_ori, file_count, filename

        # 选择单个图片
        filename = askopenfilename(title='选择图片', filetypes=[('JPG', '*.jpg'), ('PNG', '*.png'), ('All Files', '*')])

        # 保存到input文件夹
        file = open(filename, "rb")
        data = file.read()
        file.close()

        new_input = open("img/input/input" + str(file_count) + ".jpg", "wb")
        new_input.write(data)
        new_input.close()

        ims = Image.open(filename)

        self.file = ims.copy()  # 记录本次上传原始图片

        # 图片尺寸规格化
        w, h = ims.size
        if w > h:
            ime = ims.resize((360, int((360 * h / w))))
        else:
            ime = ims.resize((int(640 * w / h), 640))

        img_ori = ImageTk.PhotoImage(ime)
        lb1 = Label(self.frm0, image=img_ori, bg="white")  # 用来显示图片
        lb1.place(x=0, y=0)  # 设置图片的放置位置

    def clear(self, event=None):
        global img_ori, file_count, filename
        root.update()
        img_ori = None
        self.file = None
        filename = None
        self.frm0.update()
        file_count += 1

    def output(self, text):
        self.lb_text1 = Label(root, text=text, font=('楷体', 14), bg='#E1F3FF')
        self.lb_text1.place(x=480, y=20)

    def get_last_image_path(self):
        return filename

    def update_tree_graph(self):
        global current_tree_num
        print(current_tree_num)
        print(get_output_tree_dir_num())
        if get_output_tree_dir_num() == current_tree_num + 1:
            current_tree_num = get_output_tree_dir_num()
            print(current_tree_num)
            tree = Image.open('img/output_tree/tree' + str(current_tree_num) + '.jpg')
            print(tree)

            # 图片尺寸规格化
            w, h = tree.size
            if w > h:
                ime2 = tree.resize((400, int((400 * h / w))))
            else:
                ime2 = tree.resize((int(400 * w / h), 400))

            self.current_tree = tree.copy()
            self.frm1 = Frame(root, width=400, height=400, bg="White")
            self.frm1.place(x=480, y=60)

            img_ori2 = ImageTk.PhotoImage(ime2)
            lb2 = Label(self.frm1, image=img_ori2, bg="white")  # 用来显示图片
            lb2.place(x=0, y=0)  # 设置图片的放置位置

        root.after(1000, self.update_tree_graph)



# def refresh_tree():
#     global current_tree_num
#     if use.get_output_tree_dir_num() == current_tree_num + 1:
#         use.update_tree_graph()
#         current_tree_num = use.get_output_tree_dir_num()
#     root.after(1000, refresh_tree())

use = GUI()

root.wm_attributes("-topmost", 1)  # 窗口置顶
root.geometry('1280x720+{0}+{1}'.format(400, 120))  # 设置窗口大小和初始位置

# root.after(1000, refresh_tree())
root.after(1000, use.update_tree_graph)
root.mainloop()
