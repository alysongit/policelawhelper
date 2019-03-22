# @Time    : 2018/10/31 17:02
# @Author  : Niyoufa

class Filter:
    """过滤器父类"""
    patterns = []

    @property
    def pattern(self):
        return "|".join(self.patterns)