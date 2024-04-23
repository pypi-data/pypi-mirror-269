'''
Description: 日志类
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-03 23:30:55
LastEditTime: 2024-01-04 10:44:51
'''
import os
import logging
import platform

_IS_WINDOWS = platform.system() == "Windows"

_LoggingType = {"error": logging.ERROR,
                "warn": logging.WARNING,
                "warning": logging.WARNING,
                "info": logging.INFO,
                "debug": logging.DEBUG}

def is_folder_exists(path):
    if os.path.exists(path) and not os.path.isfile(path):
        return True
    return False

def mkdir(path):
    split_char = "\\" if _IS_WINDOWS else "/"
    path_list = path.split(split_char)
    cur_path = path_list[0]
    if not is_folder_exists(cur_path):
        os.mkdir(path)
    for i in range(1, len(path_list)):
        cur_path += split_char + path_list[i]
        if not is_folder_exists(cur_path):
            os.mkdir(path)

def get_logger(main_account, log_path="logs"):
    mkdir(log_path)
    logger = logging.getLogger(main_account)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f'{log_path}/{main_account}.log')
        formatter = logging.Formatter('%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


class Logger:
    def __init__(self, log_path, log_dir="logs", dev_mode="debug"):
        self.logger = get_logger(log_path, log_dir)
        assert dev_mode in ("debug", "release")
        self.dev_mode = dev_mode

    def log(self, msg="", mode="info", **kwargs):
        if self.dev_mode == "debug":
            level = _LoggingType.get(mode, logging.INFO)
            if msg != "":
                self.logger.log(level=level, msg=msg)
            for key, value in kwargs.items():
                self.log(mode=mode, msg=f"{key} = {value}")

    def __call__(self, msg="", mode="info", **kwargs):
        return self.log(msg, mode, **kwargs)
