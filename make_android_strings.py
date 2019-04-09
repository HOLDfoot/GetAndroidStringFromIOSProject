# encoding=UTF-8
# functions: 在非AVOID_DIR目录下的文件CONTAINS_FILE中查找内容
from __future__ import print_function
from regex import get_key_value
from insert_xml import add_element
from classes import PairModel
from read_xml import get_elements
import os
import sys
import shutil

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

cwd = os.getcwd()

DEBUG = True

android_input_folder = "multi-languages/android"
origin_android_folder = "multi-languages/values-zh"
android_file_name = "strings.xml"

ios_input_folder = "multi-languages/ios"
origin_ios_folder = "zh-Hans.lproj"
ios_file_name = "Localized.strings"
ios_folder_suffix = ".lproj"

# ios和android不同语言对应的不同文件夹
ios_lang_dir = []
android_lang_dir = []


def main():
    android_search_list = get_android_search_list()
    for pair in android_search_list:
        pair_model = pair
        find_android_value(pair_model)

# 从iOS的中文翻译中找到iOS对应的key, 正常则调用find_ios_value_by_key, 可能iOS中没有Android的翻译, 也可能有多个Android的翻译
def find_android_value(pair_model):
    android_search_key = pair_model.key
    android_search_value = pair_model.value
    key_array = find_ios_key(android_search_value) #找到key
    log("find value: %s" % android_search_value)
    log("find result: %s" % str(key_array))
    if key_array is None or len(key_array) == 0:
        log_file("Not find value", "value = %s\n" % android_search_value)
        # 此时没有找到其他语言的翻译, 应该用默认的中文翻译占位置
        # 将android默认的中文意思写到ios_lang_dir对应的android文件中
        log("write chinese android_key: " + android_search_value)
        for i in range(0, len(android_lang_dir)):
            output_lang_file = os.path.join(cwd, android_input_folder, android_lang_dir[i], android_file_name)
            if not os.path.exists(output_lang_file):
                log("Not exists file error: " + output_lang_file)
                return
            # 读取文件, 然后插入
            add_element(output_lang_file, android_search_key, android_search_value)
    elif len(key_array) > 1:
        key = "key = %s\n" % android_search_value
        keysLen = "keysLen = %d\n" % len(key_array)
        body = key + keysLen
        log_file("Many keys", body)
        for key in key_array:
            find_ios_value_by_key(android_search_key, key)
    else: # 正常只有一个key
        find_ios_value_by_key(android_search_key, key_array[0])

def get_android_search_list():
    # 获取指定文件的所有资源的key和value
    file_name = os.path.join(cwd, origin_android_folder, android_file_name)
    return get_elements(file_name)

# 在多个国家语言中找value, 返回pair, 特定文件中key是唯一的
def find_ios_value(ios_file_path, ios_key):
    ios_origin_file = open(ios_file_path, 'r+')
    lines = ios_origin_file.readlines()
    if lines:
        for line in lines:
            pair = get_key_value(line)
            if pair[0] == ios_key:
                return pair
    tuple_map = (None, None)
    return tuple_map

# 在特定中文文件中找key
def find_ios_key(ios_value):
    ios_file_path = os.path.join(cwd, ios_input_folder, origin_ios_folder, ios_file_name)
    key_array = []
    ios_origin_file = open(ios_file_path, 'r+')
    lines = ios_origin_file.readlines()
    if lines:
        for line in lines:
            pair = get_key_value(line)
            if pair[1] == ios_value:
                key_array.append(pair[0])
    return key_array

# 找到所有的ios key, 如果有的没有则打印完整log, 不向文件中添加
def find_ios_value_by_key(android_key, ios_key):
    global ios_lang_dir
    global android_lang_dir
    ios_lang_value = []
    for ios_lang_dir_child in ios_lang_dir:
        target_lang_file = os.path.join(cwd, ios_input_folder, ios_lang_dir_child, ios_file_name)
        tuple_map = find_ios_value(target_lang_file, ios_key)
        if not tuple_map[1]:
            key_body = "ios_key = %s\n" % ios_key
            file_body = "target_lang_file = %s\n" % target_lang_file
            exists_body = "exists_lang = %s\n" % ios_lang_value
            # 出现这种情况是iOS代码格式的问题, 找到相应的key调整格式, 重新调用脚本
            log_file("Key not exists in file, please format the ios resources", key_body + file_body + exists_body)
            log(exists_body)
            return
        else:
            ios_lang_value.append(tuple_map[1])
    # 将ios_lang_value写到ios_lang_dir对应的android文件中
    log("write android_key: " + android_key)
    for i in range(0, len(android_lang_dir)):
        output_lang_file = os.path.join(cwd, android_input_folder, android_lang_dir[i], android_file_name)
        if not os.path.exists(output_lang_file):
            log("Not exists file error: " + output_lang_file)
            return
        # 读取文件, 然后插入
        add_element(output_lang_file, android_key, ios_lang_value[i])


def init_lang_dir():
    global ios_lang_dir
    global android_lang_dir
    ios_input_folder_path = os.path.join(cwd, ios_input_folder)
    files = os.listdir(ios_input_folder_path)
    for folder_name in files:
        if not folder_name.__contains__(ios_folder_suffix):
            log("folder_name format error: " + folder_name)
            continue
        part_names = folder_name.split(".")
        if len(part_names) != 2:
            log("folder_name split format error: " + folder_name)
            continue
        if not part_names[0] == "zh-Hans":
            ios_lang_dir.append(folder_name)
        # 获取Android文件夹的名字
        if not part_names[0] == "zh-Hans":
            android_folder_name = "values-" + part_names[0]
            android_lang_dir.append(android_folder_name) # 2个list中顺序对应着


def log_file(title, body):
    log_path = os.path.join(cwd, "log.txt")
    fp = open(log_path, "a+")
    title_line = "==========%s==========\n" % title
    fp.writelines(title_line)
    fp.writelines(body)
    fp.close()

def log(msg):
    if DEBUG:
        print(msg)

def delete_log():
    log_path = os.path.join(cwd, "log.txt")
    if os.path.exists(log_path):
        os.remove(log_path)

def create_android_lang_dir():
    android_input_folder_path = os.path.join(cwd, android_input_folder)
    if os.path.exists(android_input_folder_path):
        lang_folder_list = os.listdir(android_input_folder_path)
        for lang_folder in lang_folder_list:
            shutil.rmtree(os.path.join(android_input_folder_path, lang_folder))
    # 根据android_lang_dir, 初始化android的多语言目录
    for lang_folder in android_lang_dir:
        android_folder = os.path.join(android_input_folder_path, lang_folder)
        os.mkdir(android_folder)
        fp = open(os.path.join(android_folder, android_file_name), "w+")
        fp.write("<resources>\n</resources>")

def test():
    #查找单一资源的翻译, 并组织成android的xml文件
    pair = PairModel("reported", "已举报")
    find_android_value(pair)

if __name__ == '__main__':
    delete_log()
    init_lang_dir()
    create_android_lang_dir()
    main()