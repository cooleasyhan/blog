title: 请求使用sql
slug: oracle_request
date: 2016-09-07


# 查询ap 批次号, ar 
```

SELECT Listagg(Ap_Batch_Id, ',') Within GROUP(ORDER BY 1)
  FROM (SELECT v.Argument_Text, TRIM(Regexp_Substr(Argument_Text, '[^,]+', 1, 2)) Ap_Batch_Id
          FROM Fnd_Conc_Req_Summary_v v
         WHERE v.Requestor = 'YIHAN'
           AND v.Request_Date > SYSDATE - 1
           AND v.User_Concurrent_Program_Name = 'Invoice Validation');

SELECT Listagg(Ar_Interface_Run_Id, ',') Within GROUP(ORDER BY 1)
  FROM (SELECT TRIM(Regexp_Substr(Argument_Text, '[^,]+', 1, 1)) Ar_Interface_Run_Id
          FROM Fnd_Conc_Req_Summary_v v
         WHERE v.Requestor = 'YIHAN'
           AND v.Request_Date > SYSDATE - 1
           AND v.Program = 'S_AR211_TRX (CUX:Interface Process)'
           AND v.Argument_Text LIKE '%DATA_IMPORT%');

```