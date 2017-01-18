# CentOS6 x86_64 + Qt5
#
# VERSION               0.0.1
# vi: set ft=dockerfile :

FROM centos:6
MAINTAINER Dmitry Svintsov <root@uralbash.ru>

ENV HOME_USER vagrant
ENV HOME_PASS 123

WORKDIR /tmp

## Add USER
RUN useradd -m -s /bin/bash ${HOME_USER} -u 1000 && \
    echo "${HOME_USER}:${HOME_PASS}"|chpasswd && \
    groupadd sudo && \
    gpasswd -a ${HOME_USER} sudo && \
    echo ${HOME_USER}' ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

## Install an SSH keys
RUN yum -y install openssh-server openssh-clients

RUN rm -f /etc/ssh/ssh_host_rsa_key
RUN rm -f /etc/ssh/ssh_host_dsa_key
RUN rm -f /etc/ssh/ssh_host_ecdsa_key
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -q -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key

RUN mkdir -p /home/vagrant/.ssh
RUN chmod 0700 /home/vagrant/.ssh
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keys
RUN chmod 0600 /home/vagrant/.ssh/authorized_keys
RUN chown -R vagrant: /home/vagrant/.ssh
RUN mkdir -p /etc/sudoers.d
RUN install -b -m 0440 /dev/null /etc/sudoers.d/vagrant
RUN echo 'vagrant ALL=NOPASSWD: ALL' >> /etc/sudoers.d/vagrant
RUN sed -i 's/Defaults    requiretty/#Defaults    requiretty/g' /etc/sudoers

## Minimal requirements
RUN yum install bzip2 tar wget -yyy

## C++11
RUN yum install -y centos-release-scl
RUN yum install -y devtoolset-3-toolchain 
RUN scl enable devtoolset-3 bash

## Xorg
RUN yum -y install libX11-devel
RUN yum -y groupinstall "X Window System"

## libxcb
RUN yum -y install libxcb libxcb-devel xcb-util xcb-util-devel

## Fonts
RUN yum -y install freetype-devel
RUN yum -y install fontconfig-devel

## Nix
RUN yum install -y perl-Digest-SHA
# Nix requires ownership of /nix.
RUN mkdir -m 0755 /nix && chown ${HOME_USER} /nix
# Change docker user to vagrant
USER ${HOME_USER}
# Set some environment variables for Docker and Nix
ENV USER ${HOME_USER}
# Change our working directory to $HOME
WORKDIR /home/${HOME_USER}
# install Nix
RUN curl https://nixos.org/nix/install | sh
# update the nix channels
# Note: nix.sh sets some environment variables. Unfortunately in
# Docker environment variables don't persist across `RUN` commands
# without using Docker's own `ENV` command, so we need to prefix
# our nix commands with `. .nix-profile/etc/profile.d/nix.sh` to
# ensure nix manages our $PATH appropriately.
RUN . .nix-profile/etc/profile.d/nix.sh && \
    nix-channel --update
# Install packages.
RUN . .nix-profile/etc/profile.d/nix.sh && \
    nix-env -i git

USER root
RUN yum -y remove git
RUN ln -s /home/vagrant/.nix-profile/bin/git /usr/bin/git

## Qt5
WORKDIR /tmp

RUN yum install -y mesa-libGL-devel
RUN rm -rf qt5
RUN git clone git://code.qt.io/qt/qt5.git

RUN cd qt5 \
        && git checkout 5.7 \
        && perl init-repository

WORKDIR /tmp/qt5
RUN PATH=/opt/gcc-4.8.2/bin/:$PATH   \
    . /opt/rh/devtoolset-3/enable && \
    ./configure                      \
    --prefix=/opt/Qt-5.7/            \
    -static                          \
    -release                         \
    -opensource                      \
    -confirm-license                 \
    -nomake examples                 \
    -nomake tests                    \
    -no-compile-examples             \
    -skip qtgamepad                  \
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
