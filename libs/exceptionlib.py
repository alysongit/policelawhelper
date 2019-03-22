#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 13:05
# @Author  : Niyoufa
# @Site    : 
# @File    : test.py.py
# @Software: PyCharm
import traceback
from pyArango.theExceptions import ValidationError, CreationError, InvalidDocument, SchemaViolation
from libs import handlerlib

# 程序异常
class ProgramException(Exception):
    def __init__(self, error_info):
        self.err = (500, error_info)

# 用户输入异常
class CustomException(Exception):

    def __init__(self,error_info):
        self.err = (400, error_info)

# token异常
class TokenException(Exception):

    def __init__(self,error_info):
        self.err = (401, error_info)

# 名称错误
class NameError(Exception):
    def __init__(self, error_info):
        self.err = (400, error_info)

def hander_response_result(response_result):
    code = (response_result or {}).get("code")
    msg = (response_result or {}).get("msg") or response_result
    if code != 200:
        import traceback
        print(traceback.format_exc())
        raise CustomException(msg)

# 异常处理装饰器 同步
def exception_handler(func):
    def handler(self,*args,**kwargs):
        try:
            return func(self,*args,**kwargs)
        except CustomException as msg:
            code = msg.err[0]
            info = msg.err[1]
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except TokenException as msg:
            code = msg.err[0]
            info = msg.err[1]
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except ValueError as msg:
            result = handlerlib.reset_response_data(msg)
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except NameError as msg:
            code = msg.err[0]
            info = msg.err[1]
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except CreationError as err:
            code = 400
            err_info = err.args[0]
            if err_info.startswith("unique constraint violated"):
                info = "对象已存在"
            else:
                info = err_info
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except ValidationError as err:
            code = 400
            info = "表单验证失败：%s"%err.args[0]
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except SchemaViolation as err:
            code = 400
            info = "表结构不支持：%s"%err.args[0]
            result = handlerlib.reset_response_data(str(info), code=int(code))
            response = handlerlib.JSONResponse(result)
            response.status_code = 200
            return response
        except:
            info = traceback.format_exc()
            result = handlerlib.reset_response_data(str(info))
            response = handlerlib.JSONResponse(result)
            response.status_code = 500
            return response
    return handler

# 抛出异常测试函数
def raiseTest():
    # 抛出异常
    raise CustomException("用户输入异常")

# 主函数
if __name__ == '__main__':
    try:
        raiseTest()
    except CustomException as msg:
       print(msg.err)
