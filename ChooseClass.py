import json
import os
import urllib.request
import urllib.parse
import time


def choose_class(data):
    while 1:
        try:
            url = 'http://xk2.cqupt.edu.cn/xkPost.php'
            req = urllib.request.Request(url)
            data = urllib.parse.urlencode(data)
            data = data.encode(encoding='UTF8')
            cookie = 'PHPSESSID=vgr1lrh7f2lp13ob9hcgb1v8h1'
            req.add_unredirected_header("Cookie", cookie)
            response = urllib.request.urlopen(req, data)
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

    os.system("pause")
