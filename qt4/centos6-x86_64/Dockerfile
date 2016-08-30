# CentOS6 x86_64 + Qt4
#
# VERSION               0.0.1
# vi: set ft=dockerfile :

FROM centos:centos6
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

RUN yum -y update; yum clean all

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

## Packages
RUN yum install bzip2 tar -yyy
RUN yum install openssh-clients openssh-server sudo -yyy
RUN yum groupinstall "X Window System" -yyy
RUN yum install dejavu-lgc-sans-fonts -yyy

## GCC 4.9.2
RUN yum install -y centos-release-scl
RUN yum install -y devtoolset-3-toolchain
RUN scl enable devtoolset-3 bash

## Fonts
RUN yum install -y freetype-devel
RUN yum install -y fontconfig-devel
RUN yum install -y wget

RUN yum --skip-broken groupinstall -y 'Development Tools'
RUN yum install -y openssl-devel
RUN yum install -y libXext-devel
RUN yum install -y libXt-devel

RUN wget -qO- \
      https://download.qt.io/archive/qt/4.8/4.8.6/qt-everywhere-opensource-src-4.8.6.tar.gz | tar xvz

WORKDIR qt-everywhere-opensource-src-4.8.6
RUN source /opt/rh/devtoolset-3/enable \
    && ./configure -platform linux-g++ -v \
        -prefix /opt/Qt-4.8/ \
        -release \
        -static \
        -fontconfig \
        -opensource \
        -confirm-license \
        -gtkstyle \
        -no-webkit \
        -nomake demos \
        -nomake examples \
        -no-libjpeg \
        -no-cups \
        -no-openvg \
        -no-libmng \
        -no-gif \
        -qt-libpng \
        -no-libtiff \
        -no-accessibility \
        -no-phonon \
        -no-script \
        -no-declarative \
        -no-declarative-debug \
        -no-openssl \
        -no-qt3support \
        -no-scripttools \
        -no-exceptions
RUN source /opt/rh/devtoolset-3/enable \
    && make -j4
RUN source /opt/rh/devtoolset-3/enable \
    && make install

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

## sshd entrypoint
CMD ["/usr/sbin/sshd", "-D"]
EXPOSE 22
ONBUILD CMD ["/usr/sbin/sshd", "-D"]
ONBUILD EXPOSE 22
