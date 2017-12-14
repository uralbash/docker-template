# CentOS6 x86_64 + Qt5
#
# VERSION               0.0.1
# vi: set ft=dockerfile :

FROM uralbash/centos6-x86_64-gcc-cpp11:latest
MAINTAINER Dmitry Svintsov <root@uralbash.ru>

## Qt5
WORKDIR /var

ENV QT_VERSION v5.9.3
RUN rm -rf qt5
RUN git clone git://code.qt.io/qt/qt5.git
RUN cd qt5 \
        && git checkout $QT_VERSION \
        && perl init-repository
RUN yum install -y mesa-libGL-devel
RUN yum install -y gstreamer-devel gstreamer-plugins-base-devel

## FireBird
RUN yum install -y epel-release
RUN yum install -y firebird-libfbclient firebird-devel

## Build Qt
WORKDIR /var/qt5

RUN echo "DEFINES+=SQLITE_ENABLE_JSON1" >> qtbase/src/plugins/sqldrivers/sqlite/sqlite.pro

RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    ./configure                      \
    --prefix=/opt/Qt-5/              \
    # -platform linux-g++              \
    -release                         \
    -opensource                      \
    -confirm-license                 \
    -nomake examples                 \
    -nomake tests                    \
    -no-compile-examples             \
    -skip qtgamepad                  \
    -skip wayland                    \
    -qt-zlib                         \
    -qt-libjpeg                      \
    -qt-libpng                       \
    -qt-xcb                          \
    -qt-xkbcommon                    \
    -qt-pcre                         \
    -qt-harfbuzz                     \
    # -qt-freetype                     \
    -fontconfig                      \
    -plugin-sql-ibase                \
    -plugin-sql-sqlite               \
    -I/usr/include/firebird          \
    -L/usr/lib/                      \
    -v

RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    make -j4
RUN . /opt/rh/devtoolset-3/enable && \
    make -j4 install

WORKDIR /var/qt5/qtvirtualkeyboard
## Qt VirtualKeyboard
RUN PATH=/opt/Qt-5/bin/:/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    qmake CONFIG+="lang-ru_RU" \
      PREFIX=/opt/Qt-5/
RUN PATH=/opt/Qt-5/bin/:/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    make -j4 install
RUN . /opt/rh/devtoolset-3/enable && \
    make -j4 clean

WORKDIR /var/qt5
RUN . /opt/rh/devtoolset-3/enable && \
    make -j4 clean
