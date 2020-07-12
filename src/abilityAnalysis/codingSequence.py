import json
import requests
import zipfile as z
import os


# 对字典按值排序，返回键的列表
def my_sort(dic: dict) -> list:
    res = sorted(dic.items(), key=lambda item: item[1])
    for i in range(0, len(res)):
        res[i] = res[i][0]
    return res


def unzip(zip_src, dst_dir):
    fz = z.ZipFile(zip_src, 'r')
    zip_src = fz.namelist()[0]
    fz.extract(zip_src, dst_dir)
    fz = z.ZipFile(zip_src, 'r')
    fz.extract('main.py', dst_dir)


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


def is_face_to_example(code):
    return True if code.count("print") >= 5 else False


if __name__ == '__main__':

    # 统计学生在某题型上的做题顺序
    coding_sequence = {}  # 按照 {'userId': {'case_type': { ... 'caseId': 'uploadTime'}}}存储做题顺序

    with open("../../test_data.json", 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    with open("../difficultyAnalysis/avgScoreCount/case_info.json") as f:
        case_info = json.load(f)

    for user_id in json_data:
        coding_sequence.setdefault(user_id, {})
        for case in json_data[user_id]['cases']:
            case_type = case_info[case['case_id']]['题目类型']
            coding_sequence[user_id].setdefault(case_type, {})
            upload_records = case['upload_records']

            try:
                if case['final_score'] == 100:
                    for record in upload_records:
                        if record['score'] == 100:
                            url = record['code_url']
                            upload_time = record['upload_time']
                            break
                else:
                    url = upload_records[-1]['code_url']
                    upload_time = upload_records[-1]['upload_time']

                # 筛选掉无效（面向用例/非python）的提交
                try:
                    r = requests.get(url)
                    with open("temp", 'wb') as f:
                        f.write(r.content)
                    unzip("temp", os.getcwd())
                    code = open("main.py").read()  # 拿到了提交代码，然后判断是否无效
                    if (not is_face_to_example(code)) and (judge(code) == 1):
                        coding_sequence[user_id][case_type][case['case_id']] = upload_time
                        print(case['case_id'] + 'success')

                # 下载不稳定，有时会中断，暂时没找到解决方法...
                except requests.exceptions.ConnectionError:
                    coding_sequence[user_id][case_type][case['case_id']] = upload_time
                    print(case['case_id'] + 'fail')
                    continue

                # 删除掉已经无用的代码文件和zip包
                for file in os.listdir("../abilityAnalysis"):
                    if file.startswith("main.py") or file.endswith("zip"):
                        os.remove(file)
            except IndexError:
                # upload_records 为空
                print("userId: " + user_id + ", caseId: " + case['case_id'] + ", 数据错误")

    # 改写coding_sequence为 分种类，按照时间顺序完成的case_id列表
    for user_id in coding_sequence:
        for case_type in coding_sequence[user_id]:
            coding_sequence[user_id][case_type] = my_sort(coding_sequence[user_id][case_type])

    json_str = json.dumps(coding_sequence, ensure_ascii=False, indent=4)
    with open("coding_sequence.json", 'w', encoding='utf-8') as f:
        f.write(json_str)
