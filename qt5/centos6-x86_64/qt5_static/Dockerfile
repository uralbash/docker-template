# CentOS6 x86_64 + Qt5
#
# VERSION               0.0.1
# vi: set ft=dockerfile :

FROM uralbash/centos6-x86_64-gcc-cpp11:latest
MAINTAINER Dmitry Svintsov <root@uralbash.ru>

## Qt5
WORKDIR /var

RUN yum install -y mesa-libGL-devel
RUN rm -rf qt5
RUN git clone git://code.qt.io/qt/qt5.git
RUN cd qt5 \
        && git checkout 5.8 \
        && perl init-repository

WORKDIR /var/qt5
RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    ./configure                      \
    --prefix=/opt/Qt-5.8/            \
    -static                          \
    -release                         \
    -opensource                      \
    -confirm-license                 \
    -nomake examples                 \
    -nomake tests                    \
    -no-compile-examples             \
    -skip qtgamepad                  \
    -skip wayland                    \
    -qt-xcb                          \
    -fontconfig                      \
    -v

RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    make -j4
RUN . /opt/rh/devtoolset-3/enable && \
    make install
RUN . /opt/rh/devtoolset-3/enable && \
    make clean

## Run sshd
CMD ["/usr/sbin/sshd", "-D"]
EXPOSE 22

ONBUILD CMD ["/usr/sbin/sshd", "-D"]
ONBUILD EXPOSE 22
