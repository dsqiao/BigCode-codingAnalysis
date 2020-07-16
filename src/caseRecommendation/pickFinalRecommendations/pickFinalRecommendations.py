import json
from src.caseRecommendation.generate_options import generateOptions
import tkinter
from tkinter.filedialog import askopenfilename
import requests
import zipfile as z
import os
import sys

ability_score_path = "../../abilityAnalysis/ability_score.json"
case_level_path = "../../difficultyAnalysis/finalScore/final_score.json"
options_path = "./generated_optional_cases.json"

case_weight = {
    "数组": 301 / 1413,  # 301
    "线性表": 128 / 1413,  # 64+11+53=128
    "排序算法": 63 / 1413,  # 63
    "字符串": 204 / 1413,  # 204
    "数字操作": 199 / 1413,  # 199
    "查找算法": 310 / 1413,  # 141+93+76=310
    "树结构": 163 / 1413,  # 163
    "图结构": 45 / 1413  # 45
}


# 加载数据
def load(path):
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


ability_score_data = load(ability_score_path)
case_level_data = load(case_level_path)


# 计算收益
def calculate_profit(difficulty, ability, weight):
    # difficulty: 题目难度分数  ability: 学生能力分数  weight: 题目类型权重
    return (200 / difficulty + (difficulty - ability)) * weight


# 产生最终推荐题目
def pick_final_recommendations(user_id):
    final_recommendations = {}
    case_profits = {}
    generateOptions.generate_options(user_id)
    options_data = load(options_path)
    for case_id in options_data.keys():
        case_type = options_data.get(case_id).get("题目类型")
        weight = case_weight.get(case_type)
        difficulty = case_level_data.get(case_id)["index"]
        # print(ability_score_data.get(user_id).get(case_type)[-1][0])
        ability = generateOptions.convert_map(ability_score_data.get(user_id).get(case_type)[-1][0])
        profit = calculate_profit(difficulty, ability, weight)
        case_profits.setdefault(case_id, profit)
    profits_sorted = sorted(case_profits.items(), key=lambda x: x[1], reverse=True)  # 字典按profit值降序排列
    print(profits_sorted)
    for i in range(2):
        # 选取收益最高的两题作为最后的推荐题目
        selected_case_id = profits_sorted[i][0]
        final_recommendations.setdefault(selected_case_id, options_data.get(selected_case_id))
    print(final_recommendations)
    json_str = json.dumps(final_recommendations, ensure_ascii=False, indent=4)
    with open('final_recommendations.json', 'w', encoding='utf-8') as fp:
        fp.write(json_str)
    return final_recommendations


def open_file(file_path):
    global json_data
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        print(json_data)


def select_file():
    global path
    path = askopenfilename()
    if path != "":
        open_file(path)


def unzip(zip_src, dst_dir):
    fz = z.ZipFile(zip_src, 'r')
    for filename in ["readme.md"]:
        fz.extract(filename, dst_dir)


def cal():
    global stu_id_entry
    global text
    stu_id = stu_id_entry.get()
    try:
        final_recommendations = pick_final_recommendations(stu_id)
        text.delete(1.0, tkinter.END)
        i = 0
        for case_id in final_recommendations:
            url = final_recommendations[case_id]['题目地址']
            try:
                print(url)
                i += 1
                text.insert("insert", "\n\n题目" + str(i) + ": " + '\n')
                r = requests.get(url)
                with open("temp" + str(case_id), "wb") as f:
                    f.write(r.content)
                unzip("temp" + str(case_id), os.getcwd())
                case = open('readme.md').read()
                print(case)
                text.insert("insert", case)
            except TimeoutError:
                text.insert("insert", "下载题目异常")
    except TypeError:
        text.delete(1.0, tkinter.END)
        if stu_id == "":
            text.insert("insert", "输入不能为空")
        else:
            text.insert("insert", "非法输入: " + stu_id + '\n')


if __name__ == '__main__':

    path = ""
    json_data = {}
    root = tkinter.Tk()
    root.geometry('1000x600')
    root.title('title')

    label = tkinter.Label(root, text="输入学生编号：")
    label.place(x=210, y=60, wid=160, height=30)

    stu_id_entry = tkinter.Entry(root)
    stu_id_entry.place(x=360, y=60, width=220, height=30)

    cal_btu = tkinter.Button(root, text="推荐", command=cal)
    cal_btu.place(x=610, y=60, width=80, height=30)

    text = tkinter.Text(root)
    text.place(x=30, y=120, width=940, height=400)
    root.mainloop()

