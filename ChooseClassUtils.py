import json
import threading
import urllib.request
import urllib.parse

import time

import Config
import info


def get_classes(url, opener):
    choice = info.choose_type()
    url = url + Config.show_class_api + '?type='
    if choice is 'e':
        return -1
    elif choice is '1':
        url += 'zyk'
    else:
        url += 'rx'
    response = opener.get_opener().open(url)
    result = json.JSONDecoder().decode(response.read().decode('utf8'))
    data = result['data']
    if data.__len__() is 0:
        print(result['info'] + '\n')
    return data


class Classes:
    def __init__(self, url, opener):
        self.classes = {}
        self.url = url
        self.opener = opener

    def select(self):
        self.classes.clear()
        result = get_classes(self.url, self.opener)
        if result is -1:
            exit(0)
        self.classes.update(result)
        if self.classes.__len__() is 0:
            return
        choice = info.print_all(self.classes)
        if choice is -1:
            return
        return self.choose_class(choice)

    def choose_class(self, cid):
        self.opener.get_opener()
        ticktock = 3
        keys = list(self.classes.keys())
        target = self.classes[keys[cid]]
        params = get_params()
        if params[0] is '':
            return ChooseClass(target, self.opener, self.url, ticktock)
        else:
            try:
                if params[1] is '1':
                    return ChooseClass(target, self.opener, self.url, int(params[0]), True)
            except IndexError:
                return ChooseClass(target, self.opener, self.url, int(params[0]))


def get_params():
    params = input('请输入参数，默认为空：')
    params = params.split(',')
    return params


class ChooseClass(threading.Thread):
    def __init__(self, data, opener, url, ticktock, female=False):
        super().__init__()
        self.data = data
        self.data['isOver'] = 0
        self.data['isTyfx'] = 0
        self.url = url
        self.female = female
        if self.female:
            self.name = '抢课姬'
        self.ticktock = ticktock
        self.opener = opener

    def start(self):
        while 1:
            try:
                request = urllib.request.Request(self.url + Config.class_api)
                data = urllib.parse.urlencode(self.data).encode('utf8')
                response = self.opener.get_opener().open(request, data).read()
                result = json.loads(response.decode('utf8'))
                second = time.strftime('%H:%M:%S', time.localtime(time.time()))
                if result['code'] == 0 or result['info'] == 'OK':
                    if self.female:
                        print(self.name + '--->' + second + " : " + '主人，主人，我抢到了！~\(≧▽≦)/~')
                    else:
                        print(self.name + '--->' + second + " : " + str(result['info']))
                    break
                else:
                    if self.female:
                        if result['info'] == '课程学生人数限制，已选满！':
                            print(self.name + '--->' + second + " : " + '主人，人家抢不到嘛！╮(╯▽╰)╭')
                        else:
                            print(self.name + '--->' + second + " : " + str(result['info']))
                    else:
                        print(self.name + '--->' + second + " : " + str(result['info']))
                    time.sleep(self.ticktock)
            except Exception as e:
                second = time.strftime('%H:%M:%S', time.localtime(time.time()))
                if self.female:
                    print(self.name + '--->' + second + " : " + '主人，人家出错了！╯﹏╰')
                else:
                    print(self.name + '--->' + second + " : " + str(e))
                time.sleep(self.ticktock)
            except KeyboardInterrupt:
                break
