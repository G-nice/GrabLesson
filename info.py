def enter():
    print('-----------------------------')
    print('欢迎来到抢课脚本（@CQUPT）v1.0')
    print('        作者：PinkD           ')
    print('-----------------------------')
    print('')


def choose_site():
    print('1.http://xk1.cqupt.edu.cn/')
    print('2.http://xk2.cqupt.edu.cn/')
    print('3.http://xk4.cqupt.edu.cn/(不稳定，不推荐使用)')
    return input('请输入选课地址（默认2）：')


def choose_type():
    print('1.专业课程')
    print('2.人文任选')
    return input('请输入选课地址（默认2）：')