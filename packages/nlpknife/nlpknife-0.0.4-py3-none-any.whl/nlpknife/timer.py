'''
Description: 程序运行时间
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 10:45:32
LastEditTime: 2024-01-04 14:40:28
'''
import time

def run_time(func):
    def inner(*args, **kwargs):
        timestamp = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - timestamp
        runtimes = str(round(duration*1000,3)) + "ms"
        result["runtimes"] = runtimes
        return result
    return inner        
