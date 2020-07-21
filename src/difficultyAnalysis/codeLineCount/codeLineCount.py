import os
import json


# 数一数代码有几行
def line_count(code):
    res = 1
    for c in code:
        if c == '\n':
            res += 1
    return res


current_path = os.getcwd()
root_path = ""
for i in range(0, len(current_path)):
    root_path += current_path[i]
    if current_path[i + 1:i + 4] == 'src':
        break

if __name__ == '__main__':
    root = '../../../data/solutions'
    case_line_statistics = {}  # 按照{'case_id': {'总答题数':'', '平均答题行数':'', 'index': ''}}储存每题行数情况
    case_ids = os.listdir(root)
    count = 0
    for case_id in case_ids:
        if case_id != '.DS_Store':  # 不考虑隐藏文件
            case_line_statistics.setdefault(case_id, {'满分答题数': 0, '平均答题行数': 0, 'index': 0})
            code_list = os.listdir(root + '/' + case_id)
            for code in code_list:
                if code[-4:] != '.zip' and code != '.DS_Store':  # 不考虑zip文件和隐藏文件
                    files = os.listdir(root + '/' + case_id + '/' + code)
                    if len(files) > 0:
                        if files[0] != '.DS_Store':
                            file = files[0]
                        else:
                            file = files[1]

                        # 获取作答代码
                        main = open(root + '/' + case_id + '/' + code + '/' + file + '/main.py').read()
                        line_num = line_count(main)
                        case_line_statistics[case_id]['平均答题行数'] += line_num
                        case_line_statistics[case_id]['满分答题数'] += 1
    for case_id in case_line_statistics:
        case_line_statistics[case_id]['平均答题行数'] /= case_line_statistics[case_id]['满分答题数']

    max_line = 0  # 2149最长182行，寻找LCT，大部分答案面向用例，这题面向用例的输出极多，故平均行数多
    min_line = 100  # 2990最短的不到4行，将输入的两个字符串连接，输出
    for case_id in case_line_statistics:
        a = case_line_statistics[case_id]['平均答题行数']
        if a > max_line:
            max_line = a
        if a < min_line:
            min_line = a

    for case_id in case_line_statistics:
        x = case_line_statistics[case_id]['平均答题行数']
        index = (x - min_line) * 100 / (max_line - min_line)
        case_line_statistics[case_id]['index'] = index

    json_str = json.dumps(case_line_statistics, ensure_ascii=False, indent=4)
    storage_path = root_path + "/src/difficultyAnalysis/codeLineCount/line_count.json"
    with open(storage_path, 'w', encoding='utf-8') as fp:
        fp.write(json_str)
