from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk  # python3.x 执行pip install Pillow

root = Tk()
root.config(bg='#E1F3FF')
root.title('自动化测试')
img_ori = None  # 设置用于显示图片的全局变量


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
        global img_ori

        # 选择单个图片
        filename = askopenfilename(title='选择图片', filetypes=[('JPG', '*.jpg'), ('PNG', '*.png'), ('All Files', '*')])
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
        global img_ori
        root.update()
        img_ori = None
        self.file = None
        self.frm0.update()


use = GUI()
root.wm_attributes("-topmost", 1)  # 窗口置顶
root.geometry('1280x720+{0}+{1}'.format(400, 120))  # 设置窗口大小和初始位置

root.mainloop()
