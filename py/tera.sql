SELECT
    'I' (CHAR(01))
  , '|' (CHAR(01))
  , BS_CD (CHAR(02))
  , '|' (CHAR(01))
  , ACTN_AC_C (FORMAT ‘—-9’) (CHAR(04)) —활동계좌수
  , '|' (CHAR(01))
  , MDTT_ISA_PYMT_ PSBL_F (CHAR(01)) —여부
  , '|' (CHAR(01))
  , T1. STD_DT (FORMAT 'YYYYMMDD') (CHAR(08)) --기준일
  , '|' (CHAR(01))
  , T1. IS_NO (CHAR(12))-- 펀드종목코드(KSD종목코드)
  , '|' (CHAR(01))
  , T1.OPN_PRC (DECIMAL(15,2))
  , '|' (CHAR(01))
  , T1.ORDR_Q (DECIMAL(10))
  , '|' (CHAR(01))
  , T1.ORDR_DT (DATE)
  , '|' (CHAR(01))
  , '03' AS STR03 (CHAR(02))
FROM T1
INNER JOIN
    (
        SELECT
            BS_CD
          , A
          , B
          , C
        FROM CC) T2
ON
    T1.BS_CD = T2.BS_CD;