import os



def getFiles(baseDir):
    dirs = os.listdir(baseDir)
    for d in dirs:
        filepath = os.path.join(baseDir, d)
        if os.path.isdir(filepath):
            getFiles(filepath)
        elif os.path.isfile(filepath) and (filepath.endswith("answer.cpp") or filepath.endswith("answer.py")):
            res.append(filepath)


def postfix_change(filelist):
    for name in filelist:
        if name.endswith(".cpp"):
            newname = name.replace(".cpp", ".txt")
            os.rename(name, newname)
        elif name.endswith(".py"):
            newname=name.replace(".py",".txt")
            os.rename(name,newname)

if __name__ == '__main__':
    baseDir = "../../data"
    res = []
    getFiles(baseDir)
    print(res)
    postfix_change(res)
