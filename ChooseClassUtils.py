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
    if choice is '1':
        url += 'zyk'
    elif choice is '2':
        url += 'rx'
    opener = LoginUtils.get_opener(cookie)
    response = opener.open(url)
    result = json.JSONDecoder().decode(response.decode('utf8'))['data']
    print(result)
    return result


class Classes:
    def __init__(self, url, cookie):
        self.classes = []
        self.url = url
        self.cookie = cookie

    def select(self, ticktock=3, count=-1):
        self.classes.clear()
        self.classes.append(get_classes(self.url, self.cookie))
        choice = info.print_all(self.classes)
        if choice is -1:
            return
        return self.choose_class(choice, count, ticktock)

    def choose_class(self, cid, count, ticktock):
        target = self.classes[cid]
        if count > -1:
            return ChooseClass(target, self.url, ticktock, '抢课姬' + str(count), True)
        else:
            return ChooseClass(target, self.url, ticktock)


class ChooseClass(threading.Thread):
    def __init__(self, data, url, ticktock, name=None, female=False):
        super().__init__()
        self.data = data
        self.url = url
        if name is not None:
            self.name = name + super()._name
        self.female = female
        self.ticktock = ticktock

    def start(self):
        while 1:
            try:
                request = urllib.request.Request(self.url)
                data = urllib.parse.urlencode(self.data)
                data = data.encode(encoding='UTF8')
                response = urllib.request.urlopen(request, data)
                response = response.read()
                result = json.loads(response.decode('UTF8'))
                if result['code'] == 0 or result['info'] == 'OK':
                    if self.female:
                        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + '主人，主人，我抢到了！')
                    else:
                        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + str(result['info']))
                    break
                else:
                    if self.female:
                        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + '主人，人家抢不到嘛！')
                    else:
                        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + str(result['info']))
                    time.sleep(self.ticktock)
            except:
                if self.female:
                    print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + '主人，人家出错了！')
                else:
                    print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + " : " + "ERROR!")
                time.sleep(self.ticktock)
