# 计算表现系数
import json
import math

def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(d: dict, file_path: str):
    json_str = json.dumps(d, ensure_ascii=False, indent=4)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)


case_info = load_json("../../difficultyAnalysis/avgScoreCount/case_info.json")
final_score = load_json("../../difficultyAnalysis/finalScore/final_score.json")
test_data = load_json("../../../test_data.json")
level_index_map = {"简单": 0, "中等": 1, "较难": 2, "困难": 3, "地狱": 4}

# 分均得分 {'user_id': 'case_type': {'case_id': ''}}
score_per_second_cur = {}
score_per_second_avg = {}
mu = {}  # 记录每人完成每题时的表现系数
# 初始化表现系数
for user_id in test_data:
    mu.setdefault(user_id, {})
    for case in test_data[user_id]['cases']:
        case_type = case_info[case['case_id']]['题目类型']
        mu[user_id].setdefault(case_type, {})


for user_id in test_data:
    score_per_second_cur.setdefault(user_id, {})
    score_per_second_avg.setdefault(user_id, {})
    for case in test_data[user_id]["cases"]:
        case_type = case_info[case['case_id']]['题目类型']
        score_per_second_cur[user_id].setdefault(case_type, {})
        # 五个数组分别对应 简单，中等，较难，困难，地狱 难度的 (sps 总值，题目数量)
        score_per_second_avg[user_id].setdefault(case_type, [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
        case_level = final_score[case['case_id']]['level']
        upload_records = case['upload_records']
        if len(upload_records) == 0:
            print("数据错误")
            continue
        else:
            if len(upload_records) == 1:
                uploadTimeIntervals = 1000
            else:
                if case['final_score'] < 100:
                    uploadTimeIntervals = upload_records[-1]['upload_time'] - upload_records[0]['upload_time']
                else:
                    uploadTimeIntervals = 0
                    for i in range(0, len(upload_records)):
                        if upload_records[i]['score'] == 100:
                            uploadTimeIntervals = upload_records[i]['upload_time'] - upload_records[0]['upload_time']
                            break
                    if uploadTimeIntervals == 0:
                        uploadTimeIntervals = 1000
            index = final_score[case['case_id']]['index']
            if index == 0:  # 对于index为0的情况，为防止log(0, 10)出现数值错误，将其替换为远小于第二小index的0.001
                index = 0.001

            sps = index / uploadTimeIntervals  # 这道题目的score per second
            score_per_second_cur[user_id][case_type][case['case_id']] = sps
            # 该题的sps影响了平均sps
            score_per_second_avg[user_id][case_type][level_index_map[case_level]][0] += sps
            score_per_second_avg[user_id][case_type][level_index_map[case_level]][1] += 1
            avg_sps = score_per_second_avg[user_id][case_type][level_index_map[case_level]][0] / \
                      score_per_second_avg[user_id][case_type][level_index_map[case_level]][1]
            y = sps / avg_sps
            # 该题的表现系数mu

            case_mu = 1 + 1/7 * math.log(y, 10)
            mu[user_id][case_type][case['case_id']] = case_mu

write_json(score_per_second_cur, "score_per_second_current.json")
write_json(mu, "performance_coefficient.json")
