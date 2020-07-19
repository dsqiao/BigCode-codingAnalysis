import matplotlib.pyplot as plt
import json
import os

current_path = os.getcwd()
root_path = ""
for i in range(0, len(current_path)):
    root_path += current_path[i]
    if current_path[i+1:i+4] == 'src':
        break

ability_score_path = root_path + "src/abilityAnalysis/ability_score.json"

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


def draw(userId):
    # 跟据用户ID绘制学习能力曲线图
    plt.figure(figsize=(8, 8))
    # plt.style.use("seaborn-dark")
    with open(ability_score_path, "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        abilities = json_data.get(userId)
        for key in abilities.keys():
            # print(key)
            # print(abilities.get(key))
            x = []  # 横坐标：做题数量
            y = []  # 纵坐标：该项能力得分
            for items in abilities.get(key):
                x.append(items[1])
                y.append(items[0])

            plt.plot(x, y, label=key, ms=5, marker='o')

        plt.xlabel("做题数量")
        plt.ylabel("该类型能力得分")
        plt.title("用户" + userId + "的学习能力曲线")
        plt.legend(loc="best")
        plt.savefig("ability_figure.jpg")
        plt.show()
        figure_path = os.path.abspath("ability_figure.jpg")
        print(figure_path)
        return figure_path

if __name__ == '__main__':
    draw("48117")
    # draw("49405")
    # draw("60836")
