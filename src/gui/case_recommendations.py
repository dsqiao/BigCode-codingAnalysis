import tkinter
import requests
from src.caseRecommendation.pickFinalRecommendations import pickFinalRecommendations
import zipfile as z
import os


class CaseRecommendations:

    def return_to_main_page(self):
        from src.gui.root import Root
        self.clear()
        r = Root(self.root)
        r.root.mainloop()

    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        self.root.title('title')

        self.ret_btn = tkinter.Button(self.root, text="返回", command=self.return_to_main_page)
        self.ret_btn.place(x=50, y=650, width=60, height=30)

        self.label = tkinter.Label(self.root, text="输入学生编号：")
        self.label.place(x=210, y=60, width=160, height=30)

        self.stu_id_entry = tkinter.Entry(self.root)
        self.stu_id_entry.place(x=360, y=60, width=220, height=30)

        self.cal_btu = tkinter.Button(self.root, text="推荐", command=self.cal)
        self.cal_btu.place(x=610, y=60, width=80, height=30)

        self.text = tkinter.Text(self.root)
        self.text.place(x=50, y=120, width=900, height=500)

    def cal(self):
        stu_id = self.stu_id_entry.get()
        final_recommendations = pickFinalRecommendations.pick_final_recommendations(stu_id)
        print(final_recommendations)
        try:
            self.text.delete(1.0, tkinter.END)
            i = 0
            for case_id in final_recommendations:
                url = final_recommendations[case_id]['题目地址']
                try:
                    i += 1
                    self.text.insert("insert", "\n\n题目" + str(i) + ": " + '\n')
                    r = requests.get(url)
                    with open("temp" , "wb") as f:
                        f.write(r.content)
                    self.unzip(self, "temp", os.getcwd())
                    case = open('readme.md',encoding='utf-8').read()
                    self.text.insert("insert", case)
                except TimeoutError:
                    self.text.insert("insert", "下载题目异常")
        except TypeError:
            self.text.delete(1.0, tkinter.END)
            if stu_id == "":
                self.text.insert("insert", "输入不能为空")
            else:
                self.text.insert("insert", "没有查到这位同学：: " + stu_id + '\n')

    @staticmethod
    def unzip(self, zip_src, dst_dir):
        fz = z.ZipFile(zip_src, 'r')
        for filename in ["readme.md"]:
            fz.extract(filename, dst_dir)

    def clear(self):
        self.ret_btn.destroy()
        self.label.destroy()
        self.stu_id_entry.destroy()
        self.cal_btu.destroy()
        self.text.destroy()
