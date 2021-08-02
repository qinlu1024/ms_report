import os
import pandas as pd
import random
import string
from pypinyin import pinyin, lazy_pinyin, Style
import openpyxl

# 基础参数
os_separator = '\\'
base_dir = 'D:\\test'
target_dir = 'ftp'
path_file_name = 'directory.xlsx'

user_name = 'user'

target_file_list = os_separator.join([base_dir, path_file_name])
# path_df = pd.read_excel(target_file_list, sheet_name=user_name)
wb = openpyxl.load_workbook(target_file_list)
# print(path_df)

sheet = wb['user']
col = sheet['D']

for i in col:
    py_tmp = lazy_pinyin(i.value)
    str_tmp = ''

    for l in py_tmp:
        str_tmp = str_tmp + l[0]

    print(str_tmp)


