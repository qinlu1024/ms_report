import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 数据库配置：
# 用户名
db_user = 'root'
# 密码
db_password = '123456'
# IP地址
db_host = '127.0.0.1'
# 端口号
db_port = 3306
# 数据库
db_name = 'regular_monitoring'
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)

# 报表基础参数
p_stat_dt = "\'2020-12-31\'"
p_curr_cd = "\'HRMB\'"
p_peroid = 'M'
p_org = "\'BSBK9919\'"
org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}

# 业务状况 SQL
sql_ywzk = "SELECT Y.GL_ACCT, Y.GL_ACCT_NAME, Y.GL_ACCT_LEVEL,	Y.CURR_CD, Y.PERIOD, Y.ORG_NUM,	" \
         " Y.LAST_D_BAL, Y.LAST_C_BAL ,Y.DR_AMT, Y.CR_AMT, Y.DR_BAL, Y.CR_BAL " \
         " FROM V_YWZK_TMP Y WHERE 1 = 1 " \
         "AND Y.ORG_NUM IN (SELECT O.ORG_NUM FROM T09_REPORT_ORG O WHERE O.ORG_LEVEL = '2' AND O.ORG_TYPE='YW') " \
         "AND Y.STAT_DT = DATE("+p_stat_dt + ") AND Y.CURR_CD = "+p_curr_cd + " AND Y.PERIOD = \'M\' "

# 通过pandas读取 机构数据
data_ywzk = pd.read_sql(sql_ywzk, engine).rename(columns={'GL_ACCT': '科目号', 'GL_ACCT_NAME': '科目名称',
                                                          'GL_ACCT_LEVEL': '科目级别', 'CURR_CD': '币种',
                                                          'PERIOD': '粒度',
                                                          'LAST_D_BAL': '1期初借方余额', 'LAST_C_BAL': '2期初贷方余额',
                                                          'DR_AMT': '3借方发生额', 'CR_AMT': '4贷方发生额',
                                                          'DR_BAL': '5借方余额', 'CR_BAL': '6贷方余额'})

# print('----------------------------业务状况输出 ----------------------------------------------------------------')
pd_exp_ywzk = pd.pivot_table(data_ywzk, values=['1期初借方余额', '2期初贷方余额', '3借方发生额', '4贷方发生额',
                                                '5借方余额', '6贷方余额'],
                             index=['科目号', '科目名称', '科目级别', '币种', '粒度'], columns='ORG_NUM',
                             aggfunc=np.sum, fill_value=0)
pd_exp_ywzk = pd_exp_ywzk.rename(columns=org_dict)

# print('---------------------------- excel输出 ----------------------------------------------------------------')
with pd.ExcelWriter('D:\\test\\业务状况各-ALL_('+p_stat_dt[1:11]+').xlsx') as writer:
    pd_exp_ywzk.to_excel(writer, sheet_name='业务状况表', na_rep='0', float_format="%.2f")
