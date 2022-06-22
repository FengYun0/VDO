import zipfile
from xml.dom.minidom import parse
import datetime
import shutil

def unzip(filename):
    try:
        file = zipfile.ZipFile(filename)
        dirname = filename.replace('.zip', '')
        # 如果存在与压缩包同名文件夹 提示信息并跳过
        if os.path.exists(dirname):
            print('{filename} dir has already existed')
            return
        else:
            # 创建文件夹，并解压
            os.mkdir(dirname)
            file.extractall(dirname)
            file.close()
            ## 递归修复编码
            #rename(dirname)
    except:
        print('{filename} unzip fail')

def rename(pwd, filename=''):
    """压缩包内部文件有中文名, 解压后出现乱码，进行恢复"""
    
    path = '{pwd}/{filename}'
    if os.path.isdir(path):
        for i in os.scandir(path):
            rename(path, i.name)
    newname = filename.encode('cp437').decode('gbk')
    os.rename(path, '{pwd}/{newname}')


def toNumber(txt):
    if txt !='':
        return int(txt)
    else:
        return 0

def toNumberOrNone(txt):
    if txt !='':
        return int(txt)
    else:
        return None

def toMyDate(txt):
    return datetime.datetime.strptime(txt,'%Y%m%d%H%M%S') 
    
def toMyDateOrNone(txt):
    if txt !='':
        return datetime.datetime.strptime(txt,'%Y%m%d%H%M%S')
    else:
        return None
    
def toDict(listkey,listvalue):
    records = {}
    recordsEnum = {k: col for k, col in enumerate(listkey)}
    for i in range(1000):
        try:
            records[recordsEnum[i]]=listvalue[i]
        except (KeyError, IndexError) as e:
            break
    return records

def getDateTime(txt):
    t=re.search("(\d{4}\d{1,2}\d{1,2}\d{1,2}\d{1,2}\d{1,2})",txt)
    if t:
        return t.group(1)
    else:
        return '19700101000000'
#===============================================================================
