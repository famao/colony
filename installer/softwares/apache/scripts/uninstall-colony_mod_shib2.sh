#!/bin/bash

source common/function.sh

a2dismod shib2

apt-get -y remove libapache2-mod-shib2


remove_templates "colony_mod_shib2"