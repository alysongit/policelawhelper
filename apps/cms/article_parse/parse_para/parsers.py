# @Time    : 2019/1/8 14:51
# @Author  : Niyoufa
from cms.article_parse.engine.parse import Parser
from cms.article_parse.engine.collections import Params
from cms.article_parse.engine.util import iter_text_line
from cms.article_parse.parse_para.rules import *

from lxml.html import etree


class ArticleParaParser(Parser):
    """解析"""

    def __init__(self):
        super(ArticleParaParser, self).__init__()

        self.addRule(H2Rule())


    def parse(self, text, **kwargs):
        """
        对每一行匹配每一个规则
        :param text: 
        :param kwargs: 
        :return: 
        """
        params = Params({"content": "", "curr_para": None})
        data_list = []

        lines = [line for line in iter_text_line(text)]
        for line in lines:
            params["block"] = line
            for rule in self.rules:
                matched = rule.condition(params, **kwargs)
                if matched:
                    if params["curr_para"]:
                        data_list.append(params["curr_para"])
                    para_html = etree.HTML(matched.groupdict()["para"])
                    new_para = dict(
                        para_name = "".join(para_html.xpath("//text()")),
                        content = ""
                    )
                    params["curr_para"] = new_para
                    break
                else:
                    if params["curr_para"]:
                        params["curr_para"]["content"] += "\n" + line
                    else:
                        params["curr_para"] = dict(
                            para_name = None,
                            content = line
                        )

        data_list.append(params["curr_para"])
        return data_list