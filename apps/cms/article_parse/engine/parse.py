# @Time    : 2018/10/23 12:53
# @Author  : Niyoufa
import re
import copy
import logging
from .rule import Rule

console_logger = logging.getLogger("console")


class Parser:
    """
    解析器父类
    """
    def __init__(self, handler=None):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        """
        添加规则
        """
        self.rules.append(rule)

    def removeRule(self, name):
        """
        删除规则
        """
        for index, rule in enumerate(self.rules):
            if hasattr(rule, "name") and rule.name == name:
                del self.rules[index]
                return index

    def replaceRule(self, repl_rule):
        """
        替换规则
        """
        if isinstance(repl_rule, Rule) and hasattr(repl_rule, "name"):
            for index, rule in enumerate(self.rules):
                if rule.name == repl_rule.name:
                    self.rules[index] = repl_rule
                    return index

    def insertRule(self, index, rule):
        """插入规则"""
        if isinstance(rule, Rule):
            self.rules.insert(index, rule)
        else:
            raise ValueError("rule must be instance of Rule")

    def addFilter(self, f):
        """
        添加过滤器
        """
        def filter(block, handler, **kwargs):
            return re.sub(f.pattern, handler.sub(f.name, **kwargs), block)
        self.filters.append(filter)

    def extract(self, doc_iter_or_text, *args, **kwargs):
        """
        抽取
        :param doc_iter_or_text: 样本迭代器
        :param args: 
        :param kwargs: 
        :return: 
        """
        pass

    def parse(self, doc_iter_or_text, *args, **kwargs):
        """
        解析
        :param doc_iter_or_text: 样本迭代器
        :param args: 
        :param kwargs: 
        :return: 
        """
        if isinstance(doc_iter_or_text, str):
            for rule in self.rules:
                if isinstance(rule, list):
                    for sub_rule in rule:
                        matched = sub_rule.condition(doc_iter_or_text)
                        if matched:
                            result = sub_rule.action(doc_iter_or_text)
                            return result
                else:
                    matched = rule.condition(doc_iter_or_text)
                    if matched:
                        result = rule.action(doc_iter_or_text)
                        return result
        else:
            result = []
            for doc in doc_iter_or_text:
                result.append(self.parse(doc, *args, **kwargs))
            return result

    def save(self, *args, **kwargs):
        vals = args[0]
        bulk_update_request = self.model.get_bulk_update_request(vals, **kwargs)
        self.bulk_update_requests.append(bulk_update_request)

        if self.parse_count % self.bulk_size == 0:
            bulk_update_requests = copy.deepcopy(self.bulk_update_requests)
            self.bulk_update_requests = []
            self.threadpool.submit(self.save_to_mongo, bulk_update_requests)

    def save_to_mongo(self, bulk_update_requests):
        if bulk_update_requests:
            self.model.bulk_update(bulk_update_requests)