# @Time    : 2018/10/23 12:55
# @Author  : Niyoufa

class Rule:
    """
    规则父类
    """

    def condition(self, params=None, **kwargs):
        """
        判断是否符合规则
        """
        pass

    def action(self, params=None, **kwargs):
        """
        动作
        """
        pass