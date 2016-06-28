import info
import LoginUtils
import ChooseClassUtils

info.enter()
logUtils = LoginUtils.LoginUtils()
cookie = logUtils.login()
url = logUtils.url
chooseClassUtils = ChooseClassUtils.Classes(url, cookie)
count = 0
ticktock = 1
while 1:
    try:
        chooseClassUtils.select(ticktock, count).start()
        count += 1
    except AttributeError:
        pass
