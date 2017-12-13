#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

proc_dir=
base_dir=$(dirname $0)
proc_dir=${proc_dir:-$base_dir}
proc_name=`echo ~+ | awk -F '/' '{print $NF}'`

if [ -f ${proc_dir}/commands/functions ];then
    . ${proc_dir}/commands/functions
elif [ -f /etc/init.d/functions ];then
    . /etc/init.d/functions
else
    echo "No functions script found in [./functions, ./install/functions, /etc/init.d/functions]"
    exit 1
fi

start() {
    proc_start=$"Starting ${proc_name} service:"
    proc_status=`"$proc_dir"/venv/bin/supervisorctl status "$proc_name" | awk '{print $2}'`
    if [ $proc_status = 'RUNNING' ];then
         echo -n "${proc_name} is Running..."
         success "$proc_start"
         echo
    else
        daemon $proc_dir/venv/bin/supervisorctl start "$proc_name" &> /dev/null
        echo -n "$proc_start"
        sleep 0.5
        proc_status=`"$proc_dir"/venv/bin/supervisorctl status "$proc_name" | awk '{print $2}'`
        if [ $proc_status = 'RUNNING' ];then
            success "$proc_start"
            echo
        else
            failure "$proc_start"
            echo
        fi
    fi
}

stop() {
    echo -n $"Stopping ${proc_name} service:"
    daemon $proc_dir/venv/bin/supervisorctl stop "$proc_name" &> /dev/null
    if [ $? -eq 0 ]; then
        echo_success
        echo
    else
        echo_failure
        echo
    fi
}

status(){
    proc_status=`"$proc_dir"/venv/bin/supervisorctl status "$proc_name" | awk '{print $2}'`
    if [ $proc_status == 'RUNNING' ];then
        echo -n "${proc_name} is Running..."
        success
        echo
    else
        echo -n "${proc_name} is Stop."
        failure
        echo
    fi
}

restart(){
    stop
    start
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;

  restart)
        restart
        ;;

  status)
        status
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 2
esac
