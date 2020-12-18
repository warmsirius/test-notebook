# 导入locust相关的类，成员
from locust import TaskSet, task, HttpUser


# 任务类
class TaskIndex(TaskSet):
    @task
    def getIndex(self):
        # 如果是https协议，verify=True
        # 如果是http协议，verify=False
        response = self.client.get("https://www.baidu.com", verify=True, catch_response=True)
        if response.status_code == 200:
            response.success()
        else:
            response.failure("百度网页获取错误")


class WebSite(HttpUser):
    tasks = [TaskIndex]
    min_wait = 1000
    max_wait = 2000


if __name__ == "__main__":
    import os

    os.system("locust -f 5.locustDemo.py --host=http://0.0.0.0:8089")
