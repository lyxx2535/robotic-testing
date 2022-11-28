from tkinter import Tk


from tkinterGUI import GUI


root = Tk()
root.config(bg='#E1F3FF')
root.title('自动化测试')
use = GUI(root)



root.wm_attributes("-topmost", 1)  # 窗口置顶
root.geometry('1540x720+{0}+{1}'.format(100, 120))  # 设置窗口大小和初始位置

# root.after(1000, refresh_tree())
root.after(1000, use.update_tree_graph)
root.mainloop()
