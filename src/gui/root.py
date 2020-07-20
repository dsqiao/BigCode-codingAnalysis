import tkinter
from src.gui.case_recommendations import CaseRecommendations
from src.gui.ability_analysis_show import AbilityAnalysisShow
from src.gui.case_inquire import CaseInquire


class Root:

    def call_case_recommendation(self):
        self.clear()
        cr = CaseRecommendations(self.root)
        cr.root.mainloop()

    def call_ability_analysis(self):
        self.clear()
        aas = AbilityAnalysisShow(self.root)
        aas.root.mainloop()

    def call_case_inquire(self):
        self.clear()
        ci = CaseInquire(self.root)
        ci.root.mainloop()

    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')

        self.root.title('')
        self.label = tkinter.Label(self.root, text="数据科学基础大作业gui", font=("", 40))
        self.btn1 = tkinter.Button(self.root, text="学生题目推荐", command=self.call_case_recommendation)
        self.btn2 = tkinter.Button(self.root, text="学生能力曲线查询", command=self.call_ability_analysis)
        self.btn3 = tkinter.Button(self.root, text="题目查询", command=self.call_case_inquire)
        self.label.place(x=200, y=110, width=600, height=50)
        self.btn1.place(x=350, y=250, width=300, height=50)
        self.btn2.place(x=350, y=350, width=300, height=50)
        self.btn3.place(x=350, y=450, width=300, height=50)

    def clear(self):
        self.label.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()


# 启动程序
if __name__ == '__main__':
    r = tkinter.Tk()
    t = Root(r)
    t.root.mainloop()
