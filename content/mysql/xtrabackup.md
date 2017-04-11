title: xtrabackup 小结
date: 2015-12-13
slug: xtrabackup


## 安装  
官网下载相关rpm 包, 此处为 percona-xtrabackup-20-2.0.8-587.rhel6.x86_64.rpm， 其中5.1版本的mysql只能使用 2.0版本的xtrabackup
```
rpm -ivh xxx.rpm
```


## 单表备份
/usr/bin/innobackupex --defaults-file=/etc/my.cnf \
--slave-info --safe-slave-backup --no-lock \
--no-timestamp --user=xxx --password=xxxx \
--host=xxxx --port=3306 --stream=xbstream --compress \
--include='^database.table_name' /tmp \

## 单表恢复
1.安装qpress
wget http://www.quicklz.com/qpress-11-linux-x64.tar
2. xbstream解压
xbstream -x < xxx.xxx.xbstream -C ./test
3. qpress 解压
```
for f in `find ./ -iname "*\.qp"`; do qpress -dT2 $f  $(dirname $f) && rm -f $f; done
```
4. apply log
```
innobackupex --apply-log --export /home/yihan/test/
```
5. 拿掉tablespace 
```
ALTER TABLE xxx.xxx DISCARD TABLESPACE;
```
6. cp data 至 mysql data 目录
```
cp xxx.ibd /data/mysql/xxx/xxx.ibd
cp xxx.exp /data/mysql/xxx/xxx.exp
# 5.6 需要copy
cp xxx.cfg /data/mysql/xxx/xxx.cfg
```
7. chown to mysql
chown mysql:mysql /data/mysql/xxx/xxx.*
8 导入tablesapce 
```
ALTER TABLE xxx.xxx IMPORT TABLESPACE;
```


## 备份脚本
写了一个脚本，用于每周日全备，其他时候增量备份
```
#!/bin/bash
#author: yihan
#date: 2015-12-13
#
#
#创建用户
#mysql> CREATE USER 'bkpuser'@'localhost' IDENTIFIED BY 'xxx';
#mysql> GRANT RELOAD, LOCK TABLES, REPLICATION CLIENT, REPLICATION SLAVE,SUPER ON *.* TO 'bkpuser'@'localhost';
#mysql> GRANT RELOAD, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'bkpuser'@'localhost';
#mysql> FLUSH PRIVILEGES;


weekday=`date +%w`
port=3306
ip=localhost
base_dir=/data/bakup2
back_dir_name=mysql
back_dir=$base_dir/$back_dir_name
lsn_dir=$back_dir/lsn
file_cnf=/etc/my.cnf
user_name=bkpuser
password=xxx
ssh_tool="ssh xxx@1.1.1.1"


timestamp=`date +"%Y%m%d%H%M%S"`
Xtrabackup_log=$back_dir/Xtrabackup_log_$timestamp.out
shell_log=$base_dir/backup.log


function log
{
    t=`date +"%Y-%m-%d %H:%M:%S"`
    echo "[$t] $1" >> $shell_log
}

function full_backup
{
    log "full_backup begin, paras: $1"
    target_dir=$1
    innobackupex --defaults-file=$file_cnf --slave-info --safe-slave-backup --no-lock --no-timestamp\
      --user=$user_name --password=$password \
      --host=$ip --port=$port --stream=xbstream --compress --extra-lsndir="$lsn_dir" /tmp 2>$Xtrabackup_log \
      > ${back_dir}/${target_dir}_${timestamp}.xbstream
      #| $ssh_tool \ "cat - > ${back_dir}/${target_dir}_${timestamp}.xbstream"
      #| gzip > $back_dir/$target_dir.xbstream
    log "full_backup end"
}


function incremental_bakup
{
    log "incremental_bakup begin paras: $1, $2"
    xtra_target_dir=$1
    innobackupex --defaults-file=$file_cnf --slave-info --no-lock --no-timestamp \
    --user=$user_name --password=$password --safe-slave-backup --host=$ip \
    --port=$port --incremental --incremental-basedir="$lsn_dir" --extra-lsndir="$lsn_dir" \
    --stream=xbstream --compress /tmp 2>$Xtrabackup_log \
    > ${back_dir}/${xtra_target_dir}_${timestamp}.xbstream
    # | $ssh_tool \ "cat - > ${back_dir}/${xtra_target_dir}_${timestamp}.xbstream"
    # > $back_dir/$xtra_target_dir.xbstream
    log "incremental_bakup end"
}

function back_up_dir
{
    mv $back_dir ${back_dir}_bak_${timestamp}
    $ssh_tool \ "mv $back_dir ${back_dir}_bak_${timestamp}"
}

function delete_old_backup
{
    if [ -d $base_dir ]; then
        cd $base_dir
        find ${back_dir_name}_bak_* -mtime +20 | xargs rm -f
    fi
}

####################main###############
mkdir -p $back_dir
$ssh_tool \ "mkdir -p $back_dir"

mkdir -p $lsn_dir
log "++++++++++++++++++++++++++++++++++++++++++++++++++"
log "weekday:$weekday"
if [ 0 -eq $weekday ];then
    # 备份目录,从而删除lsn文件或者全备目录,当前启用的增备方式为lsn文件
    back_up_dir
    mkdir -p $back_dir
    full_backup backup0_full_backup
else
    # xtrabackup lsn文件存在则增备,不存在则全备.
    if [ -f $lsn_dir/xtrabackup_checkpoints ]; then
      incremental_bakup backup${weekday}_incremental_bakup
    else
      full_backup backup${weekday}_full_backup
    fi
fi

log "delete old backup"
delete_old_backup


log "--------------------------------------------------"

```


## 恢复脚本 

```
#!/bin/bash

SCRIPT_BASE_PATH=/u01/scripts
BACK_BASH_PATH=/data/master_backup
RESTORE_PATH=$BACK_BASH_PATH/mysql
FULL_DB_BACK_NAME=full_db_backup_from_master
MYSQL_DATA_DIR=/data/mysql

#db config
file_cnf=/etc/my.cnf
user_name=bkpuser
password=xxx
port=3306
ip=localhost
base_dir=/data/bakup2
back_dir_name=mysql
back_dir=$base_dir/$back_dir_name
lsn_dir=$back_dir/lsn

Xtrabackup_log=$back_dir/$FULL_DB_BACK_NAME.out

function getDiffTime
{
  return $(($2-$1))
}

#从主库备份数据到本地
function full_backdb_from_master
{
    startTime=`date +%s`
    echo "full backupdb process starting ...................."
    echo "back dir: ${back_dir}"
    #rm -rf ${back_dir}/${FULL_DB_BACK_NAME}.xbstream
    #rm -rf $Xtrabackup_log
    innobackupex --defaults-file=$file_cnf --slave-info --safe-slave-backup --no-lock --no-timestamp\
      --user=$user_name --password=$password \
      --host=$ip --port=$port \
      ${back_dir} \
      1> $Xtrabackup_log 2>$Xtrabackup_log
      #--stream=xbstream --compress --extra-lsndir="$lsn_dir" \
      # /tmp 2>$Xtrabackup_log \
      #> ${back_dir}/${FULL_DB_BACK_NAME}.xbstream
     endTime=`date +%s`
     diffTime=$(getDiffTime $startTime $endTime)
     echo "full backupdb complate and total time(second) is ${diffTime}"
    innobackupex --defaults-file=/etc/my.cnf --user=$user_name --password=$password --apply-log $back_dir/  1> ${Xtrabackup_log}.applylog 2>${Xtrabackup_log}.applylog
}

#还原数据
function restore_backdb
{
     startTime=`date +%s`
     echo "restore process starting........................."
     restore_log=$BACK_BASH_PATH/full_copy_from_master_restore.log
     mv $MYSQL_DATA_DIR ${MYSQL_DATA_DIR}_$startTime
     mkdir $MYSQL_DATA_DIR

     innobackupex --defaults-file=/etc/my.cnf --user=$user_name --password=$password --copy-back $RESTORE_PATH/ 1> $restore_log 2> $restore_log

     echo "restore complete and delete db disk file"
     endTime=`date +%s`

     diffTime=$(getDiffTime $startTime $endTime)
     echo "restore process complete and total time(second) is : ${diffTime}"
}

#启动slave
function start_slave
{
    startTime=`date +%s`
    echo `date -d @${startTime} "+%Y-%m-%d %H:%M:%S"` "slave reset process starting..................."
    endTime=`date +%s`

    chown mysql:mysql $MYSQL_DATA_DIR
    service mysqld start

    diffTime=$(getDiffTime $startTime $endTime)
    echo `date -d @${endTime} "+%Y-%m-%d %H:%M:%S"` "slave reset complete and total time(second) is : ${diffTime}"

}

#full_backdb_from_master
restore_backdb
start_slave
```
