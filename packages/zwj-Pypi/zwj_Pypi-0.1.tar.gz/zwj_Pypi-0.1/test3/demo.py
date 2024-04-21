from textaugment import *

# 实例化CodeRefactor类
t = CodeRefactor()

# 读取文件内容
filename = r"D:\pythonProject1\test1\test.py"
with open(filename, 'r', encoding='ISO-8859-1') as open_file:
    code = open_file.read()

# 调用rename_local_variable方法并输出结果
refactored_code = t.rename_local_variable(code)
print(refactored_code)
