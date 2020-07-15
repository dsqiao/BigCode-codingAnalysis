import json
from src.caseRecommendation.generate_options import generateOptions

ability_score_path = "../../abilityAnalysis/ability_score.json"
case_level_path = "../../difficultyAnalysis/finalScore/final_score.json"
options_path = "./generated_optional_cases.json"

case_weight = {
    "数组": 301/1413,  # 301
    "线性表": 128/1413,  # 64+11+53=128
    "排序": 63/1413,  # 63
    "字符串": 204/1413,  # 204
    "数字操作": 199/1413,  # 199
    "查找": 310/1413,  # 141+93+76=310
    "树": 163/1413,  # 163
    "图":  45/1413 # 45
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
        profit = calculate_profit(difficulty,ability,weight)
        case_profits.setdefault(case_id,profit)
    profits_sorted = sorted(case_profits.items(),key = lambda x:x[1],reverse = True) # 字典按profit值降序排列
    print(profits_sorted)
    for i in range(2):
        # 选取收益最高的两题作为最后的推荐题目
        selected_case_id = profits_sorted[i][0]
        final_recommendations.setdefault(selected_case_id,options_data.get(selected_case_id))
    print(final_recommendations)
    json_str = json.dumps(final_recommendations, ensure_ascii=False, indent=4)
    with open('final_recommendations.json', 'w', encoding='utf-8') as fp:
        fp.write(json_str)

if __name__ == '__main__':
    pick_final_recommendations("48117")