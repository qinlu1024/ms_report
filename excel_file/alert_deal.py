import xlrd
import pandas as pd
import os

base_dir = "D:\\Excel\\"
file_name = "员工手机号签约非员工手机银行.xls"
main_sheet = "预警"
type_col = "经办行所属管辖行"
main_key = "预警编号"
file_path = base_dir + file_name
new_dir = file_name.split('.')[0]
# print(new_dir)

data = xlrd.open_workbook(file_path)
# table = data.sheet_by_name(main_sheet)
sheet_names = data.sheet_names()
# print(sheet_names)
# 读主Sheet 分类字段
main_df = pd.read_excel(file_path, sheet_name=main_sheet)
type_fh = main_df[type_col].drop_duplicates()
# 机构分类
list_fh = type_fh.to_list()

# 循环开始 按机构 创建 文件夹 预警结果
for org in list_fh:
    print(org+" begin:")
    df_m = main_df.loc[main_df[type_col] == org]
    list_alert_keys = df_m[main_key].drop_duplicates().to_list()
    init_condition_1 = os.path.exists(base_dir + new_dir + "\\")
    if not init_condition_1:
        os.makedirs(base_dir + new_dir + "\\")

    with pd.ExcelWriter(base_dir + new_dir + "\\" + org + ".xls") as writer:
        for sheet_i in sheet_names:
            df_i = pd.read_excel(file_path, sheet_name=sheet_i)
            df_df = df_i[df_i[main_key].isin(list_alert_keys)]
            df_df.to_excel(writer, sheet_name=sheet_i)
            print(org + " " + sheet_i + "ok!")

    print(org + " finish:")
