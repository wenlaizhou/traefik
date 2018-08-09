# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import os
from datetime import datetime
import sys
import traceback
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')


class Preconditions:
    """
    pre condition check

    """

    def __init__(self):
        pass

    @staticmethod
    def checkArguments(expr):
        if not expr:
            raise AssertionError('illegal arguments')
        pass

    @staticmethod
    def checkString(arg):
        if arg and arg is not 0 and arg is not True:
            return
        else:
            raise AssertionError('illegal arguments')

    @staticmethod
    def checkNotNull(*arg):
        if arg is not None:
            return
        else:
            raise AssertionError('illegal arguments')

    @staticmethod
    def checkCollection(arg):
        if arg and arg is not 0 and arg is not True:
            return
        else:
            raise AssertionError('illegal arguments')


class DbUtils:
    """
    db tools

    """

    def __init__(self):
        pass

    @staticmethod
    def execute(connMap, sql, params):
        """
        exec sql string

        :param connMap : like this : {
            'host' : 'localhost',
            'port' : 1024,
            'user' : 'root',
            'password' : 'chj',
            'db' : 'hello'
        }

        :param sql: sql

        :param params: tuple (1, '18611145474', 2, )

        :return: data or lines number
        """
        from datetime import datetime
        import mysql.connector as db
        Preconditions.checkCollection(connMap)
        Preconditions.checkString(sql)
        connection = None
        result = []
        try:
            connection = db.connect(host=connMap['host'],
                                    port=connMap['port'],
                                    user=connMap['user'],
                                    password=connMap['password'],
                                    db=connMap['db'])
            sql = sql.strip()
            cur = connection.cursor()
            if sql.startswith("select") or sql.startswith("show"):
                cur.execute(sql, params=params)
                fetchData = cur.fetchall()
                if fetchData and len(fetchData) > 0:
                    for row in fetchData:
                        rowRes = {}
                        for columnIndex in range(len(row)):
                            columnData = row[columnIndex]
                            if columnData:
                                if isinstance(columnData, datetime):
                                    rowRes[cur.column_names[
                                        columnIndex]] = format(
                                        columnData,
                                        columnData.strftime('%Y-%m-%d %H:%M:%S'))
                                else:
                                    rowRes[cur.column_names[columnIndex]] = row[columnIndex]
                            else:
                                rowRes[cur.column_names[columnIndex]] = ''
                        result.append(rowRes)
                    return result
                else:
                    return []
            else:
                cur.execute(sql, params=params)
                connection.commit()
                result = cur.lastrowid
                if result <= 0:
                    result = cur.rowcount
                return result

        except Exception, e:
            print "error"
            print e
            print e.message
            # raise e
            pass
        finally:
            if connection is not None:
                connection.close()
        pass

    pass


def get(url, headers=None):
    """
    get url

    :param url: url

    :param headers: headers

    :return: code, headers, data
    """
    import urllib2
    try:
        req = urllib2.Request(url)
        if headers:
            for k in headers:
                v = headers[k]
                req.add_header(k, v)
        resp = urllib2.urlopen(req)
        return 200, resp.headers.dict, resp.read()
    except urllib2.HTTPError, e:
        return e.code, {}, e.read()
    except urllib2.URLError, e:
        raise e
    pass


def postForm(url, headers=None, data=None):
    """
    post form数据

    :param url:

    :param headers:

    :param data:

    :return: code, headers, data
    """
    import urllib
    if data:
        data = urllib.urlencode(data)
    if headers:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    else:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    return doRequest(url, headers, data)


def postJson(url, headers=None, data=None):
    """
    直接post json数据

    并添加Content-Type : application/json 头

    :param url:
    :param headers:
    :param data:
    :return: code, headers, data
    """
    if not headers:
        headers = {}
    headers['Content-Type'] = 'application/json'
    if isinstance(data, dict):
        data = json.dumps(data)
    return doRequest(url, headers=headers, data=data)
    pass


def post(url, headers=None, data=None):
    """
    发送post请求

    :param url: url

    :param headers: headers

    :param data: post data

    :return: code, headers, data
    """
    return doRequest(url=url, headers=headers, data=data)


def doRequest(url, headers=None, data=None, method='POST'):
    """
    发送请求
    默认post

    :param url: url

    :param headers: headers

    :param data: post data

    :param method: method

    :return: code, headers, data
    """
    if not url:
        raise Exception('utils.post : url is null')
    import urllib2
    try:
        req = urllib2.Request(url)
        if headers:
            for k in headers:
                v = headers[k]
                req.add_header(k, v)
        if data:
            req.add_data(data=data)
        req.get_method = lambda: method
        resp = urllib2.urlopen(req)
        return 200, resp.headers.dict, resp.read()
    except urllib2.HTTPError, e:
        return e.code, {}, e.read()
    except urllib2.URLError, e:
        raise e
    pass


def execute(cmd):
    """
    执行系统命令

    :param cmd: 系统命令

    :return: result, pid
    """

    Preconditions.checkString(cmd)
    import os
    _, stdOut = os.popen2(cmd)
    res = stdOut.readlines()
    pid = os.getpid()
    return res, pid


def zip_dir(dirname, zipfilename):
    """
    使用zip进行目录打包

    :param dirname:
    :param zipfilename:
    :return:
    """
    import os, zipfile
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()


def writeFile(fileName, content):
    """
    直接写入文件, 并在写入完毕关闭文件句柄

    如果文件不存在则创建文件

    :param fileName: 文件名
    :param content: 文件内容
    :return: None
    """
    with open(fileName, 'w+') as fs:
        fs.write(content)
    pass


def appendLine(fileName, content):
    """
    直接在文件末尾添加一行, 并在写入完毕关闭文件句柄

    如果文件不存在则创建文件

    :param fileName: 文件名
    :param content: 文件内容
    :return:
    """
    with open(fileName, 'a+') as fs:
        if os.path.exists(fileName):
            fs.write('\n')
        fs.write(content)
    pass


def inputPass(msg):
    """
    获取密码输入

    :param msg:

    :return:
    """
    import getpass
    return getpass.getpass(msg)


def fileReplace(fileName, oldContent, newContent):
    """
    文件内容替换

    :param fileName: 文件名

    :param oldContent: 旧文件内容

    :param newContent: 新文件内容

    :return:
    """
    fileContent = ''
    with open(fileName) as fs:
        fileContent = fs.read()
    return fileContent.replace(oldContent, newContent)


def readFile(fileName):
    """
    读取文件内容
    文件不存在则返回None

    :param fileName:
    :return:
    """
    if os.path.exists(fileName):
        with open(fileName) as fs:
            return fs.read()
    return None


def readLines(fileName):
    """
    读取文件内容
    按行读取
    文件不存在则返回None

    :param fileName:
    :return:
    """
    if os.path.exists(fileName):
        with open(fileName) as fs:
            return fs.readlines()
    return None


def guid():
    """
    返回32位guid字符串

    伪随机

    :return: 大写32位随机串
    """
    return uuid.uuid4().hex.upper()


def parseJson(string):
    """
    字符串转换为json对象

    :param string:
    :return: 转换失败返回:None
    """
    if not string:
        return None
    try:
        return json.loads(string)
    except Exception, e:
        return None


def getStacktrace():
    """
    获取堆栈信息

    :return: 堆栈信息
    """
    return traceback.format_exc()


def utf2datetime(utcStr):
    # UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    UTC_FORMAT_A = "%Y-%m-%dT%H:%MZ"
    UTC_FORMAT_B = "%Y-%m-%dT%H:%M:%SZ"
    try:
        return datetime.strptime(utcStr, UTC_FORMAT_A)
    except:
        return datetime.strptime(utcStr, UTC_FORMAT_B)


def restResponse(code, message, data):
    """
    返回 rest类型 flask-Response

    :param data: data
    :param message: message
    :param code: code
    :return: flask.Response
    """
    from flask import Response
    return Response(response=json.dumps({
        'code': code,
        'message': message,
        'data': data
    }), content_type='application/json; charset=utf-8')


def getGoDeps(sourcePath="."):
    """
    获取指定路径下所有golang代码依赖

    :param sourcePath: 代码根目录, 默认为当前目录
    :return: 依赖列表
    """
    import os, re, itertools

    importsDict = {}
    imports = []

    multiLineImportRegex = re.compile('''import \((.*?)\)''', flags=re.MULTILINE + re.DOTALL)
    simpleImportRegex = re.compile('''import "(.*?)"''')

    for root, dirs, files in os.walk(sourcePath):
        for f in files:
            if not f.endswith('.go'):
                continue

            fileName = "{}{}{}".format(root, os.path.sep, f)
            with open(fileName) as fs:
                fileContent = fs.read()
                multiImports = multiLineImportRegex.findall(fileContent)
                singleImports = simpleImportRegex.findall(fileContent)
                for i in itertools.chain(multiImports, singleImports):
                    i = i.strip()
                    if not i:
                        continue
                    if '"' in i:
                        words = i.split('"')
                        for w in words:
                            w = w.strip()
                            if w:
                                importsDict[w] = True
                    else:
                        importsDict[i] = True

    for k in importsDict:
        if re.match("(\w+\.\w+)", k):
            imports.append(k)
    return imports
    pass
