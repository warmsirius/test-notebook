# 导入psutil
import psutil
import time

delay = 3
print("CPU使用率     内存使用率      根目录使用率")
while True:
    time.sleep(delay)
    print(str(psutil.cpu_percent()) + "%         " + str(psutil.virtual_memory().percent) + "%         " +
          str(psutil.disk_usage("/").percent) + "%")


# CPU使用率     内存使用率      根目录使用率
# 28.2%         68.4%         13.0%
# 15.6%         67.9%         13.0%