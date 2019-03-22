# @Time    : 2018/10/23 12:58
# @Author  : Niyoufa

class Handler:
    """
    处理程序父类
    """
    def callback(self, prefix, name, *args, **kwargs):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args, **kwargs)

    def sub(self, name, **kwargs):
        def substitution(match):
            result = self.callback('sub_', name, match, **kwargs)
            if result is None: result = match.group(0)
            return result
        return substitution