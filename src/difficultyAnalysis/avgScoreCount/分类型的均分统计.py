import json

with open("../case_info.json", 'r', encoding='utf-8') as fp:
    json_data = json.load(fp)

# 按照 {'题目类型':{'题目数量':'', '题目均分':''}}存储结果
case_type = {}
for item in json_data:
    key = json_data[item]['题目类型']
    case_type.setdefault(key, {'题目数量': 0, '题目均分': 0})
    case_type[key]['题目数量'] += 1
    case_type[key]['题目均分'] += json_data[item]['平均得分']

for key in case_type:
    case_type[key]['题目均分'] /= case_type[key]['题目数量']


print(case_type)
json_str = json.dumps(case_type, ensure_ascii=False, indent=4)
with open('../avg_score.json', 'w', encoding='utf-8') as fp:
    fp.write(json_str)
