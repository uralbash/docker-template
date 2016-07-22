#!/usr/bin/env python
# Workaround for CentOS 6 yum overlay issue (docker/docker#10180)
# Based on yum-utils-1.1.31-34.el7 (GPLv2+)
#
# Example Dockerfile:
#  FROM centos:centos6
#  ADD this.py /
#  RUN /this.py && yum install -y pkg1
#  RUN /this.py && yum install -y pkg2

from os import walk, path, fstat

def _stat_ino_fp(fp):
    """
    Get the inode number from file descriptor
    """
    return fstat(fp.fileno()).st_ino


def get_file_list(rpmpath):
    """
    Enumerate all files in a directory
    """
    for root, _, files in walk(rpmpath):
        for f in files:
            yield path.join(root, f)


def for_each_file(files, cb, m='rb'):
    """
    Open each file with mode specified in `m`
    and invoke `cb` on each of the file objects
    """
    if not files or not cb:
        return []
    ret = []
    for f in files:
        with open(f, m) as fp:
            ret.append(cb(fp))
    return ret


def do_detect_copy_up(files):
    """
    Open the files first R/O, then R/W and count unique
    inode numbers
    """
    num_files = len(files)
    lower = for_each_file(files, _stat_ino_fp, 'rb')
    upper = for_each_file(files, _stat_ino_fp, 'ab')
    diff = set(lower + upper)
    return len(diff) - num_files

def main():
    rpmdb_path = '/var/lib/rpm'
    try:
        files = list(get_file_list(rpmdb_path))
        copied_num = do_detect_copy_up(files)
        print("ovl: Copying up (%i) files from OverlayFS lower layer" % copied_num)
    except Exception as e:
        print("ovl: Error while doing RPMdb copy-up:\n%s" % e)

if __name__ == '__main__':
    main()
