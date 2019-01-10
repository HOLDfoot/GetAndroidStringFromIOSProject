# encoding: utf-8
from __future__ import print_function
import lxml
from lxml import etree, objectify
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def add_element(file_name, key, value):
    value = value.encode(sys.getdefaultencoding()).decode("utf-8")
    tree = lxml.etree.parse(file_name)
    res = tree.xpath('/resources')[0]
    children = res.getchildren()
    count = len(children)
    E = objectify.ElementMaker(annotate=False)
    element = E.string(value)
    element.set("name", key)
    element.tail = "\n"
    res.insert(count, element)

    tree.write(file_name, encoding='utf-8')

if __name__ == "__main__":
    print("__main__ test.py")
    file_name = "values-de/strings.xml"
    ss = "选择结果"
    add_element(file_name, "choose", ss)
