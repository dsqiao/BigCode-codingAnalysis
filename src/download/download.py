import json
import urllib.request, urllib.parse
import os
import zipfile


def download(baseUrl, jsonPath, baseStorage):
    f = open(jsonPath, encoding='utf-8')
    res = f.read()
    data = json.loads(res)  # 将res字符串转成json对象
    for userId in data:
        cases = data[userId]["cases"]
        if os.path.exists(userId):
            os.removedirs(userId)
        baseDir = os.path.join(baseStorage, userId)
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        for case in cases:
            url = baseUrl + urllib.parse.quote(os.path.basename(case["case_zip"]))  # 中文转码url
            storage = os.path.join(baseDir, os.path.basename(case["case_zip"]))  # 存储地址
            if not os.path.exists(storage):
                urllib.request.urlretrieve(url, storage)


def un_zip(file_name):
    if not os.path.exists(file_name[:-4]):
        os.mkdir(file_name[:-4])  # 建立文件夹
        zip_file = zipfile.ZipFile(file_name)
        # print(zip_file)
        for name in zip_file.namelist():
            zip_file.extract(name, file_name[:-4])  # 解压
        zip_file.close()
    if os.path.exists(file_name):  # 删除zip文件
        os.remove(file_name)


def un_zip_tree(baseStorage):
    for dir in os.listdir(baseStorage):
        dirpath = os.path.join(baseStorage, dir)
        # print(dirpath)
        # print(len(os.listdir(dirpath)))
        for file in os.listdir(dirpath):
            filepath = os.path.join(dirpath, file)
            # print(filepath)
            un_zip(filepath)


if __name__ == '__main__':
    baseUrl = "http://mooctest-site.oss-cn-shanghai.aliyuncs.com/target/"
    baseStorage = "../../data"
    if not os.path.exists("../../data"):
        os.makedirs("../../data")
    jsonPath = "../../test_data.json"
    download(baseUrl, jsonPath, baseStorage)
    un_zip_tree(baseStorage)
