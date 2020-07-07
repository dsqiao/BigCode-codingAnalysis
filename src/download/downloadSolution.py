import json
import urllib.request, urllib.parse
import os
import zipfile


def download(baseUrl, jsonPath, baseStorage):
    f = open(jsonPath, encoding='utf-8')
    res = f.read()
    data = json.loads(res)  # 将res字符串转成json对象
    for case_id in data:
        path=os.path.join(baseStorage,case_id)
        if not os.path.exists(path):
            os.makedirs(path)
        for url in data[case_id]:
            storage=os.path.join(path,urllib.parse.unquote(os.path.basename(url)))
            print(storage)
            if not os.path.exists(storage):
                urllib.request.urlretrieve(url, storage)


def un_zip2(file_name):
    if zipfile.is_zipfile(file_name) and not os.path.exists(file_name[:-4]):
        os.mkdir(file_name[:-4])
        zip_file=zipfile.ZipFile(file_name)
        for name in zip_file.namelist():
            try:
                zip_file.extract(name,file_name[:-4])
                new_file_name = os.path.join(file_name[:-4], name)
                un_zip2(new_file_name)
            except:
                pass
        zip_file.close()
        os.remove(file_name)
    elif os.path.isdir(file_name):
        for name in os.listdir(file_name):
            new_file_name=os.path.join(file_name,name)
            un_zip2(new_file_name)


def un_zip_tree(baseStorage):
    for dir in os.listdir(baseStorage):
        dirpath = os.path.join(baseStorage, dir)
        # print(dirpath)
        # print(len(os.listdir(dirpath)))
        for file in os.listdir(dirpath):
            filepath = os.path.join(dirpath, file)
            # print(filepath)
            un_zip2(filepath)


if __name__ == '__main__':
    baseUrl = "http://mooctest-site.oss-cn-shanghai.aliyuncs.com/target/"
    baseStorage = "../../data/solutions"
    if not os.path.exists("../../data/solutions"):
        os.makedirs("../../data/solutions")
    jsonPath = "../../solution_to_case.json"
    download(baseUrl, jsonPath, baseStorage)
    un_zip_tree(baseStorage)