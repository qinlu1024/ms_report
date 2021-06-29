

CREATE TABLE T_loan_s01_msd AS
SELECT
	`l`.`LOAN_NO` AS `LOAN_NO`,
	`l`.`PARTNER_NO` AS `PARTNER_NO`,
	`l`.`BHDT_BCH_CDE` AS `BHDT_BCH_CDE`,
	L.LOAN_CLASS,
	concat(
		'BSBK99',
		LEFT (`l`.`BHDT_BCH_CDE`, 2)
	) AS `FH`,
	cast(`l`.`DIS_AMT` AS FLOAT) AS `DIS_AMT`,
	`l`.`LOAN_TYP` AS `LOAN_TYP`,
	cast(`l`.`INT_START_DT` AS date) AS `INT_START_DT`,
	cast(`l`.`LAST_DUE_DT` AS date) AS `LAST_DUE_DT`,
	cast(`l`.`ACTV_DT` AS date) AS `ACTV_DT`,
	(
		CASE trim(`l`.`LAST_SETL_DT`)
		WHEN '00010101' THEN
			NULL
		ELSE
			cast(`l`.`LAST_SETL_DT` AS date)
		END
	) AS `LAST_SETL_DT`,
	`l`.`SETL_FLG` AS `SETL_FLG`,
	`l`.`LOAN_SEC_TYP` AS `LOAN_SEC_TYP`,
	`l`.`REPAY_FRQ` AS `REPAY_FRQ`,
	`l`.`REP_CATE` AS `REP_CATE`,
	(
		CASE trim(`l`.`EXCU_RATE`)
		WHEN '' THEN
			NULL
		ELSE
			cast(
				trim(`l`.`EXCU_RATE`) AS FLOAT
			)
		END
	) AS `EXCU_RATE`,
	`l`.`BASE_AMT` AS `BASE_AMT`,
	`l`.`RES_AMT` AS `RES_AMT`,
	`l`.`I_OVER_AMT` AS `I_OVER_AMT`,
	`l`.`O_OVER_AMT` AS `O_OVER_AMT`,
	`l`.`I_IOA_AMT` AS `I_IOA_AMT`,
	`l`.`O_IOA_AMT` AS `O_IOA_AMT`,
	`l`.`PINT_AMT` AS `PINT_AMT`,
	(`l`.`FKQX` + 0) AS `FKQX`,
	(
		CASE trim(`l`.`YKQX`)
		WHEN '' THEN
			NULL
		ELSE
			cast(trim(`l`.`YKQX`) AS FLOAT)
		END
	) AS `YKQX`
FROM
	`loan_info` `l`
WHERE 1 = 1
 AND L.PRODUCT_TYP = '个人消费类贷款'
 AND L.LOAN_TYP LIKE '马上贷%'
