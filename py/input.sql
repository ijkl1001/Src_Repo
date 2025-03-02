SELECT
ACTN_AC_C          --활동계좌수
, '|', MDTT_ISA_PYMT_ PSBL_F        --여부
, '|', T1. STD_DT    --기준일
, '|', T1. IS_NO    -- 펀드종목코드(KSD종목코드)
, '|', T1.OPN_PRC
, '|', T1.ORDR_Q
, '|', T1.ORDR_DT
, '|', '03'
   AS  STR03
, '|'
, T2.colC
FROM T1
INNER JOIN (SELECT BS_CD, colA, colB, colC FROM CC) T2 
      ON T1.BS_CD = T2.BS_CD
;