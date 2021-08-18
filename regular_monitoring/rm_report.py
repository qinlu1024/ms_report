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
db_name1 = 'regular_monitoring'
db_name2 = 'loan'
engine1 = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name1}', echo=True)
engine2 = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name2}', echo=True)
# 报表基础参数
p_stat_dt = "\'2021-07-31\'"
p_curr_cd = "\'HRMB\'"
p_peroid = "\'M\'"


org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}

acct_dict = {'PB_D': '对公定期', 'PB_H': '对公活期', 'PV_D': '对私定期', 'PV_H': '对私活期'}
cust_dict = {'GS': '对公', 'GR': '对私'}
open_chnl = {'1001': '柜面', '1105': '本行自助终端', '1400': '其他外围', '1401': '信用卡'}

sql_org_1 = " SELECT ORG_NUM,ORG_NAME FROM T09_REPORT_ORG WHERE ORG_TYPE=\'YW\' "
# 通过pandas读取 机构数据
data_org_1 = pd.read_sql(sql_org_1, engine1)

for index, row in data_org_1.iterrows():
    p_org = "\'" + row['ORG_NUM'] + "\'"

    sql_fz_1 = " SELECT X.INDIC_KEY, X.INDIC_NAME, X.STAT_DT, ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
               " WHERE 1=1  AND X.INDIC_TYPE = \'1\' " \
               " AND X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
               " AND X.ORG_NUM = " + p_org + " " \
               "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = " + p_peroid + " " \
               "ORDER BY STAT_DT,INDIC_KEY "

    sql_fz_2 = "SELECT X.INDIC_KEY, X.INDIC_NAME, X.STAT_DT, ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
               "WHERE 1=1  AND X.INDIC_TYPE = \'2\' " \
               "AND X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
               "AND X.ORG_NUM = " + p_org + " " \
               "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = " + p_peroid + " " \
               "ORDER BY STAT_DT,INDIC_KEY "

    sql_fz_3 = "SELECT X.DISPLAY_SEQ AS INDIC_KEY, X.INDIC_NAME, X.STAT_DT, X.IND_VAL " \
               "FROM V_09_RM_REPORT_SHOP X " \
               "WHERE X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
               "AND X.ORG_NUM = " + p_org + " " \
               "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = " + p_peroid + " " \
               "ORDER BY STAT_DT,INDIC_KEY "
    # 业务状况 SQL
    sql_ywzk = " SELECT Y.STAT_DT, Y.GL_ACCT, Y.GL_ACCT_NAME, Y.GL_ACCT_LEVEL,	Y.CURR_CD,  " \
               " Y.PERIOD, Y.ORG_NUM, Y.DR_AMT, Y.CR_AMT, Y.DR_BAL, Y.CR_BAL " \
               " FROM V_YWZK_TMP Y WHERE 1 = 1 " \
               " AND Y.STAT_DT <= DATE(" + p_stat_dt + ") AND Y.CURR_CD = " + p_curr_cd + " " \
               " AND Y.PERIOD = " + p_peroid + " " \
               " AND Y.ORG_NUM = " + p_org

    sql_loan_prod = " SELECT L.ACTV_MON, L.DATA_DATE, L.BHDT_BCH_CDE, L.PRODUCT_TYP, L.LOAN_TYP, " \
                    " L.NBR, L.DIS_AMT, L.BASE_AMT, L.PINT_AMT, L.I_OVER_AMT, L.I_IOA_AMT, L.O_OVER_AMT, " \
                    " L.O_IOA_AMT , L.NBR_P, L.RES_AMT_P FROM V_REPORT_LOAN L " \
                    " WHERE 1=1 AND L.BHDT_BCH_CDE = " + p_org

    sql_acct_prod = " SELECT A.ETL_DATE, A.FH, A.TP, A.CURR_CD, A.PRODUCT_ID, A.FIN_PROD_TYP_CD, " \
                    " A.PRODUCT_NAME, A.CUST_NBR, A.ACCT_NBR, A.AMT_VAL FROM V_REPORT_ACCT A " \
                    " WHERE 1=1 " \
                    " AND A.FH = " + p_org

    sql_cust_new = " SELECT C.TYPE, C.FH, C.OPN_ACT_CNL, C.OPEN_MTH, C.NBR FROM V_REPORT_CUST C " \
                   " WHERE 1=1 " \
                   " AND C.FH = " + p_org

    data_fz_1 = pd.read_sql(sql_fz_1, engine1).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})
    data_fz_2 = pd.read_sql(sql_fz_2, engine1).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})
    data_fz_3 = pd.read_sql(sql_fz_3, engine1).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})
    data_ywzk = pd.read_sql(sql_ywzk, engine1).rename(columns={'STAT_DT': '日期', 'GL_ACCT': '科目号',
                                                               'GL_ACCT_NAME': '科目名称',
                                                               'GL_ACCT_LEVEL': '科目级别', 'CURR_CD': '币种',
                                                               'PERIOD': '粒度',
                                                               'DR_AMT': '1借方发生额', 'CR_AMT': '2贷方发生额',
                                                               'DR_BAL': '3借方余额', 'CR_BAL': '4贷方余额'})
    data_loan_prod = pd.read_sql(sql_loan_prod, engine2).rename(columns={'ACTV_MON': '放款月份', 'DATA_DATE': '观察月份',
                                                                         'BHDT_BCH_CDE': '机构',
                                                                         'PRODUCT_TYP': '产品类型', 'LOAN_TYP': '贷款类型',
                                                                         'NBR': '放款笔数', 'DIS_AMT': '放款金额',
                                                                         'BASE_AMT': '贷款余额', 'PINT_AMT': '利息收入',
                                                                         'I_OVER_AMT': '表内逾期', 'I_IOA_AMT': '表内罚息',
                                                                         'O_OVER_AMT': '表外逾期', 'O_IOA_AMT': '表外罚息',
                                                                         'NBR_P': '逾期笔数', 'RES_AMT_P': '逾期本金'})

    data_acct_prod = pd.read_sql(sql_acct_prod, engine2).rename(columns={'ETL_DATE': '观察月份', 'FH': '机构',
                                                                         'TP': '分类', 'CURR_CD': '币种',
                                                                         'PRODUCT_ID': '产品ID',
                                                                         'FIN_PROD_TYP_CD': '产品类型',
                                                                         'PRODUCT_NAME': '产品名称',
                                                                         'CUST_NBR': '客户数', 'ACCT_NBR': '账户数',
                                                                         'AMT_VAL': '余额'})
    data_acct_prod['分类'].replace(acct_dict, inplace=True)

    data_cust_new = pd.read_sql(sql_cust_new, engine2).rename(columns={'TYPE': '客户类型', 'FH': '机构',
                                                                       'OPN_ACT_CNL': '开户渠道', 'OPEN_MTH': '开户月份',
                                                                       'NBR': '新开数量'})
    data_cust_new['客户类型'].replace(cust_dict, inplace=True)
    data_cust_new['开户渠道'].replace(open_chnl, inplace=True)

    pd_exp_fz_1 = pd.pivot_table(data_fz_1, values='IND_VAL', index=['指标ID', '指标名称'], columns='STAT_DT',
                                 aggfunc=np.sum, fill_value=0)

    pd_exp_fz_2 = pd.pivot_table(data_fz_2, values='IND_VAL', index=['指标ID', '指标名称'], columns='STAT_DT',
                                 aggfunc=np.sum, fill_value=0)

    pd_exp_fz_3 = pd.pivot_table(data_fz_3, values='IND_VAL', index=['指标ID', '指标名称'], columns='STAT_DT',
                                 aggfunc=np.sum, fill_value=0)
    pd_exp_ywzk = pd.pivot_table(data_ywzk, values=['1借方发生额', '2贷方发生额', '3借方余额', '4贷方余额'],
                                 index=['科目号', '科目名称', '科目级别', '币种', '粒度'], columns='日期',
                                 aggfunc=np.sum, fill_value=0)
    pd_exp_ywzk = pd_exp_ywzk.rename(columns=org_dict)

    pd_loan_prod = pd.pivot_table(data_loan_prod, values=['贷款余额', '利息收入', '表内逾期', '表内罚息', '表外逾期', '表外罚息',
                                                          '逾期笔数', '逾期本金'],
                                  index=['放款月份', '产品类型', '贷款类型', '放款笔数', '放款金额'],
                                  columns='观察月份',
                                  aggfunc=np.sum, fill_value=0)

    pd_acct_prod = pd.pivot_table(data_acct_prod, values=['客户数', '账户数', '余额'],
                                  index=['分类', '币种', '产品ID', '产品类型', '产品名称'],
                                  columns='观察月份',
                                  aggfunc=np.sum, fill_value=0)

    pd_cust_new = pd.pivot_table(data_cust_new, values=['新开数量'],
                                 index=['客户类型', '开户渠道'],
                                 columns='开户月份',
                                 aggfunc=np.sum, fill_value=0)

    print('---------------------------- excel输出 ----------------------------------------------------------------')
    with pd.ExcelWriter(
            'D:\\test\\report\\' + row['ORG_NAME'] + '_' + p_stat_dt[1:11] + '_' + p_peroid + '.xlsx') \
            as writer:
        pd_exp_fz_3.to_excel(writer, sheet_name='衍生指标', na_rep='0', float_format="%.4f")
        pd_exp_fz_1.to_excel(writer, sheet_name='资产负债', na_rep='0', float_format="%.2f")
        pd_exp_fz_2.to_excel(writer, sheet_name='利润', na_rep='0', float_format="%.2f")
        pd_exp_ywzk.to_excel(writer, sheet_name='业务状况表', na_rep='0', float_format="%.2f")
        pd_loan_prod.to_excel(writer, sheet_name='贷款业务', na_rep='0', float_format="%.2f")
        pd_acct_prod.to_excel(writer, sheet_name='存款业务', na_rep='0', float_format="%.2f")
        pd_cust_new.to_excel(writer, sheet_name='客户新开', na_rep='0', float_format="%.2f")


