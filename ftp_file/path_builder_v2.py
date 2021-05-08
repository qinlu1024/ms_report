import os
import pandas as pd

# 基础参数
os_separator = '\\'
base_dir = 'D:\\test'
target_dir = 'ftp'
path_file_name = 'directory.xlsx'

path_sheet_name = 'dep'
target_sheet_name = 'file_hier'

target_file_list = os_separator.join([base_dir, path_file_name])

path_df = pd.read_excel(target_file_list, sheet_name=path_sheet_name)
path_df = path_df.astype(str)

dir_df = pd.read_excel(target_file_list, sheet_name=target_sheet_name)
dir_df = dir_df.astype(str)

target_df = pd.merge(path_df, dir_df, on='l1')
target_df = target_df.dropna()

for row in target_df.iterrows():
    pa = os_separator.join([base_dir, target_dir, row[1][1], row[1][2], row[1][3], row[1][4]])
    pa = pa.replace('\\nan', '')
    if not os.path.exists(pa):
        os.makedirs(pa)

