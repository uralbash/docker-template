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
    && PATH=/opt/Qt-4.8/bin/:$PATH      \
    qmake                               \
    && PATH=/opt/Qt-4.8/bin/:$PATH      \
    make
