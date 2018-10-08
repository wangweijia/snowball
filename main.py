from urllib import request, parse, error
import http.cookiejar
import ssl
from jsonToTxt import *
import json

context = ssl._create_unverified_context()
header = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

def initOpener():
    cookie_file = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    return opener

def requestHistory(opener, cube_symbol, page):
    url = 'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol={}&count=20&page={}'
    historyUrl = url.format(cube_symbol, page)
    req = request.Request(url=historyUrl,headers=header)
    response = opener.open(req)

    content = response.read().decode()
    return json.loads(content)

def saveJsonFile(content, fileName, rootPath='.'):
    path = rootPath + '/' + fileName
    f = open(path, 'w', encoding='utf-8')
    f.write(content)
    f.close()

def readJsonFile(fileName, rootPath='.'):
    path = rootPath + '/' + fileName
    with open(path, encoding='utf-8') as file_object:
        contents = file_object.read()
        return contents


def getAllHistory(opener, cube_symbol):
    page = 1
    list = []
    while(1):
        # print(page)
        res = requestHistory(opener, cube_symbol, page)
        list = list + res['list']
        count = res['count']
        totalCount = res['totalCount']
        if count * page >= totalCount:
            return  list
        else:
            page += 1

def getSymbol(opener, cube_symbol):
    list = getAllHistory(opener, cube_symbol)
    listStr = json.dumps(list)
    saveJsonFile(listStr, './symbols'+cube_symbol+'.json')

def getAllSymbol():
    jsonToTxt()
    opener = initOpener()
    with open('./cube_symbol.txt', encoding='utf-8') as file_object:
        line = file_object.readline()
        print(type(line))
        while line:
            print(line)
            getSymbol(opener, line)
            line = file_object.readline()

getAllSymbol()