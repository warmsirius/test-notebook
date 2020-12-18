# 导入locust相关的类，成员
from locust import TaskSet, task, HttpUser


# 任务类
class TaskIndex(TaskSet):
    @task
    def getIndex(self):
        # 如果是https协议，verify=True
        # 如果是http协议，verify=False
        self.client.get("https://www.baidu.com", verify=True)


class WebSite(HttpUser):
    tasks = [TaskIndex]
    min_wait = 1000
    max_wait = 2000


if __name__ == "__main__":
    import os

    os.system("locust -f user.py --host=http://0.0.0.0:8089")
