import json
import threading
import urllib.request
import urllib.parse

import time


def get_classes():
    #TODO
    return []


class Classes:
    def __init__(self, url, cookie):
        self.classes = get_classes()
        self.url = url
        self.cookie = cookie

    def choose_class(self, cid):
        target = self.classes[cid]
        threading._start_new_thread(self.choose_class, target)


class ChooseClass(threading.Thread):
    def __init__(self, data, url):
        super().__init__()
        self.data = data
        self.url = url

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
                    print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "--->" + str(result))
                    break
                else:
                    print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "--->" + str(result))
                    time.sleep(3)
            except:
                print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "--->" + "ERROR!")
