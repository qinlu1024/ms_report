import xlrd
import pandas as pd
import os

base_dir = "D:\\Excel\\"
file_name = "员工与授信客户资金往来.xls"
main_sheet = "QUERY_FOR_员工与授信客户"
type_col = "分行"
# main_key = "预警编号"
file_path = base_dir + file_name
new_dir = file_name.split('.')[0]
# print(new_dir)

data = xlrd.open_workbook(file_path)
# table = data.sheet_by_name(main_sheet)
sheet_names = data.sheet_names()
# print(sheet_names)
# 读主Sheet 分类字段
# , converters={"我行账户": str, "柜员": str,	"复核柜员": str, "对方账号": str, "流水号": str}
main_df = pd.read_excel(file_path, sheet_name=main_sheet, converters={"我行账户": str, "柜员": str, "员工号": str,
                                                                      "授信客户账号": str, "流水号": str})
print(main_df.info())
type_fh = main_df[type_col].drop_duplicates()
# 机构分类
list_fh = type_fh.to_list()
print(list_fh)
# 循环开始 按机构 创建 文件夹 预警结果
for org in list_fh:

    df_m = main_df.loc[main_df[type_col] == org]

    init_condition_1 = os.path.exists(base_dir + new_dir + "\\")
    if not init_condition_1:
        os.makedirs(base_dir + new_dir + "\\")

    df_m.to_excel(base_dir + new_dir + "\\" + org + ".xls", sheet_name=sheet_names[0], index=False)
