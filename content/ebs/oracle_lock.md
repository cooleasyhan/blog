title: oracle 锁
slug: oracle_lock
date: 2016-04-22


## oracle查询锁
```
SELECT Obj.Owner,
       Obj.Object_Id,
       Obj.Object_Name,
       Lo.Locked_Mode,
       s.Sid,
       s.Serial#,
       s.Username,
       s.Machine,
       s.Terminal,
       s.Program,
       s.Client_Identifier,
       s.Module,
       s.Action,
       s.Row_Wait_Obj#,
       s.Row_Wait_File#,
       s.Row_Wait_Block#,
       s.Row_Wait_Row#,
       CASE
         WHEN l.Request <> 0 THEN
          Dbms_Rowid.Rowid_Create(1,
                                  Row_Wait_Obj#,
                                  Row_Wait_File#,
                                  Row_Wait_Block#,
                                  Row_Wait_Row#)
         ELSE
          'no row id'
       END Row_Id,
       'select * from ' || Obj.Owner || '.' || Obj.Object_Name ||
       ' where rowid = ''' || CASE
         WHEN l.Request <> 0 THEN
          Dbms_Rowid.Rowid_Create(1,
                                  Row_Wait_Obj#,
                                  Row_Wait_File#,
                                  Row_Wait_Block#,
                                  Row_Wait_Row#)
         ELSE
          'no row id'
       END || '''' Select_Row_Sql,
       l.Type,
       Lt.Name,
       Lt.Description,
       Lt.Id1_Tag,
       l.Id1,
       Lt.Id2_Tag,
       l.Id2,
       Decode(l.Lmode,
              0,
              ' 0 - None ',
              1,
              ' 1 - NULL(NULL) ',
              2,
              ' 2 - ROW - s(Ss) ',
              3,
              ' 3 - ROW - x(Sx) ',
              4,
              ' 4 - SHARE(s) ',
              5,
              ' 5 - s / ROW - x(Ssx) ',
              6,
              ' 6 - EXCLUSIVE(x) ') Lock_Mode,
       Decode(l.Request,
              0,
              ' 0 - None ',
              1,
              ' 1 - NULL(NULL) ',
              2,
              ' 2 - ROW - s(Ss) ',
              3,
              ' 3 - ROW - x(Sx) ',
              4,
              ' 4 - SHARE(s) ',
              5,
              ' 5 - s / ROW - x(Ssx) ',
              6,
              ' 6 - EXCLUSIVE(x) ') Request,
       l.Block,
       Decode(l.Block,
              0,
              ' 0 - THE LOCK IS NOT Blocking ANY Other Processes ',
              1,
              ' 1 - THE LOCK IS Blocking Other Processes ',
              2,
              ' 2 - THE LOCK IS NOT Blocking ANY Blocked Processes ON THE LOCAL Node,
       But It May OR May NOT Be Blocking Processes ON Remote Nodes. ')
  FROM V$lock          l,
       V$lock_Type     Lt,
       V$locked_Object Lo,
       All_Objects     Obj,
       V$session       s
 WHERE 1 = 1
   AND l.Type = Lt.Type
   AND Lo.Session_Id = s.Sid
   AND Lo.Object_Id = Obj.Object_Id
   AND l.Sid = s.Sid
   AND Obj.Object_Name = 'xxxxxx'
   AND (l.Block <> 0 OR l.Request <> 0);

```

