import json
import urllib.request
import urllib.parse
import http.cookiejar

from PIL import Image
import io

import Config


def create_cookie():
    cookie = http.cookiejar.MozillaCookieJar(Config.cookie_file_name)
    try:
        cookie.load(ignore_discard=True, ignore_expires=True)
    except FileNotFoundError:
        pass
    return cookie


def choose_site(site=2):
    return 'http://xk' + str(site) + '.cqupt.edu.cn/'


class CookieHandler(urllib.request.BaseHandler):
    def __init__(self, cookie, cookiejar):
        self.cookie = cookie
        self.cookiejar = cookiejar

    def http_request(self, request):
        if not request.has_header('Cookie'):
            request.add_unredirected_header('Cookie', self.cookie)
            request.add_header('Cookie', self.cookie)
        else:
            cookie = request.get_header('Cookie')
            request.add_unredirected_header('Cookie', cookie + '; ' + cookie)
        self.cookiejar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self.cookiejar.extract_cookies(response, request)
        self.cookiejar.save(ignore_discard=True, ignore_expires=True)
        return response


class Opener:
    def __init__(self, cookie, cookie_handler=None):
        if cookie_handler:
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie), cookie_handler)
        else:
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

    def get_opener(self):
        return self.opener


class LoginUtil:
    def __init__(self, url, cookie=None):
        self.url = url
        self.cookie = create_cookie()
        self.opener = Opener(self.cookie)

    def show_picture(self):
        response = self.opener.get_opener().open(self.url + Config.picture_api)
        tmp = io.BytesIO(response.read())
        img = Image.open(tmp)
        img.show()
        return self.cookie

    def get_validation_code(self):
        self.show_picture()
        return input('请输入验证码:')

    def login(self):
        if self.cookie.cookies.__len__() > 0:
            print(self.cookie)
            return self.opener
        print('登录')
        while 1:
            username = input('用户名：')
            password = input('密码：')
            validation = self.get_validation_code()
            data = {'id': username, 'psw': password, 'vCode': validation}
            print(data)
            data = urllib.parse.urlencode(data)
            data = data.encode('utf8')
            response = self.opener.get_opener().open(self.url + Config.login_api, data).read()
            result = json.loads(response.decode('UTF8'))
            if result['code'] == 0 or result['info'] == 'OK':
                print('登陆成功')
                self.cookie.save(ignore_discard=True, ignore_expires=True)
                return self.opener
            print(result['info'])
