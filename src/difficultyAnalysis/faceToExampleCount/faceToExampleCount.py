import os
import json
import numpy as np


def is_face_to_example(file):
    with open(file, 'r', encoding='utf-8') as f:
        res = f.read()
        return True if res.count("print") >= 5 else False


if __name__ == '__main__':
    with open("../../../test_data.json", 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    # 读取所有user_id
    user_ids = []
    for key in json_data.keys():
        user_ids.append(key)

    # 读取所有case_id
    case_ids = []
    case_info = {}  # 统计每题信息的字典
    for user_id in user_ids:
        cases = json_data[user_id]['cases']
        for case in cases:
            if case['case_id'] not in case_ids:  # 发现新的题目
                case_ids.append(case['case_id'])
                case_info.setdefault(case['case_id'],
                                     {'题目类型': case['case_type'], '题目地址': case['case_zip']})  # 初始化case_info
    proportions = []
    base_dir = "../../../data/solutions"
    for case in os.listdir(base_dir):
        case_dir = os.path.join(base_dir, case)
        case_info.get(case)['解答数量'] = len(os.listdir(case_dir))
        count = 0
        for answer in os.listdir(case_dir):
            answer_dir = os.path.join(case_dir, answer)
            result_list = os.listdir(answer_dir)
            if len(result_list) > 0:
                result_path = os.path.join(answer_dir, result_list[0])
                final_list = os.listdir(result_path)
                if len(final_list) > 0:
                    final_path = os.path.join(result_path, final_list[2])
                    if is_face_to_example(final_path):
                        print("Face_To_Example:True")
                        count += 1
                    else:
                        print("Face_To_Example:False")
                    print(final_path + ":finished")
        case_info.get(case)['面向用例数量'] = count
        proportion = case_info.get(case)['面向用例数量'] / case_info.get(case)['解答数量']
        case_info.get(case)['面向用例比例'] = proportion
        proportions.append(proportion)
    max_proportion = np.max(proportions)
    min_proportion = np.min(proportions)
    for case in case_info:
        case_info.get(case)['index'] = (case_info.get(case)['面向用例比例'] - min_proportion) / (
                    max_proportion - min_proportion) * 100
    json_str = json.dumps(case_info, ensure_ascii=False, indent=4)
    with open('case_info_face_to_example.json', 'w', encoding='utf-8') as fp:
        fp.write(json_str)
