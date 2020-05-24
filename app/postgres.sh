#!/bin/bash
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

function replace(){
    echo $1 $2
    if [ "$OS" == "Darwin" ] ; then
        echo $i|sed -i '' $1 $2
    else
        echo $i|sed -i $1 $2
    fi
}


function print_green(){
    echo -e "\e[32m$1\e[39m"
}

print_green "Would you like to set a password for your postgres user? [N/y]"
read SET_POSTGRES_PASSWORD
if [[ "$SET_POSTGRES_PASSWORD" == "y" ]]
then
    sudo -u postgres createuser --superuser $USER
    echo "\password $USER" | sudo -u postgres psql
    createdb $USER
fi


if [ ! -f ./app/settings/local_settings.py ] ; then
    print_green "Generating local settings"

    cp app/local_settings.py.default app/local_settings.py

    if [ INSTALL_POSTGRE ] ; then
        replace "s/database-name/${PWD##*/}/g" app/local_settings.py

        print_green "remember to configure in app/local_setings.py your database"
    else
        replace "s/postgresql_psycopg2/sqlite3/g" app/local_settings.py

        replace "s/database-name/\/tmp/${PWD##*/}.sql/g" app/local_settings.py
    fi
fi

engine=`python -c"from app.local_settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['ENGINE'])"`
debug=`python -c"from app.local_settings import DEBUG; print(DEBUG)"`
dbname=`python -c"from app.local_settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['NAME'])"`

if [ $debug = "True" ] ; then
echo "----------------------drop-database------------------------------"
    if [ $engine == "django.db.backends.sqlite3" ]; then
        if [ -f $dbname ] ; then
            echo "SQLITE: deleting $dbname"
            rm $dbname
        fi
    else
        dbuser=`python -c"from app.local_settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['USER'])"`
        dbpass=`python -c"from app.local_settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['PASSWORD'])"`
        if [ $engine == "django.db.backends.mysql" ]; then
            echo "drop database $dbname" | mysql --user=$dbuser --password=$dbpass
            echo "create database $dbname" | mysql --user=$dbuser --password=$dbpass
        else
            dropdb $dbname
            createdb $dbname
        fi
    fi
    python manage.py migrate
fi
