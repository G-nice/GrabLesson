import info
import LoginUtils
import ChooseClassUtils

info.enter()

url = LoginUtils.choose_site(info.get_site())
if info.input_cookie() is '1':
    cookie = LoginUtils.create_cookie()
    content = input('请输入Cookie:PHPSESSID=')
    handler = LoginUtils.CookieHandler('PHPSESSID=' + content, cookie)
    opener = LoginUtils.Opener(cookie, handler)

else:
    opener = LoginUtils.LoginUtil(url).login()

chooseClassUtils = ChooseClassUtils.Classes(url, opener)
while 1:
    try:
        chooseClassUtils.select().start()
    except AttributeError:
        pass
