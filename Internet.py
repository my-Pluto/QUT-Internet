from urllib import request
import time
import json


class Vpn:
    def __init__(self, params):
        self.url = 'http://10.20.10.11/drcom/login'
        self.user = params.get('user')
        self.pwd = params.get('pwd')
        self.type = params.get('type')
        self.type_list = ['', '@cmcc', '@unicom', '@telecom']

    # 获取登录url
    def get_url(self):
        get_params = {
            'callback': 'dr' + str(int(time.time() * 1000)),
            'DDDDD': self.user + self.type_list[self.type],
            'upass': self.pwd,
            '0MKKey': '123456',
            'R1': '0',
            'R3': '0',
            'R6': '0',
            'para': '0',
            'v6ip': '0',
            '_': str(int(time.time() * 1000))
        }

        url = self.url + "?"
        keys = get_params.keys()

        i = 0
        for temp in keys:
            if i == 0:
                url = url + temp + "=" + get_params[temp]
                i = i + 1
            else:
                url = url + "&" + temp + "=" + get_params[temp]

        return url

    # 登录
    def login(self):

        url = self.get_url()
        # 登录并获取返回信息

        r = request.urlopen(url=url)
        r = r.read().decode("GBK")
        r = r.split('(')[1].split(')')[0]
        r = json.loads(r)

        # 检测登录情况
        if r['result'] is 1:
            # print("YES!")
            return True
        else:
            # print("NO!")
            return False


if __name__ == '__main__':
    user_info = {
        'user': '',  # 填写你的用户名
        'pwd': '',  # 填写你的登录密码
        'type': 0,  # 账号类型，0为校园网，1为移动，2为联通，3为电信，学校默认校园网
    }
    vpn = Vpn(user_info)
    flag = False
    code = 404
    while True:
        # 每5s检测一次是否连接互联网，如果没有连接，则登录网络
        try:
            code = 404
            response = request.urlopen("http://www.baidu.com")
            # print(time.time(), end=" ")
            # print(response.getcode())
            code = response.getcode()
        except:
            code = 404
            # print(code)
        if code != 200:
            flag = False
            while flag is False:
                try:
                    flag = vpn.login()
                except:
                    flag = False
                    time.sleep(5)
                    continue
                time.sleep(5)
        time.sleep(5)

