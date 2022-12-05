# gunicorn.conf.py
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = '0.0.0.0:8881'  #绑定ip和端口号

backlog = 512 #监听队列
timeout = 30  # 响应耗时（单位为秒）

worker_class = 'gevent' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = multiprocessing.cpu_count() * 2 + 1    #进程数
threads = 2 #指定每个进程开启的线程数

#loglevel = 'debug' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
#access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置

"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
#accesslog = "./logs/access.log"      #访问日志文件
#errorlog = "./logs/error.log"        #错误日志文件
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,

    "root": {"level": "INFO", "handlers": ["error_file", "access_file"]},
    "loggers": {
        "gunicorn.error": {
            "level": "ERROR",  # 打日志的等级可以换的，下面的同理
            "handlers": ["error_file"],  # 对应下面的键
            "propagate": 1,
            "qualname": "gunicorn.error"
        },

        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "gunicorn.access"
        }
    },
    "handlers": {
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 50,  # 打日志的大小，我这种写法是1个G
            "backupCount": 1,  # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            "formatter": "generic",  # 对应下面的键
            # "mode": "w+",
            "filename": "./logs/error.log"  # 打日志的路径
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 50,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "./logs/access.log",
        }
    },
    "formatters": {
        "generic": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",  # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
            "class": "logging.Formatter"
        },
        "access": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
            "class": "logging.Formatter"
        }
    }
}

