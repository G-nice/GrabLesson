import json
import threading
import urllib.request
import urllib.parse

import time

import Config
import info
import LoginUtils


# http://xk2.cqupt.edu.cn/data/json-data.php?type=zyk

def get_classes(url, cookie):
    choice = info.choose_type()
    url = url + Config.show_class_api + '?type='
    if choice is 'e':
        return -1
    elif choice is '1':
        url += 'zyk'
    else:
        url += 'rx'
    opener = LoginUtils.get_opener(cookie)
    response = opener.open(url)
    result = json.JSONDecoder().decode(response.read().decode('utf8'))
    data = result['data']
    if data.__len__() is 0:
        print(result['info'] + '\n')
    return data


class Classes:
    def __init__(self, url, cookie):
        self.classes = {}
        self.url = url
        self.cookie = cookie

    def select(self, ticktock=3, count=-1):
        self.classes.clear()
        result = get_classes(self.url, self.cookie)
        if result is -1:
            exit(0)
        self.classes.update(result)
        if self.classes.__len__() is 0:
            return
        choice = info.print_all(self.classes)
        if choice is -1:
            return
        return self.choose_class(choice, count, ticktock)

    def choose_class(self, cid, count, ticktock):
        keys = list(self.classes.keys())
        target = self.classes[keys[cid]]
        if count > -1:
            return ChooseClass(target, self.url, ticktock, '抢课姬' + str(count), True)
        else:
            return ChooseClass(target, self.url, ticktock)


class ChooseClass(threading.Thread):
    def __init__(self, data, url, ticktock, name=None, female=False):
        super().__init__()
        self.data = data
        self.data['isOver'] = 0
        self.data['isTyfx'] = 0
        self.url = url
        if name is not None:
            self.name = name
        self.female = female
        self.ticktock = ticktock

    def start(self):
        while 1:
            try:
                request = urllib.request.Request(self.url + Config.class_api)
                data = urllib.parse.urlencode(self.data).encode('utf8')
                response = urllib.request.urlopen(request, data).read()
                result = json.loads(response.decode('utf8'))
                second = time.strftime('%H:%M:%S', time.localtime(time.time()))
                if result['code'] == 0 or result['info'] == 'OK':
                    if self.female:
                        print(second + " : " + '主人，主人，我抢到了！~\(≧▽≦)/~')
                    else:
                        print(second + " : " + str(result['info']))
                    break
                else:
                    if self.female:
                        print(second + " : " + '主人，人家抢不到嘛！╮(╯▽╰)╭')
                    else:
                        print(second + " : " + str(result['info']))
                    time.sleep(self.ticktock)
            except Exception as e:
                second = time.strftime('%H:%M:%S', time.localtime(time.time()))
                if self.female:
                    print(second + " : " + '主人，人家出错了！╯﹏╰')
                else:
                    print(second + " : " + str(e))
                time.sleep(self.ticktock)
