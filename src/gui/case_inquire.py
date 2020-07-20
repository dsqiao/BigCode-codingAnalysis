import tkinter
from tkinter import ttk
from src.caseRecommendation.generate_options.generateOptions import *
import tkinter.font as tf


def inquire():
    global difficulty
    global kind
    global text
    difficulty_level = difficulty.get()
    case_type = kind.get()
    result = {}
    text.delete(1.0,tkinter.END)
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
        text.insert("insert", "题目ID:" + res + '\n')
        text.insert("insert", "题目地址:" + result.get(res)["题目地址"] + '\n\n')


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry('700x600')
    root.title("题目查询")
    ft = tf.Font(family="等距更纱黑体 T SC Semibold", size=11)
    difficulty = ttk.Combobox(root, font=ft, justify="center")
    difficulty.place(x=100, y=50, width=120, height=28)
    difficulty['value'] = ('全部', '简单', '中等', '较难', '困难', '地狱')
    difficulty.current(0)
    kind = ttk.Combobox(root, justify="center", font=ft)
    kind.place(x=290, y=50, width=120, height=28)
    kind['value'] = ('全部', '数组', '线性表', '排序算法', '查找算法', '数字操作', '字符串', '树结构', '图结构')
    kind.current(0)
    inquire_btu = ttk.Button(root, text="查询", command=inquire)
    inquire_btu.place(x=480, y=50, width=120, height=28)
    text = tkinter.Text(root, font=ft)
    text.place(x=50, y=100, width=600, height=450)
    root.mainloop()
