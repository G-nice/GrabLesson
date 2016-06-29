import info
import LoginUtils
import ChooseClassUtils

info.enter()

url = LoginUtils.choose_site(info.get_site())
if info.input_cookie() is '1':
    cookie = LoginUtils.create_cookie()
    cookie.add_cookie_header(LoginUtils.get_opener1(url, input('请输入Cookie:')))
else:
    cookie = LoginUtils.LoginUtil(url).login()
chooseClassUtils = ChooseClassUtils.Classes(url, cookie)
count = 0
ticktock = 1
while 1:
    try:
        chooseClassUtils.select(ticktock, count).start()
        count += 1
    except AttributeError:
        pass
