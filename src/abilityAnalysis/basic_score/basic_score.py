import json


def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(d: dict, file_path: str):
    json_str = json.dumps(d, ensure_ascii=False, indent=4)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)


test_data = load_json("../../../test_data.json")
case_info = load_json("../../difficultyAnalysis/avgScoreCount/case_info.json")
final_score = load_json("../../difficultyAnalysis/finalScore/final_score.json")

score_map = {"简单": 1, "中等": 2, "较难": 3, "困难": 4, "地狱": 5}
basic_score = {}
for user_id in test_data:
    basic_score.setdefault(user_id, {})
    for case in test_data[user_id]['cases']:
        case_type = case_info[case['case_id']]['题目类型']
        basic_score[user_id].setdefault(case_type, {})
        case_level = final_score[case['case_id']]['level']
        basic_score[user_id][case_type].setdefault(case['case_id'], score_map[case_level] * case['final_score'] / 100)

write_json(basic_score, 'basic_score.json')

