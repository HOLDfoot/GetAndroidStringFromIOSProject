# encoding: utf-8

import lxml
from lxml import etree, objectify
from classes import PairModel
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def get_elements(file_name):
    print("get_elements: " + file_name)
    tree = lxml.etree.parse(file_name)
    res = tree.xpath('/resources')[0]  # 获取bndbox元素的内容
    elements_list = []
    for ss in res.getchildren():  # 便利bndbox元素下的子元素
        element_name = ss.get("name")
        element_text = ss.text
        if element_name: # 注释会有text
            elements_list.append(PairModel(element_name, element_text))
    return elements_list


if __name__ == "__main__":
    print("__main__")
    file_name = "multi-languages/values-zh/strings.xml"
    elements_list = get_elements(file_name)
    print(elements_list[0])
