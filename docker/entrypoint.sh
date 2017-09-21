#!/bin/bash


function test_mysql {
  mysqladmin -h ${PMGMT_MYSQL} -p${PMGMT_MYSQL_PWD} -P ${PMGMT_MYSQL_PORT} ping
}

RUN_CMD="${@:-python manage.py runserver 0.0.0.0:8000}"

DEBUG="${DEBUG:False}"

if [[ $RUN_CMD == *"python manage.py"* ]]; then

  count=0
  until ( test_mysql )
  do
    ((count++))
    if [ ${count} -gt 300 ]
    then
    echo "Services didn't become ready in time"
    exit 1
    fi
    sleep 0.1
  done

  if [[ $RUN_CMD != *"python manage.py test"* ]]; then
    python manage.py migrate
  fi
fi

if [[ $DEBUG == "False" ]] || [[ $DEBUG == "false" ]]; then
  python manage.py collectstatic --noinput
fi

exec $RUN_CMD
