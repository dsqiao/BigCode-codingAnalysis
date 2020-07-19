import tkinter
from src.abilityAnalysis.visualizeAbilityScore import draw
from PIL import Image,ImageTk


def show():
    global stu_id_entry
    global root
    stu_id = stu_id_entry.get()
    try:
        ability_figure_path = draw(stu_id)
        img_open = Image.open(ability_figure_path)
        img_open = img_open.resize((550, 550), Image.ANTIALIAS)  # 修改图片大小便于显示
        img = ImageTk.PhotoImage(img_open)
        figure = tkinter.Label(root,image=img)
        figure.place(x=30, y=120, width=940, height=550)
    except TimeoutError:
        figure=tkinter.Label(root, text="加载图片异常")
        figure.place(x=100, y=120)
    except AttributeError:
        if stu_id == "":
            figure = tkinter.Label(root, text="输入不能为空")
            figure.place(x=100, y=120)
        else:
            figure = tkinter.Label(root, text="非法输入：" + stu_id)
            figure.place(x=100, y=120)

    root.mainloop()


if __name__ == '__main__':

    root = tkinter.Tk()
    root.geometry('1000x700')
    root.title("学生能力曲线查询")

    label = tkinter.Label(root, text="输入学生编号：")
    label.place(x=210, y=60, wid=160, height=30)

    stu_id_entry = tkinter.Entry(root)
    stu_id_entry.place(x=360, y=60, width=220, height=30)

    show_btu = tkinter.Button(root, text="生成曲线", command=show)
    show_btu.place(x=610, y=60, width=80, height=30)

    root.mainloop()

