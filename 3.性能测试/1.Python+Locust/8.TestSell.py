import json
from random import randint

from locust import HttpUser, TaskSet, task

"""
1.实现查看商品请求
2.实现查看会员请求
3.将前面2个请求的响应所需要的数据取回来
4.构造销售出库的请求
"""

"""
问题:
1.关于cookie: locust中自动帮我们管理了cookie
2.self.client会加到结果统计中去，如果不想加，可用原生的 `requests` 库发送请求
"""


# 任务类
class TestSell(TaskSet):
    # 任务开始前自动执行
    def on_start(self):
        self.loginData = [{"username": "zhangsan", "password": "zs123"}, {"username": "lisi", "password": "ls123"},
                          {"username": "wangwu", "password": "ww123"}, {"username": "zhaoliu", "password": "zl123"}]
        self.barCodes = [1001, 1002, 1003]
        self.costumers = ["18683668666", "17911112222", "18055556666", "19011112222"]
        # 此时登录是前提，而不是任务
        self.doLogin()

    def randomValue(self, myList):
        """随机返回列表中的某个函数"""
        randIndex = randint(1, 10000) % len(myList)
        return myList[randIndex]

    def getGoods(self):
        """返回商品价格"""
        # http://localhost:8080/WoniuSales/sell/barcode
        # barcode=1001
        body = {"barcode": self.randomValue(self.barCodes)}
        response = self.client.post("/WoniuSales/sell/barcode", body)
        # 解析响应的JSON数据，后续正常使用列表或字典操作数据
        newText = json.load(response.text)
        return newText[0]["unitprice"]

    def getCustomerInfo(self):
        """获取会员信息"""
        # http://localhost:8080/WoniuSales/customer/query
        # customerphone=18683668666
        body = {"customerphone": self.randomValue(self.costumers)}
        response = self.client.post("/WoniuSales/customer/query", body)
        newText = json.load(response.text)
        return newText[0]["credittotal"], newText[0]["customerphone"]

    @task
    def doSell(self):
        """销售出库"""
        # http://localhost:8080/WoniuSales/sell/summary
        # customerphone=18683668666     第2个请求
        # paymethod=现金                 默认
        # totalprice=186                第1个请求 uniteprice*0.78
        # creditratio=2.0               默认
        # creditsum=372                 totalprice * creditratio
        # tickettype=无                 默认
        # ticketsum=0                   默认
        # oldcredit=6730                第2个请求credittotal
        price = int(self.getGoods() * 0.78)
        credittotal, phone = self.getCustomerInfo()
        body = {"customerphone": phone, "paymethod": "现金", "totalprice": price, "creditratio": 2.0,
                "creditsum": price * 2, "tickettype": "无", "ticketsum": 0, "oldcredit": credittotal}
        response = self.client.post("/WoniuSales/sell/summary", body, catch_response=True)

        # 断言
        if response.text.isdigit():
            response.success()
        else:
            response.failure("Cannot Sell")

    def doLogin(self):
        # 发送POST请求
        response = self.client.post("url", data=self.randomValue(self.loginData), catch_response=True)

        # 断言
        if "login-pass" in response.text:
            response.success()
        else:
            response.failure("cannot login")


class WebSite(HttpUser):
    tasks = [TestSell]
    min_wait = 1000
    max_wait = 2000


if __name__ == "__main__":
    import os

    os.system("locust -f 8.TestSell.py --host=http://0.0.0.0:8089")
