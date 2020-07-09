import json
import numpy as np

# 读取json文件并写入为字典格式
with open("../../../test_data.json", 'r', encoding='utf-8') as fp:
    json_data = json.load(fp)

# 读取所有user_id
user_ids = []
for key in json_data.keys():
    user_ids.append(key)

# 读取所有case_id
case_ids = []
case_average_upload_intervals = {}
case_info = {}  # 统计每题信息的字典
for user_id in user_ids:
    cases = json_data[user_id]['cases']
    for case in cases:
        upload_records = case['upload_records']
        intervals = 0
        if len(upload_records) > 0:
            intervals = upload_records[-1]["upload_time"] - upload_records[0]["upload_time"]
        if case['case_id'] not in case_ids:  # 发现新的题目
            case_ids.append(case['case_id'])
            case_info.setdefault(case['case_id'], {'题目类型': case['case_type'], '题目地址': case['case_zip']})
            case_average_upload_intervals.setdefault(case['case_id'], [intervals])
        else:  # 已有题目
            case_average_upload_intervals.get(case['case_id']).append(intervals)

for case_id in case_average_upload_intervals.keys():
    case_info.get(case_id).setdefault('标准化后平均提交时间间隔', np.log10(np.average(case_average_upload_intervals.get(case_id))))

average_upload_time = []
for case_id in case_info:
    average_upload_time.append(case_info[case_id]['标准化后平均提交时间间隔'])

max_upload_time = np.max(average_upload_time)
min_upload_time = np.min(average_upload_time)

for case_id in case_average_upload_intervals.keys():
    case_info.get(case_id).setdefault('index', (case_info.get(case_id)['标准化后平均提交时间间隔'] - min_upload_time) / (
                max_upload_time - min_upload_time) * 100)

json_str = json.dumps(case_info, ensure_ascii=False, indent=4)
with open('case_info_uploadIntervals.json', 'w', encoding='utf-8') as fp:
    fp.write(json_str)
