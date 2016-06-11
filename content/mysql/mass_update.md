title: 批量修改sql
slug: mass_update
date: 2016-04-22

## Mysql 批量修改view 的definer
```
select concat("alter DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW ",
	TABLE_SCHEMA,
	".",
	TABLE_NAME,
	" as "
	,VIEW_DEFINITION,
	";") 
 from information_schema.VIEWS 
where table_schema <> 'sys'  ORDER BY 1 ASC;
```

## 批量修改table engine
```
SELECT  CONCAT('ALTER TABLE `',table_schema,
	'`.`',
	table_name,
	'` ENGINE=InnoDB;') AS sql_statements
 FROM    information_schema.tables AS tb
WHERE   `ENGINE` = 'MyISAM'
  AND     `TABLE_TYPE` = 'BASE TABLE'
  and table_schema not in ('mysql','')
ORDER BY table_name DESC;
```

