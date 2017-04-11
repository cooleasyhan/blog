title: 代码dependence
slug: oracle_dependence
date: 2016-09-07


# 收集dependence信息
```plsql
-- Created on 2016/9/7 by YIHAN 
DECLARE
  -- Local variables here
  i INTEGER;
BEGIN
  -- Test statements here
  DELETE Cux_Yh_Dependencies;
  INSERT INTO Cux_Yh_Dependencies
    SELECT *
      FROM Dba_Dependencies d
     WHERE d.Name IN
           (SELECT Upper(Substr(e.Execution_File_Name, 1, Instr(e.Execution_File_Name, '.', -1) - 1))
              FROM Fnd_Executables_Vl e
             WHERE e.Execution_Method_Code = 'I'
               AND e.Executable_Id IN (SELECT Vl.Executable_Id
                                         FROM Fnd_Request_Groups         g,
                                              Fnd_Request_Group_Units    u,
                                              Fnd_Concurrent_Programs_Vl Vl,
                                              Fnd_Application            a
                                        WHERE g.Request_Group_Name = 'QIHU_AR_ACCOUNT_REPORTS'
                                          AND g.Request_Group_Id = u.Request_Group_Id
                                          AND u.Request_Unit_Id = Vl.Concurrent_Program_Id
                                          AND u.Request_Unit_Type = 'P'
                                          AND Vl.User_Concurrent_Program_Name LIKE 'CUX%'
                                          AND Vl.Enabled_Flag = 'Y'
                                          AND Vl.Application_Id = a.Application_Id
                                       
                                       )
            UNION
            
            SELECT DISTINCT Upper(Substr(Req.Exec_Program, 1, Instr(Req.Exec_Program, '.', -1) - 1))
              FROM Cux_Unify_Import_Prf_Req Req, Cux_Unify_Import_Profile p
             WHERE p.Interface_Profile_Id = Req.Interface_Profile_Id
               AND p.Interface_Key IN
                   (SELECT REPLACE(TRIM(Substr(f.Parameters, Instr(f.Parameters, '"', 1))), '"', '')
                      FROM Fnd_Menus_Vl m, Fnd_Menu_Entries_Vl e, Fnd_Form_Functions_Vl f
                     WHERE Menu_Name IN ('CUX_RECE_IMP', 'CUX_REC_IMP')
                       AND m.Menu_Id = e.Menu_Id
                       AND f.Function_Id = e.Function_Id
                       AND Form_Id IS NOT NULL
                       AND PARAMETERS LIKE 'INTERFACE_KEY%'))
       AND d.Referenced_Name LIKE 'CUX%';

  FOR i IN 1 .. 10 LOOP
  
    INSERT INTO Cux_Yh_Dependencies
      SELECT *
        FROM Dba_Dependencies d
       WHERE d.Name IN (SELECT Cd.Referenced_Name FROM Cux_Yh_Dependencies Cd)
         AND d.Referenced_Name LIKE 'CUX%'
         AND NOT EXISTS
       (SELECT 1
                FROM Cux_Yh_Dependencies Cd1
               WHERE Cd1.Owner = d.Owner
                 AND Cd1.Name = d.Name
                 AND Cd1.Type = d.Type
                 AND Cd1.Referenced_Owner = d.Referenced_Owner
                 AND Cd1.Referenced_Name = d.Referenced_Name
                 AND Cd1.Referenced_Type = d.Referenced_Type
                 AND Nvl(Cd1.Referenced_Link_Name, 'dummy') = Nvl(d.Referenced_Link_Name, 'dummy')
                 AND Cd1.Dependency_Type = d.Dependency_Type);
  
  END LOOP;
END;

```


获取需要导入的数据
```plsql

SELECT 'REQUESTGROUP AR.QIHU_AR_ACCOUNT_REPORTS'
  FROM Dual
UNION ALL

SELECT 'MENU CUX.CUX_RECE_IMP'
  FROM Dual
UNION ALL
SELECT 'MENU CUX.CUX_REC_IMP'
  FROM Dual
UNION ALL
SELECT DISTINCT 'CUSTOMRULE FND.' || Function_Name
  FROM Fnd_Form_Custom_Rules
 WHERE Function_Name LIKE 'AR%'
   AND (Form_Name LIKE 'AR%' OR Form_Name LIKE 'RA%')
UNION ALL

--CUSTOMRULE
-- 有请求集还要加上
SELECT --g.Request_Group_Name,
--g.Application_Id,
--Vl.User_Concurrent_Program_Name,
 'REQUEST ' || a.Application_Short_Name || '.' || Vl.Concurrent_Program_Name Download_Str --,
--Vl.Application_Id
  FROM Fnd_Request_Groups         g,
       Fnd_Request_Group_Units    u,
       Fnd_Concurrent_Programs_Vl Vl,
       Fnd_Application            a
 WHERE g.Request_Group_Name = 'QIHU_AR_ACCOUNT_REPORTS'
   AND g.Request_Group_Id = u.Request_Group_Id
   AND u.Request_Unit_Id = Vl.Concurrent_Program_Id
   AND u.Request_Unit_Type = 'P'
   AND Vl.User_Concurrent_Program_Name LIKE 'CUX%'
   AND Vl.Enabled_Flag = 'Y'
   AND Vl.Application_Id = a.Application_Id
UNION ALL

SELECT Decode(TYPE, 'PACKAGE', 'PACKAGE_SPECIAL', 'PACKAGE BODY', 'PACKAGE_BODY', TYPE) || ' ' ||
       Owner || '.' || NAME
  FROM (SELECT DISTINCT Owner, NAME, TYPE
          FROM Cux_Yh_Dependencies d
        UNION
        SELECT DISTINCT d.Referenced_Owner, d.Referenced_Name, d.Referenced_Type
          FROM Cux_Yh_Dependencies d)
 WHERE TYPE != 'SYNONYM'
 
```