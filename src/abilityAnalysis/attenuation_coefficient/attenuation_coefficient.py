import json
import math


def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(d: dict, file_path: str):
    json_str = json.dumps(d, ensure_ascii=False, indent=4)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)


# 计算衰减系数
# 定义x： 该类型，该难度下已实际完成的题目 / 该类型， 该难度下总的题目数量
case_info = load_json("../../difficultyAnalysis/avgScoreCount/case_info.json")
final_score = load_json("../../difficultyAnalysis/finalScore/final_score.json")
coding_sequence = load_json("../coding_sequence.json")


# total字典，统计 某类型，某难度下的总题目
total = {}  # {'case_type': {... ,'level': num }}
for case_id in case_info:
    case_type = case_info[case_id]['题目类型']
    level = final_score[case_id]['level']
    total.setdefault(case_type, {'简单': 0, "中等": 0, "较难": 0, "困难": 0, "地狱": 0})
    total[case_type][level] += 1


# current字典，统计某用户在某时刻已完成的某类型的某难度的题目总数
current = {}  # {'user_id': {'case_type': { ... 'level', num}}}
for user_id in coding_sequence:
    current.setdefault(user_id, {})
    for case_type in coding_sequence[user_id]:
        current[user_id].setdefault(case_type, {'简单': 0, "中等": 0, "较难": 0, "困难": 0, "地狱": 0})


# attenuation_coefficient 字典，统计用户完成的每道题的 衰减系数
attenuation_coefficient = {}  # {'user_id': {'case_type': }}
for user_id in coding_sequence:
    attenuation_coefficient.setdefault(user_id, {})
    for case_type in coding_sequence[user_id]:
        attenuation_coefficient[user_id].setdefault(case_type, {})
        for i in range(0, len(coding_sequence[user_id][case_type])):
            case_id = coding_sequence[user_id][case_type][i]
            level = final_score[case_id]['level']
            current[user_id][case_type][level] += 1
            x = current[user_id][case_type][level] / total[case_type][level]
            coefficient = 1 / (1 + math.log(pow(x+1, 1/3), 10))
            attenuation_coefficient[user_id][case_type][case_id] = coefficient
write_json(attenuation_coefficient, "attenuation_coefficient.json")
