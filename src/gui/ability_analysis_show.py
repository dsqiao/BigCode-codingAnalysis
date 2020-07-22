import tkinter
from src.abilityAnalysis.visualizeAbilityScore import draw
from PIL import Image, ImageTk


class AbilityAnalysisShow:

    def return_to_main_page(self):
        from src.gui.root import Root
        self.clear()
        r = Root(self.root)
        r.root.mainloop()

    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        self.root.title('学生能力曲线查询')
        self.label = tkinter.Label(self.root, text="输入学生编号：")
        self.label.place(x=210, y=60, wid=160, height=30)

        self.stu_id_entry = tkinter.Entry(self.root)
        self.stu_id_entry.place(x=360, y=60, width=220, height=30)

        self.show_btu = tkinter.Button(self.root, text="生成曲线", command=self.show)
        self.show_btu.place(x=610, y=60, width=80, height=30)

        self.ret_btn = tkinter.Button(self.root, text="返回", command=self.return_to_main_page)
        self.ret_btn.place(x=50, y=650, width=60, height=30)

        self.figure = tkinter.Label()
        self.text = tkinter.Text()

    def show(self):
        self.figure.destroy()
        stu_id = self.stu_id_entry.get()
        self.text.delete(1.0, tkinter.END)
        try:
            ability_figure_path = draw(stu_id)
            img_open = Image.open(ability_figure_path)
            img_open = img_open.resize((500, 500), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img_open)
            self.figure = tkinter.Label(self.root, image=img)
            self.figure.place(x=30, y=120, width=940, height=500)
        except TimeoutError:
            self.figure.destroy()
            self.text.insert("insert", "加载图片异常")
            self.text.place(x=100, y=120)
        except AttributeError:
            self.figure.destroy()
            if stu_id == "":
                self.text.insert("insert", "输入不能为空")
                self.text.place(x=100, y=120)
            else:
                self.text.insert("insert", "没有查到这位同学：" + stu_id)
                self.text.place(x=100, y=120)
        self.root.mainloop()

    def clear(self):
        self.label.destroy()
        self.stu_id_entry.destroy()
        self.show_btu.destroy()
        self.ret_btn.destroy()
        self.figure.destroy()
        self.text.destroy()

