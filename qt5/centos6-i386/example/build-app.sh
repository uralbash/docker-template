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
    && make clean \
    && PATH=/opt/gcc-4.8.2/bin/:/opt/Qt-5.7/bin/:$PATH \
    qmake \
    && PATH=/opt/gcc-4.8.2/bin/:/opt/Qt-5.7/bin/:$PATH \
    make
