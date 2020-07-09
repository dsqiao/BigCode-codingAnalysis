import os
import json


# 判断是否是python作答
# 返回值：（1 => 很可能为python） ; （-1 => 很可能不为python）; （0 => 无法确定）
def judge(code):
    for i in range(0, len(code)):
        # 检索出5份疑似c++代码
        if code[i:i+11] == '# include <':
            return -1
        # 检索出 6 份疑似java代码
        if code[i:i+17] == 'System.out.print(':
            return -1
        # 检索出13份疑似java代码
        if code[i:i+19] == 'System.out.println(':
            return -1
        # 这个条件筛选出 267 道疑似cpp答案
        if code[i:i+11] == 'int main(){':
            return -1
        # 这个条件单独删选出 137 道疑似cpp答案
        if code[i:i+12] == 'int main() {':
            return -1
        # 这个条件筛选出 562 道疑似cpp答案
        if code[i:i+9] == '#include<':
            return -1
        # 这个条件单独筛选出 309道 疑似 cpp答案
        if code[i:i+10] == '#include <':
            return -1
        # 1份
        if code[i:i+10] == '#include "':
            return -1
        # 1份疑似C语言
        if code[i:i+7] == 'printf(':
            return -1
        if code[i:i+6] == 'print(':
            return 1
        if code[i:i+7] == 'print (':
            return 1
        if code[i:i+7] == 'input()':
            return 1
        if code[i:i+9] == 'sys.stdin':
            return 1
        # 6份
        if code[i:i+26] == "if __name__ == '__main__':":
            return 1
        # 15份
        if code[i:i+17] == 'sys.stdout.write(':
            return 1
    return 0


if __name__ == '__main__':
    root = '../../../data/solutions'
    case_lang = {}  # 按照{'case_id': {'python':'', '非python':'', '无法确定': '', ratio:'', 'index':''}}储存每题语言使用情况
    case_ids = os.listdir(root)
    count = 0
    for case_id in case_ids:
        if case_id != '.DS_Store':  # 不考虑隐藏文件
            case_lang.setdefault(case_id, {'python': 0, '非python': 0, '无法确定': 0, 'ratio': 0, 'index': 0})
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
                        judge_res = judge(main)
                        if judge_res == -1:
                            case_lang[case_id]['非python'] += 1
                        elif judge_res == 1:
                            case_lang[case_id]['python'] += 1
                        else:
                            count += 1
                            print(root + '/' + case_id + '/' + code + '/' + file + '/main.py')
                            case_lang[case_id]['无法确定'] += 1

    # 有两份无法确定的答案
    # 2084 非负权单源最短路_1584632127381 和 2080 广度优先遍历图_1584592949661
    print(count)
    maxRatio = 0
    minRatio = 1
    for case_id in case_lang:
        ratio = case_lang[case_id]['非python'] / (case_lang[case_id]['非python'] + case_lang[case_id]['python'])
        case_lang[case_id]['ratio'] = ratio
        if ratio > maxRatio:
            maxRatio = ratio
        if ratio < minRatio:
            minRatio = ratio

    for case_id in case_lang:
        case_lang[case_id]['index'] = (case_lang[case_id]['ratio'] - minRatio) * 100 / (maxRatio - minRatio)
    json_str = json.dumps(case_lang, ensure_ascii=False, indent=4)
    with open('lang_result.json', 'w', encoding='utf-8') as fp:
        fp.write(json_str)
