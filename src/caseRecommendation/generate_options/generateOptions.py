import json
import numpy as np
import random
import math
import os

current_path = os.getcwd()
root_path = ""
for i in range(0, len(current_path)):
    root_path += current_path[i]
    if current_path[i + 1:i + 4] == 'src':
        break
# print(root_path)


ability_score_path = root_path + "src/abilityAnalysis/ability_score.json"
case_level_path = root_path + "src/difficultyAnalysis/finalScore/final_score.json"
total_info_path = root_path + "test_data.json"
case_info_path = root_path + "src/difficultyAnalysis/avgScoreCount/case_info.json"


# 加载数据
def load(path):
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


ability_score_data = load(ability_score_path)
case_level_data = load(case_level_path)
total_info_data = load(total_info_path)
case_info_data = load(case_info_path)

total_case_type = ["字符串", "数组", "线性表", "排序算法", "查找算法", "数字操作", "树结构", "图结构"]


# 映射函数
def convert_map(x):
    return 80 * math.log(1 + pow(x, 2), 2) / (
            math.log(1 + pow(x, 2), 2) + math.log(pow(1 + x, 0.5), 2) + 80 * math.pow(1 + x, -1 / 2.5))


# 检查与能力是否匹配
def check_fitness(converted_score, case_level):
    return abs(converted_score - case_level) <= 5


# 产生备选题目
def generate_options(user_id):
    user_final_score = {}
    total_options = []
    generated_optional_cases = {}
    user_score = ability_score_data.get(user_id)
    for case in user_score:
        user_final_score.setdefault(case, user_score.get(case)[-1][0] if len(user_score.get(case)) > 0 else 0)
    for case in total_case_type:
        if case not in user_final_score.keys():
            user_final_score.setdefault(case, 0)
    finished_case_ids = []
    case_data = total_info_data.get(user_id)["cases"]
    for case in case_data:
        finished_case_ids.append(case["case_id"])
    for case_id in case_info_data:
        if case_id in finished_case_ids:
            continue
        else:
            case_type = case_info_data.get(case_id)["题目类型"]
            if check_fitness(convert_map(user_final_score.get(case_type)), case_level_data.get(case_id)["index"]):
                total_options.append(case_id)
    np.random.shuffle(total_options)
    basic_options = total_options[:8]
    for op in basic_options:
        generated_optional_cases.setdefault(op, {"题目类型": case_info_data.get(op)["题目类型"],
                                                 "题目地址": case_info_data.get(op)["题目地址"]})
    # print(generated_optional_cases)
    # for case_id in generated_optional_cases:
    #     print(case_id)
    #     for info in generated_optional_cases.get(case_id):
    #         print(info)
    print(generated_optional_cases)
    json_str = json.dumps(generated_optional_cases, ensure_ascii=False, indent=4)
    storage_path = root_path + "/src/caseRecommendation/generate_options/generated_optional_cases.json"
    with open(storage_path, 'w', encoding='utf-8') as fp:
        fp.write(json_str)


if __name__ == '__main__':
    generate_options("48117")
