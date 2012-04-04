#!/bin/bash


basedir="/etc/horizon"
databasedir="/var/lib/horizon"

pushd $basedir/dashboard

# create db directory
mkdir -p $databasedir

chown www-data.www-data $databasedir
su www-data -c "/usr/bin/python manage.py syncdb"
popd
