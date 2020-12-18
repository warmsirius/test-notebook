"""
1.实现登录基本功能，输出响应，脚本正确
2.多用户随机登录: doLogin方法构造随机数据
3.on_start: 类似于构造方法，可以将公共数据放在这个函数里，每个用户只运行1次
4.添加检查点(断言):
    - 在请求方法中设置catch_response参数为True
    - 调用success 和 failure方法标注成功或失败
"""
from random import randint

from locust import HttpUser, TaskSet, task


# 任务类
class TestLogin(TaskSet):
    # 任务开始前自动执行
    def on_start(self):
        self.loginData = [{"username": "zhangsan", "password": "zs123"}, {"username": "lisi", "password": "ls123"},
                          {"username": "wangwu", "password": "ww123"}, {"username": "zhaoliu", "password": "zl123"}]

    @task
    def doLogin(self):
        # 请求正文接收字典

        # 1000以内的随机数，对用户长度3进行取余
        randInx = randint(1, 1000) % len(self.loginData)

        # 发送POST请求
        response = self.client.post("url", data=self.loginData[randInx], catch_response=True)

        # 断言
        if "login-pass" in response.text:
            response.success()
        else:
            response.failure("cannot login")


class WebSite(HttpUser):
    tasks = [TestLogin]
    min_wait = 1000
    max_wait = 2000


if __name__ == "__main__":
    import os

    os.system("locust -f 5.TestLogin.py --host=http://0.0.0.0:8089")
