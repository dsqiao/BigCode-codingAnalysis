import json
import os

avgScore_path = "../avgScoreCount/case_info.json"
codeLineCount_path = "../codeLineCount/line_count.json"
faceToExample_path = "../faceToExampleCount/case_info_face_to_example.json"
fullScoreCount_path = "../fullScoreCount/case_info_fullCount.json"
langJudge_path = "../langJudge/lang_result.json"
uploadIntervals_path = "../uploadIntervals/case_info_uploadIntervals.json"
uploadTimesBeforeFull_path = "../uploadTimesBeforeFull/case_info_uploadTimes.json"

final_score = {}


def addToFinal(file_path, weight):
    with open(file_path, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
        for case in json_data:
            final_score.setdefault(case, {'score': 0})
            final_score.get(case)['score'] += json_data.get(case)['index'] * weight


addToFinal(avgScore_path, 0.2)
addToFinal(codeLineCount_path, 0.1)
addToFinal(faceToExample_path, 0.15)
addToFinal(fullScoreCount_path, 0.2)
addToFinal(langJudge_path, 0.15)
addToFinal(uploadIntervals_path, 0.05)
addToFinal(uploadTimesBeforeFull_path, 0.15)

final_scores = []
for case in final_score:
    final_scores.append(final_score.get(case)['score'])

min_final_scores = min(final_scores)
max_final_scores = max(final_scores)

count = 0
for case in final_score:
    index = (final_score.get(case)['score'] - min_final_scores) / (max_final_scores - min_final_scores) * 100
    final_score.get(case)['index'] = index
    if 0 <= index < 10:
        final_score.get(case)['level'] = '简单'
    elif index < 20:
        final_score.get(case)['level'] = '中等'
    elif index < 40:
        final_score.get(case)['level'] = '较难'
    elif index < 60:
        final_score.get(case)['level'] = '困难'
    else:
        final_score.get(case)['level'] = '地狱'

json_str = json.dumps(final_score, ensure_ascii=False, indent=4)
with open('final_score.json', 'w', encoding='utf-8') as fp:
    fp.write(json_str)

print(count)
