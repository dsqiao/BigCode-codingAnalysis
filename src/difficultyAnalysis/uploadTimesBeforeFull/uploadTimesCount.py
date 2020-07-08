import json

with open("../../../test_data.json",'r',encoding="utf-8") as f:
    json_data = json.load(f)

user_ids = []
for key in json_data.keys():
    user_ids.append(key)

case_ids = []
case_upload_times = {}  # 统计每题满分前提交次数的字典，按照{case_id:[满分人数，总共提交次数]存储数据
case_info_uploadTimes = {}  # 统计每道信息的字典，按照{case_id:['题目类型':'', '满分人数':''，'平均提交次数':'']存储数据

for user_id in user_ids:
    cases = json_data[user_id]['cases']
    for case in cases:
        if case['case_id'] not in case_ids:
            case_ids.append(case['case_id'])
            case_info_uploadTimes.setdefault(case['case_id'],{'题目类型': case['case_type'],'题目地址': case['case_zip']})
            if case['final_score'] == 100:  # 满分，计算提交次数
                uploadTimes = 1  # 初始值为1，至少提交1次
                for uploadRecord in case['upload_records']:
                    if uploadRecord['score'] != 100:
                        uploadTimes += 1
                case_upload_times.setdefault(case['case_id'],[1,uploadTimes])
            else:  # 没有满分
                case_upload_times.setdefault(case['case_id'],[0,0])
        else:
            if case['final_score'] == 100:
                case_upload_times[case['case_id']][0] += 1
                uploadTimes = 1
                for uploadRecord in case['upload_records']:
                    if uploadRecord['score'] != 100:
                        uploadTimes += 1
                case_upload_times[case['case_id']][1] += uploadTimes

maxUploadTimes = 1
minUploadTimes = 1
for key in case_upload_times:
    case_info_uploadTimes[key]['满分人数'] = case_upload_times[key][0]
    case_info_uploadTimes[key]['平均提交次数'] = case_upload_times[key][1] / case_upload_times[key][0]
    maxUploadTimes = max(maxUploadTimes,case_info_uploadTimes[key]['平均提交次数'])
    minUploadTimes = min(minUploadTimes,case_info_uploadTimes[key]['平均提交次数'])

# print(maxUploadTimes)
# print(minUploadTimes)

for key in case_upload_times:
    case_info_uploadTimes[key]['index'] = (case_info_uploadTimes[key]['平均提交次数']-minUploadTimes) * 100 / (maxUploadTimes - minUploadTimes)


json_str = json.dumps(case_info_uploadTimes,ensure_ascii=False, indent=4)
with open('./case_info_uploadTimes.json','w',encoding='utf-8') as fp:
    fp.write(json_str)
