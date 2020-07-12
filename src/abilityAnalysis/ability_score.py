import json


def load_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(d: dict, file_path: str):
    json_str = json.dumps(d, ensure_ascii=False, indent=4)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)


if __name__ == '__main__':
    coding_sequence = load_json("coding_sequence.json")
    basic_score = load_json("basic_score/basic_score.json")
    attenuation = load_json("attenuation_coefficient/attenuation_coefficient.json")
    performance = load_json("performance_coefficient/performance_coefficient.json")

    # 记录学生学习能力评分变化
    # {
    #     "user_id": {
    #         ...
    #         "case_type": [
    #             [ 当前能力得分, 1(当前题目完成数量) ],
    #             [ 当前能力得分, 2 ]
    #         ],
    #     },
    # }
    ability_score = {}

    for user_id in coding_sequence:
        ability_score.setdefault(user_id, {})
        for case_type in coding_sequence[user_id]:
            ability_score[user_id].setdefault(case_type, [])
            for i in range(0, len(coding_sequence[user_id][case_type])):
                case_id = coding_sequence[user_id][case_type][i]
                new_score_added = basic_score[user_id][case_type][case_id] * \
                                  attenuation[user_id][case_type][case_id] * \
                                  performance[user_id][case_type][case_id]
                if i == 0:
                    ability_score[user_id][case_type].append((new_score_added, 1))
                else:
                    ability_score[user_id][case_type].append(
                        (ability_score[user_id][case_type][-1][0] + new_score_added, i+1)
                    )

    print(ability_score)
    write_json(ability_score, "ability_score.json")
