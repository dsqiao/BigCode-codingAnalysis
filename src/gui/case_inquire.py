import tkinter
from tkinter import ttk
from src.caseRecommendation.generate_options.generateOptions import *
import tkinter.font as tf


class CaseInquire:

    def return_to_main_page(self):
        from src.gui.root import Root
        self.clear()
        r = Root(self.root)
        r.root.mainloop()

    def inquire(self):
        difficulty_level = self.difficulty.get()
        case_type = self.kind.get()
        result = {}
        self.text.delete(1.0, tkinter.END)
        for case_id in case_level_data:
            if case_type == "全部" and difficulty_level == "全部":
                result.setdefault(case_id, {"题目地址": case_info_data.get(case_id)["题目地址"]})
            elif case_type == "全部":
                if case_level_data.get(case_id)["level"] == difficulty_level:
                    result.setdefault(case_id, {"题目地址": case_info_data.get(case_id)["题目地址"]})
            elif difficulty_level == "全部":
                if case_info_data.get(case_id)["题目类型"] == case_type:
                    result.setdefault(case_id, {"题目地址": case_info_data.get(case_id)["题目地址"]})
            else:
                if case_level_data.get(case_id)["level"] == difficulty_level and case_info_data.get(case_id)["题目类型"]==case_type:
                    result.setdefault(case_id, {"题目地址": case_info_data.get(case_id)["题目地址"]})
        for res in result:
            self.text.insert("insert", "题目ID:" + res + '\n')
            self.text.insert("insert", "题目地址:" + result.get(res)["题目地址"] + '\n\n')

    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        self.root.title("题目查询")
        ft = tf.Font(family="等距更纱黑体 T SC Semibold", size=11)
        self.difficulty = ttk.Combobox(root, font=ft, justify="center")
        self.difficulty.place(x=175, y=50, width=150, height=28)
        self.difficulty['value'] = ('全部', '简单', '中等', '较难', '困难', '地狱')
        self.difficulty.current(0)
        self.kind = ttk.Combobox(root, justify="center", font=ft)
        self.kind.place(x=425, y=50, width=150, height=28)
        self.kind['value'] = ('全部', '数组', '线性表', '排序算法', '查找算法', '数字操作', '字符串', '树结构', '图结构')
        self.kind.current(0)
        self.inquire_btu = ttk.Button(root, text="查询", command=self.inquire)
        self.inquire_btu.place(x=675, y=50, width=150, height=28)
        self.text = tkinter.Text(root, font=ft)
        self.text.place(x=70, y=110, width=860, height=500)

        self.ret_btn = tkinter.Button(self.root, text="返回", command=self.return_to_main_page)
        self.ret_btn.place(x=50, y=650, width=60, height=30)

    def clear(self):
        self.difficulty.destroy()
        self.kind.destroy()
        self.inquire_btu.destroy()
        self.text.destroy()
        self.ret_btn.destroy()

