# encoding=UTF-8
from __future__ import print_function
import re

# grep命令输出的行的正则表达式, 会有文件名和行号
# 第一部分以分号结束, 第二部分变量的命名规范(数字字母下划线), 第三部分被引号包含的含有'='的字符串, 第四部分从开始到不包含'"'的位置, 第五部分以'"'开始到最后的位置
grep_pattern = re.compile(r'(.*:"?)([a-zA-Z0-9_]{0,100})(".*=.*")([^"]*)(".*)', re.I) # 匹配字符串test_line1
# 文件中一行的正则表达式
line_pattern = re.compile(r'(\s*"?)([a-zA-Z0-9_]{0,100})(".*=.*")([^"]*)(".*)', re.I)



def get_key_value(line):
    match_obj = line_pattern.match(line)
    key = None
    value = None
    if match_obj:
        key = match_obj.group(2)
        value = match_obj.group(4)
    tuple_map = (key, value)
    return tuple_map



if __name__ == '__main__':
    test_line1 = 'Localized.strings:10:"ASLocalizedLanguage_Tarot_QuickDivine_String"="选择";  // 选择'
    test_line = '"ASLocalizedLanguage_Tarot_QuickDivine_String"="选择";  // 选择'
    #test_line = '"ASLocalizedLanguage_Tarot_MessageCenter_Reportdescribe_String" = "请输入举报具体原因，例如吐字不清、声音太小、凑时长、答非所问、语速太快等";  //请输入举报具体原因，例如吐字不清、声音太小、凑时长、答非所问、语速太快等'
    # matchObj = re.match(r'(.*:"?)([a-zA-Z0-9_]{0,100})(".*=.*")([^"]{0,100})(".*)', test_line, re.I) # 被key和value切割了5部分
    matchObj = line_pattern.match(test_line)
    if matchObj:
        print("matchObj.group():", matchObj.group())
        print("matchObj.group(1):", matchObj.group(1))
        print("matchObj.group(2):", matchObj.group(2))
        print("matchObj.group(3):", matchObj.group(3))
        print("matchObj.group(4):", matchObj.group(4))
        print("matchObj.group(5):", matchObj.group(5))
    else:
        print("No match!!")

    key = get_key_value(line=test_line)
    print("key=",key)

'''

matchObj.group(): Localized.strings:10:"ASLocalizedLanguage_Tarot_QuickDivine_String"="快速占い";  // 快速占卜
matchObj.group(1): Localized.strings:10:"
matchObj.group(2): ASLocalizedLanguage_Tarot_QuickDivine_String
matchObj.group(3): "="
matchObj.group(4): 快速占い
matchObj.group(5): ";  // 快速占卜

'''
