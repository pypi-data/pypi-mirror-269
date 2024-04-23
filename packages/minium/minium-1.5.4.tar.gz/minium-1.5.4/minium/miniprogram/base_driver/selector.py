'''
Author: yopofeng yopofeng@tencent.com
Date: 2024-01-30 12:31:32
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2024-03-06 17:58:57
FilePath: /py-minium/minium/miniprogram/base_driver/selector.py
Description: minium元素选择器类, 记录元素选择的信息
'''
from enum import Enum, auto
from typing import Dict, List
from cssselect import GenericTranslator

class _Selector(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        name = name.lower()
        if name.startswith("selector"):
            return name[9:]
        return name
    CSS = auto()
    XPATH = auto()

    TEXT = auto()
    START_TEXT = auto()
    CONTAINS_TEXT = auto()
    VAL = auto()
    INDEX = auto()
    CHILD = auto()
    PARENT = auto()
    TEXT_REGEX = auto()
    CLASS_REGEX = auto()
    NODE_ID = auto()

class SelectorMetaClass(type):
    def __new__(mcs, cls_name, bases, attr_dict):
        def set_value(selector):
            def wrapper(self: 'Selector', v):
                if v is not None:
                    self._selector[selector] = v
            return wrapper
        def get_value(selector):
            def wrapper(self: 'Selector'):
                return self._selector.get(selector, None)
            return wrapper
        for _selector in _Selector.__members__.values():
            if _selector.value not in attr_dict:
                attr_dict[_selector.value] = property(
                    get_value(_selector),
                    set_value(_selector),
                )
        return type.__new__(mcs, cls_name, bases, attr_dict)

class Selector(object, metaclass=SelectorMetaClass):
    _selector: Dict[_Selector, str or int or _Selector]
    def __init__(self, _: 'Selector'=None, **selector) -> None:
        self._selector = {_Selector.INDEX: -1}
        if _:
            for k, v in _._selector.items():
                self._selector[k] = v
            return
        self._selector.update({getattr(_Selector, k.upper()): v for k, v in selector.items() if v is not None})

    @property
    def need_filter(self):
        return not (self.text is None and self.val is None and self.contains_text is None)

    def check_selector(self):
        selector = self.css
        is_xpath = False
        if not selector:
            selector = self.xpath = self._selector.get(_Selector.XPATH, "//*")
            is_xpath = True
        elif selector.startswith("/"):
            self.xpath = selector
            self.css = ""
            is_xpath = True
        return selector, is_xpath

    def to_selector(self):
        if not self._selector:
            raise ValueError('No element found')
        selector, is_xpath = self.check_selector()
        if is_xpath:
            if _Selector.TEXT in self._selector:
                selector += '[normalize-space(text())="%s"]' % self._selector[_Selector.TEXT]
            elif _Selector.CONTAINS_TEXT in self._selector:
                selector += '[contains(text(), "%s")]' % self._selector[_Selector.CONTAINS_TEXT]
            elif _Selector.VAL in self._selector:
                selector += '[@value="%s"]' % self._selector[_Selector.VAL]
            return selector if selector.startswith("/") else ("//" + selector)
        else:
            return selector
    
    def full_selector(self) -> str:
        def has_xpath(selector: Selector):
            if selector.xpath:
                return True
            if selector.parent:
                return has_xpath(selector.parent)
            return False
        if has_xpath(self):  # 统一转化成xpath
            return self.to_xpath()
        if self.parent:
            return self.parent.full_selector() + (" >>> " if self.parent.node_id else " ") + self.css
        return self.css

    def to_xpath(self):
        """转成xpath表达"""
        if self.xpath:
            xpath = self.to_selector()
            if self.parent and (xpath.startswith("//") or xpath.startswith("/descendant-or-self::")):
                return self.parent.to_xpath() + xpath
            return xpath
        else:
            try:
                selector = Selector(self)
            except TypeError:
                print(self)
                raise
            selector.xpath = GenericTranslator().css_to_xpath(self.css, "//")
            selector.css = ""
            if self.parent:
                return self.parent.to_xpath() + selector.to_selector()
            return selector.to_selector()

    def __repr__(self):
        return f"{{{', '.join([f'{k.value}: {v}'for (k, v) in self._selector.items()])}}}"

        

    
