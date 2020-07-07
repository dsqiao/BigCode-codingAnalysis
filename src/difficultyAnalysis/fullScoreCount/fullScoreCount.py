import json

with open("../../../test_data.json",'r',encoding="utf-8") as f:
    json_data = json.load(f)


user_ids = []
for key in json_data.keys():
    user_ids.append(key)

case_ids = []
case_full_score = {}  # 统计每题满分人数的字典，按照{case_id:[累计作答人数，满分人数]}存储数据
case_info_fullNum = {}  # 统计每题信息字典，按照{case_id:['题目类型':'', '作答人数':''，'满分人数':''，'满分比例':'']}存储数据
for user_id in user_ids:
    cases = json_data[user_id]['cases']
    for case in cases:
        if case['case_id'] not in case_ids:
            case_ids.append(case['case_id'])
            case_info_fullNum.setdefault(case['case_id'],{'题目类型': case['case_type'],'题目地址': case['case_zip']})
            if case['final_score'] == 100:
                case_full_score.setdefault(case['case_id'],[1,1])
            else:
                case_full_score.setdefault(case['case_id'],[1,0])
        else:
            case_full_score[case['case_id']][0] += 1
            if case['final_score'] == 100 :
                case_full_score[case['case_id']][1] += 1  # 满分，增加满分人数

for key in case_full_score:
    case_info_fullNum[key]['作答人数'] = case_full_score[key][0]
    case_info_fullNum[key]['满分人数'] = case_full_score[key][1]
    case_info_fullNum[key]['满分比例'] = case_full_score[key][1] / case_full_score[key][0]
    case_info_fullNum[key]['index'] = (1 - case_info_fullNum[key]['满分比例']) * 100  # 该项得分 = 1 - 满分比例（100分制）

json_str = json.dumps(case_info_fullNum,ensure_ascii=False, indent=4)
with open('./case_info_fullCount.json','w',encoding='utf-8') as fp:
    fp.write(json_str)
