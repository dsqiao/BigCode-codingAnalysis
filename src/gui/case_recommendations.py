import tkinter
import requests
from src.caseRecommendation.pickFinalRecommendations import pickFinalRecommendations
import zipfile as z
import os


def cal():
    global stu_id_entry
    global text
    stu_id = stu_id_entry.get()
    try:
        final_recommendations = pickFinalRecommendations.pick_final_recommendations(stu_id)
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


def unzip(zip_src, dst_dir):
    fz = z.ZipFile(zip_src, 'r')
    for filename in ["readme.md"]:
        fz.extract(filename, dst_dir)


if __name__ == '__main__':

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
