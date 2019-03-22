# @Time    : 2019/1/8 14:30
# @Author  : Niyoufa
import re
from cms.article_parse.engine.rule import Rule


class H2Rule(Rule):
    """<h2>标记的段落"""
    name = "h2"

    regex = r"<h2[^>]*?>(?P<para>.*?)</h2>"
    compile_regex = re.compile(regex, flags=re.M)

    def condition(self, params=None, **kwargs):
        matched = self.compile_regex.search(params.block)
        return matched