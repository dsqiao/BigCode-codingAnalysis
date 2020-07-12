import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

final_score_path = "./final_score.json"
with open(final_score_path,'r',encoding="utf-8") as fp:
    res = fp.read()
    count_easy = res.count("简单")
    print(count_easy)
    count_middle = res.count("中等")
    print(count_middle)
    count_lhard = res.count("较难")
    print(count_lhard)
    count_hard = res.count("困难")
    print(count_hard)
    count_hell = res.count("地狱")
    print(count_hell)

font = FontProperties(fname=r"C:\Windows\Fonts\simyou.ttf",size=15)

x = ['简单','中等','较难','困难','地狱']
y = [count_easy,count_middle,count_lhard,count_hard,count_hell]

plt.rcParams['font.sans-serif']=['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus']=False

plt.figure(figsize=(15,15))

plt.title(u"各等级题目数量",fontproperties = font,fontsize = 25)
plt.xlabel(u"等级",fontproperties = font,fontsize = 20)
plt.ylabel(u"数量",fontproperties = font,fontsize = 20)
plt.tick_params(labelsize = 18)

plt.bar(x,y,color='#7AACFF',width=0.5)

for a,b in zip(x,y):
    plt.text(a,b,'%s' % b, ha='center',va='bottom',fontsize=18)

plt.show()

