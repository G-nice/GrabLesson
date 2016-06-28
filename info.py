def enter():
    print('-----------------------------')
    print('欢迎来到抢课脚本（@CQUPT）v1.0')
    print('        作者：PinkD           ')
    print('-----------------------------')
    print('')


def input_cookie():
    print('1.手动输入cookie（可使用WireShark抓包）')
    print('2.登录自动获取cookie（需要安装库）')
    return input('请选择（默认2）：')


def choose_site():
    print('选择选课地址:')
    print('1.http://xk1.cqupt.edu.cn/')
    print('2.http://xk2.cqupt.edu.cn/')
    print('3.http://xk4.cqupt.edu.cn/(不稳定，不推荐使用)')
    return input('请输入选课地址（默认2）：')


def get_site():
    choice = choose_site()
    if choice != '1' and choice != '2' and choice != '4':
        print('使用默认')
        choice = '2'
    else:
        print('使用选课' + choice)
    return choice


def choose_type():
    print('选择类型:')
    print('1.专业课程')
    print('2.人文任选')
    print('e.退出程序')
    return input('请选择（默认2）：')


def print_all(data): # TODO debug
    print('所有课程信息:')
    position = 0
    for tmp in data:
        print('序号:' + str(position))
        print(tmp['kcmc'])  # 课程名
        print(tmp['teacher'])  # 老师
        print(tmp['sdPrint'])  # 时间
        print(tmp['kchType'])  # 课程类型
        print(tmp['nj'])  # 年级
        print(tmp['kclb'])  # 课程类别
        print(tmp['xf'])  # 学分
        print('\n')
        position += 1
    print('tips:输入-1返回上一层\n')
    while 1:
        try:
            tmp = input('请输入你要抢的课的序号:')
            tmp = int(tmp)
            if -2 < tmp < data.__len__():
                break
        except ValueError:
            pass
    return tmp
