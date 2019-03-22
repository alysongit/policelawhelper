# @Time    : 2018/10/23 12:54
# @Author  : Niyoufa
import os
import re
import time
import logging
from collections import Iterable

console_logger = logging.getLogger("console")

def read_lines(path):
    lines = [line for line in iter_line(path)]
    return lines

# 迭代生成文件非空行
def iter_line(path):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line

# 迭代文本生成文非空行
def iter_text_line(text):
    lines = re.split(r"[\n]", text)
    for line in lines:
        line = line.strip()
        if line:
            yield line

# 迭代处理指定目录下的文件
def iter_file(path, file_func=None):

    for parent_path, dirnames, filenames in os.walk(path, topdown=True, onerror=lambda e:print(e)):

        for filename in sorted(filenames, reverse=False):
            file_path = os.path.join(parent_path, filename)
            if callable(file_func):
                gen = file_func(file_path)
                if isinstance(gen, Iterable):
                    for item in gen:
                        yield item
            else:
                yield file_path

def time_consume(func):
    """函数耗时计算"""

    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        time_useage = time.time() - start_time
        console_logger.info("{func_name}:{time_useage}ms".format(
            func_name = func.__name__,
            time_useage  = int(time_useage*1000)
        ))
        return result
    return wrapper

if __name__ == "__main__":
    path = "/home/admin/niyoufa/project/xcases_parse/media/xcases/index_data_dulp/cpws_20180718"
    iter_obj = iter_file(path)
    for obj in iter_obj:
        print(obj)