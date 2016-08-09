Date: 2016-08-01
Title: salt安装
Tags: Salt
sulg: salt_install

最近研究salt装我那小一百台服务器, 之前一直是fabric安装的, 感觉salt还是挺好用的。python 安装还是习惯使用pip安装。 


## PIP 配置,指向豆瓣源
```
cat ~/.pip/pip.conf

[global]
index-url = http://pypi.douban.com/simple

[install]
trusted-host = pypi.douban.com
```


## 配置master
master 主要配置file_roots, pillar_roots, 
```
external_auth:
  pam:
    salt:
        - .*
        - '@runner'
        - '@wheel'
        
file_recv: False
file_recv_max_size: 1000
        
file_roots:
   base:
     - /srv/salt/base
   dev:
     - /srv/salt/dev
     - /srv/formulas/redis-formula
   prod:
     - /srv/salt/prod
     - /srv/formulas/redis-formula

pillar_roots:
  base:
    - /srv/pillar/base
  prod:
    - /srv/pillar/prod
```

## 配置minion
```
cat /etc/salt/minion

master: 10.1.1.1

```

```
cat /etc/salt/minion_id

hostname.x.x.x

```

## 设置init.d 文件, 并开机启动

```
chkconfig salt-minion on
chkconfig salt-master on
service salt-minion restart
service salt-master restart
```

/etc/init.d/salt-master
```
#!/bin/sh
#
# Salt master
###################################

# LSB header

### BEGIN INIT INFO
# Provides:          salt-master
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Salt master control daemon
# Description:       This is a daemon that controls the Salt minions.
### END INIT INFO


# chkconfig header

# chkconfig: 345 96 05
# description:  This is a daemon that controls the Salt minions
#
# processname: /usr/bin/salt-master


DEBIAN_VERSION=/etc/debian_version
SUSE_RELEASE=/etc/SuSE-release
# Source function library.
if [ -f $DEBIAN_VERSION ]; then
   break
elif [ -f $SUSE_RELEASE -a -r /etc/rc.status ]; then
    . /etc/rc.status
else
    . /etc/rc.d/init.d/functions
fi

# Default values (can be overridden below)
SALTMASTER=/usr/bin/salt-master
PYTHON=/usr/bin/python2.6
MASTER_ARGS=""

if [ -f /etc/default/salt ]; then
    . /etc/default/salt
fi

SERVICE=salt-master
PROCESS=salt-master

RETVAL=0

start() {
    echo -n $"Starting salt-master daemon: "
    if [ -f $SUSE_RELEASE ]; then
        startproc -f -p /var/run/$SERVICE.pid $SALTMASTER -d $MASTER_ARGS
        rc_status -v
    elif [ -e $DEBIAN_VERSION ]; then
        if [ -f $LOCKFILE ]; then
            echo -n "already started, lock file found"
            RETVAL=1
        elif $PYTHON $SALTMASTER -d $MASTER_ARGS >& /dev/null; then
            echo -n "OK"
            RETVAL=0
        fi
    else
        daemon --check $SERVICE $SALTMASTER -d $MASTER_ARGS
        RETVAL=$?
        [ $RETVAL -eq 0 ] && touch /var/lock/subsys/$SERVICE
        echo
        return $RETVAL
    fi
    RETVAL=$?
    echo
    return $RETVAL
}

stop() {
    echo -n $"Stopping salt-master daemon: "
    if [ -f $SUSE_RELEASE ]; then
        killproc -TERM $SALTMASTER
        rc_status -v
    elif [ -f $DEBIAN_VERSION ]; then
        # Added this since Debian's start-stop-daemon doesn't support spawned processes
        if ps -ef | grep "$PYTHON $SALTMASTER" | grep -v grep | awk '{print $2}' | xargs kill &> /dev/null; then
            echo -n "OK"
            RETVAL=0
        else
            echo -n "Daemon is not started"
            RETVAL=1
        fi
    else
        killproc $PROCESS
        RETVAL=$?
        echo
        [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/$SERVICE
        return $RETVAL
    fi
    RETVAL=$?
    echo
}

restart() {
   stop
   start
}

# See how we were called.
case "$1" in
    start|stop|restart)
        $1
        ;;
    status)
        if [ -f $SUSE_RELEASE ]; then
            echo -n "Checking for service salt-master "
            checkproc $SALTMASTER
            rc_status -v
        elif [ -f $DEBIAN_VERSION ]; then
            if [ -f $LOCKFILE ]; then
                RETVAL=0
                echo "salt-master is running."
            else
                RETVAL=1
                echo "salt-master is stopped."
            fi
        else
            status $PROCESS
            RETVAL=$?
        fi
        ;;
    condrestart)
        [ -f $LOCKFILE ] && restart || :
        ;;
    reload)
        echo "can't reload configuration, you have to restart it"
        RETVAL=1
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart|condrestart|reload}"
        exit 1
        ;;
esac
exit $RETVAL
```


/etc/init.d/salt-minion
```
#!/bin/sh
#
# Salt minion
###################################

# LSB header

### BEGIN INIT INFO
# Provides:          salt-minion
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Salt minion daemon
# Description:       This is the Salt minion daemon that can be controlled by the
#                    Salt master.
### END INIT INFO


# chkconfig header

# chkconfig: 345 97 04
# description:  This is the Salt minion daemon that can be controlled by the Salt master.
#
# processname: /usr/bin/salt-minion


DEBIAN_VERSION=/etc/debian_version
SUSE_RELEASE=/etc/SuSE-release
# Source function library.
if [ -f $DEBIAN_VERSION ]; then
   break
elif [ -f $SUSE_RELEASE -a -r /etc/rc.status ]; then
    . /etc/rc.status
else
    . /etc/rc.d/init.d/functions
fi

# Default values (can be overridden below)
SALTMINION=/usr/bin/salt-minion
PYTHON=/usr/bin/python2.6
MINION_ARGS=""

if [ -f /etc/default/salt ]; then
    . /etc/default/salt
fi

SERVICE=salt-minion
PROCESS=salt-minion

RETVAL=0

start() {
    echo -n $"Starting salt-minion daemon: "
    if [ -f $SUSE_RELEASE ]; then
        startproc -f -p /var/run/$SERVICE.pid $SALTMINION -d $MINION_ARGS
        rc_status -v
    elif [ -e $DEBIAN_VERSION ]; then
        if [ -f $LOCKFILE ]; then
            echo -n "already started, lock file found"
            RETVAL=1
        elif $PYTHON $SALTMINION -d $MINION_ARGS >& /dev/null; then
            echo -n "OK"
            RETVAL=0
        fi
    else
        if [[ ! -z "$(pidofproc -p /var/run/$SERVICE.pid $PROCESS)" ]]; then
            RETVAL=$?
            echo -n "already running"
        else
            daemon --check $SERVICE $SALTMINION -d $MINION_ARGS
            RETVAL=$?
            [ $RETVAL -eq 0 ] && touch /var/lock/subsys/$SERVICE
            echo
            return $RETVAL
        fi
    fi
    RETVAL=$?
    echo
    return $RETVAL
}

stop() {
    echo -n $"Stopping salt-minion daemon: "
    if [ -f $SUSE_RELEASE ]; then
        killproc -TERM $SALTMINION
        rc_status -v
        RETVAL=$?
    elif [ -f $DEBIAN_VERSION ]; then
        # Added this since Debian's start-stop-daemon doesn't support spawned processes
        if ps -ef | grep "$PYTHON $SALTMINION" | grep -v grep | awk '{print $2}' | xargs kill &> /dev/null; then
            echo -n "OK"
            RETVAL=0
        else
            echo -n "Daemon is not started"
            RETVAL=1
        fi
    else
        killproc $PROCESS
        RETVAL=$?
        [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/$SERVICE
        # tidy up any rogue processes:
        PROCS=`ps -ef | grep "$SALTMINION" | grep -v grep | awk '{print $2}'`
        if [ -n "$PROCS" ]; then
            kill $PROCS &> /dev/null
            sleep 1
            PROCS=`ps -ef | grep "$SALTMINION" | grep -v grep | awk '{print $2}'`
            if [ -n "$PROCS" ]; then
                kill -9 $PROCS &> /dev/null
            fi
        fi
    fi
    echo
}

restart() {
   stop
   start
}

# See how we were called.
case "$1" in
    start|stop|restart)
        $1
        ;;
    status)
        if [ -f $SUSE_RELEASE ]; then
            echo -n "Checking for service salt-minion "
            checkproc $SALTMINION
            rc_status -v
        elif [ -f $DEBIAN_VERSION ]; then
            if [ -f $LOCKFILE ]; then
                RETVAL=0
                echo "salt-minion is running."
            else
                RETVAL=1
                echo "salt-minion is stopped."
            fi
        else
            status $PROCESS
            RETVAL=$?
        fi
        ;;
    condrestart)
        [ -f $LOCKFILE ] && restart || :
        ;;
    reload)
        echo "can't reload configuration, you have to restart it"
        RETVAL=1
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart|condrestart|reload}"
        exit 1
        ;;
esac
exit $RETVAL
```


