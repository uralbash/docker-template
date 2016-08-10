#! /bin/bash
#
# build-app.sh
# Copyright (C) 2016 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
#


PROJECT_PATH=/home/vagrant/app

# build Qt project
cd ~/app \
    && . /opt/rh/devtoolset-3/enable    \
    && make clean                       \
    && PATH=/opt/Qt-5.7/bin/:$PATH      \
    qmake                               \
    && PATH=/opt/Qt-5.7/bin/:$PATH      \
    make
