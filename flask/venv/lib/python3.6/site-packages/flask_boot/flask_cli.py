#!/usr/bin/env python
# coding: utf-8

"""
Flask Boot
Usage:
  flask_boot new <project>

Options:
  -h, --help          Help information.
  -v, --version       Show version.
"""

import os
import io
from os.path import (
    dirname,
    abspath
)
import logging
import errno
import shutil
from tempfile import mkstemp
from logging import StreamHandler, DEBUG
from docopt import docopt
from flask_boot import __version__

logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())

REWRITE_FILE_EXTS = ('.html', '.conf', '.py', '.json', '.md')


def generate_project(args):
    src = os.path.join(dirname(abspath(__file__)), 'project')

    project_name = args.get('<project>')

    if not project_name:
        logger.warning('Project name cannot be empty.')
        return
    dst = os.path.join(os.getcwd(), project_name)

    # if os.path.isdir(dst):
    #     logger.warning('Project directory already exists.')
    #     return
    logger.info('Start generating application files.')

    _mkdir_p(dst)

    for src_dir, sub_dirs, file_names in os.walk(src):
        relative_path = src_dir.split(src)[1].lstrip(os.path.sep)
        dst_dir = os.path.join(dst, relative_path)
        dst_dir = dst_dir.replace('application', project_name)

        if src != src_dir:
            _mkdir_p(dst_dir)

        for filename in file_names:
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)

            if filename.endswith(REWRITE_FILE_EXTS):
                _rewrite_and_copy(src_file, dst_file, project_name)
            else:
                shutil.copy(src_file, dst_file)

    logger.info('Finish generating project files.')


def _mkdir_p(path):
    """mkdir -p path"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    else:
        logger.info("New: %s%s", path, os.path.sep)


def _rewrite_and_copy(src_file, dst_file, project_name):
    """Replace vars and copy."""
    # Create temp file
    fh, abs_path = mkstemp()

    with io.open(abs_path, 'w', encoding='utf-8') as new_file:
        with io.open(src_file, 'r', encoding='utf-8') as old_file:
            for line in old_file:
                new_line = line.replace('application', project_name). \
                    replace('Application', project_name.title())
                new_file.write(new_line)

    # Copy to new file
    shutil.copy(abs_path, dst_file)
    os.close(fh)


def main():
    args = docopt(__doc__, version="flask_boot {0}".format(__version__))
    if args.get('new'):
        generate_project(args)
    else:
        print args


if __name__ == "__main__":
    main()
