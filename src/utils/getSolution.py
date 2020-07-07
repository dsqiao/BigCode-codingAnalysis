
import json

solutionToCase={}

with open("../../test_data.json","r",encoding='utf-8') as fp:
    json_data=json.load(fp)
    for user_id in json_data:
        cases = json_data[user_id]['cases']
        for case in cases:
            if case["final_score"]==100:
                upload_records=case["upload_records"]
                url=""
                for record in upload_records:
                    if record["score"]==100:
                        url=record["code_url"]
                        break
                if url=="":
                    pass
                if case["case_id"] not in solutionToCase.keys():
                    solutionToCase.setdefault(case["case_id"],[url])
                else:
                    solutionToCase.get(case["case_id"]).append(url)

json_str = json.dumps(solutionToCase, ensure_ascii=False, indent=4)
with open('../../solution_to_case.json', 'w', encoding='utf-8') as fp:
    fp.write(json_str)
