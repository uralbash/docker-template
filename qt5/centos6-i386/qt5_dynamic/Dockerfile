# CentOS6 x86_i386 + Qt5
#
# VERSION               0.0.1
# vi: set ft=dockerfile :

FROM uralbash/centos6-x86_i386-gcc-cpp11:latest
MAINTAINER Dmitry Svintsov <root@uralbash.ru>

## Qt5
WORKDIR /var

RUN yum install -y mesa-libGL-devel
RUN rm -rf qt5
RUN git clone git://code.qt.io/qt/qt5.git
RUN cd qt5 \
        && git checkout v5.9.1 \
        && perl init-repository

## Firebird
RUN yum install -y epel-release
RUN yum install -y firebird-libfbclient firebird-devel
# RUN ln -s /usr/lib/libfbclient.so.2 /usr/lib/libfbclient.so
# RUN yum install -y libtermcap-devel libstdc++-devel libtool ncurses-dev \
#       libstdc++-devel libicu
RUN mkdir -p /opt/firebird/src
RUN chmod 777 -R /opt/firebird
USER ${HOME_USER}
RUN GIT_SSL_NO_VERIFY=true git clone https://github.com/FirebirdSQL/firebird.git /opt/firebird/src
RUN . /home/vagrant/.nix-profile/etc/profile.d/nix.sh && \
      \
      nix-env -i autoconf automake pkg-config
# RUN PATH=/opt/gcc-4.8.2/bin/:$PATH \
#     . /home/vagrant/.nix-profile/etc/profile.d/nix.sh && \
#     cd /opt/firebird/src && \
#     \
#     ./autogen.sh --prefix=/opt/firebird --enable-debug=yes

USER root
WORKDIR /var/qt5
RUN PATH=/opt/gcc-4.8.2/bin/:$PATH  \
    . /home/vagrant/.nix-profile/etc/profile.d/nix.sh && \
    ./configure                     \
    --prefix=/opt/Qt-5/             \
    -release                        \
    -opensource                     \
    -confirm-license                \
    -nomake examples                \
    -nomake tests                   \
    -no-compile-examples            \
    -skip qtgamepad                 \
    -skip wayland                   \
    -qt-xcb                         \
    -platform linux-g++-32          \
    # -fontconfig                     \
    -plugin-sql-ibase               \
    -plugin-sql-sqlite              \
    -I/usr/include/firebird         \
    -L/usr/lib/                     \
    -v

RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /home/vagrant/.nix-profile/etc/profile.d/nix.sh && \
    make -j1
RUN make install
RUN make clean

## Run sshd
CMD ["/usr/sbin/sshd", "-D"]
EXPOSE 22

ONBUILD CMD ["/usr/sbin/sshd", "-D"]
ONBUILD EXPOSE 22
