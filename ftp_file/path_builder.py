import os
import shutil
import pandas as pd

os_separator = '\\'
base_dir = 'D:\\test'
target_dir = 'ftp'
path_file_name = 'directory.xlsx'
copy_path = 'file_list'

path_sheet_name = 'dep'
target_sheet_name = 'file_hier'

target_file_path = os_separator.join([base_dir, target_dir])
target_file_list = os_separator.join([base_dir, path_file_name])
target_copy_path = os_separator.join([base_dir, copy_path])

init_condition_1 = os.path.exists(target_file_path)
init_condition_2 = os.path.exists(target_file_list)
init_condition_3 = os.path.exists(target_copy_path)

if not init_condition_1:
    os.makedirs(target_file_path)
    print('Base path: ' + target_file_path + ' build ok !')
else:
    print('Base path: ' + target_file_path + ' is all set !')


if not init_condition_2:
    print('path_file: ' + target_file_list + ' not found !')
else:
    print('path_file: ' + target_file_list + ' is all set !')


if not init_condition_3:
    os.makedirs(target_copy_path)
    print('target_copy_path: ' + target_copy_path + ' not found !')
else:
    print('target_copy_path: ' + target_copy_path + ' is all set !')


target_df = pd.read_excel(target_file_list, sheet_name=target_sheet_name, dtype={'file_type': str})
# print(target_pd)
target_df['path_file'] = target_copy_path + os_separator + target_df['file_type']
# print(target_df)

for row in target_df.index:
    if not os.path.exists(target_df.iloc[row, 2]):
        os.makedirs(target_df.iloc[row, 2])
        print('file_list: ' + target_df.iloc[row, 2] + ' creationComplete !')
    else:
        print('file_list: ' + target_df.iloc[row, 2] + ' already exists !')


path_df = pd.read_excel(target_file_list, sheet_name=path_sheet_name, dtype={'l1': str, 'l2': str})
path_df['path'] = target_file_path + os_separator + path_df['l1'] + os_separator + path_df['l2']
# print(path_df)

for row1 in path_df.index:

    if not os.path.exists(path_df.iloc[row1, 3]):
        os.makedirs(path_df.iloc[row1, 3])
        print('path_file: ' + path_df.iloc[row1, 3] + ' creationComplete !')
    else:
        print('path_file: ' + path_df.iloc[row1, 3] + ' already exists !')

    if os.path.exists(target_copy_path):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(target_copy_path):
            for d in dirs:
                if not os.path.exists(os_separator.join([path_df.iloc[row1, 3], d])):
                    os.makedirs(os_separator.join([path_df.iloc[row1, 3], d]))


print('Completed the task !')
