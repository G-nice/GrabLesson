import json
import urllib.request
import urllib.parse
import http.cookiejar

from PIL import Image
import io

import Config
import info


def create_cookie():
    cookie = http.cookiejar.MozillaCookieJar()
    try:
        cookie.load(Config.cookie_file_name)
    except FileNotFoundError:
        pass
    return cookie


def choose_site(site=2):
    return 'http://xk' + str(site) + '.cqupt.edu.cn/'


def get_site():
    choice = info.choose_site()
    if choice != '1' and choice != '2' and choice != '4':
        print('使用默认')
        choice = '2'
    else:
        print('使用选课' + choice)
    return choice


def get_available_classes(cookie):
    opener = get_opener(cookie)
    opener.open(Config.show_class_api)
    # TODO
    pass


def get_opener(cookie):
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))


class LoginUtils:
    def __init__(self):
        self.cookie = create_cookie()
        self.url = choose_site(get_site())

    def show_picture(self):
        opener = get_opener(self.cookie)
        file = opener.open(self.url + Config.picture_api)
        tmp = io.BytesIO(file.read())
        img = Image.open(tmp)
        img.show()
        return self.cookie

    def get_validation_code(self):
        self.show_picture()
        return input('请输入验证码:')

    def login(self):
        print('登录：')
        while 1:
            username = input('用户名：')
            password = input('密码：')
            validation = self.get_validation_code()
            data = {'id': username, 'psw': password, 'vCode': validation}
            print(data)
            data = urllib.parse.urlencode(data)
            data = data.encode('utf8')
            print(self.cookie)
            opener = get_opener(self.cookie)
            response = opener.open(self.url + Config.login_api, data)
            response = response.read()
            result = json.loads(response.decode('UTF8'))
            if result['code'] == 0 or result['info'] == 'OK':
                self.cookie.save(Config.cookie_file_name)
                return self.cookie
            print(result['info'])
            print(self.cookie)
