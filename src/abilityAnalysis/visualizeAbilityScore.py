import matplotlib.pyplot as plt
import json

ability_score_path = "./ability_score.json"

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
        plt.show()


if __name__ == '__main__':
    draw("48117")
    draw("49405")
    draw("60836")
