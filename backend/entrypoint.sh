#!/bin/bash
if [ ! -z "$SQL_HOST" ]
then
    echo "waiting for postgres..."
    while ! /bin/nc -z "$SQL_HOST" "$SQL_PORT"; do
        sleep 0.5
    done

    echo "PostgreSQL started"
fi

exec "$@"

