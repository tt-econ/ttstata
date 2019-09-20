#! /usr/bin/env python

import os
import time
import re
import locale
import subprocess

import make.py.private.metadata as metadata
import make.py.private.messages as messages
from glob import glob
from make.py.private.exceptionclasses import CritError, SyntaxError
from make.py.private.preliminaries import print_error

######################################################
# Directory modification functions
######################################################


def delete_all_files(top, exceptfile=''):
    """Delete every non-hidden file [except for any file with the same base
    name as "exceptfile"] in non-hidden sub-directories reachable from the
    directory named in "top". The original directory structure is kept intact
    (i.e. sub-directories are unchanged).

    CAUTION:  This is dangerous!  For example, if top == '/', it
    could delete all your disk files."""

    if exceptfile == '':
        print("\nDelete all files in", top)
    else:
        print("\nDelete all files in", top, "except files with base name",)
        os.path.basename(exceptfile)

    if os.path.isdir(top):
        for root, dirs, files in os.walk(top, topdown=True):
            # Ignore non-hidden sub-directories
            dirs_to_keep = []
            for dirname in dirs:
                if not dirname.startswith('.'):
                    dirs_to_keep.append(dirname)
            dirs[:] = dirs_to_keep

            # Remove all non-hidden files
            for filename in files:
                if (not filename.startswith('.')) and \
                        (filename != os.path.basename(exceptfile)):
                    os.remove(os.path.join(root, filename))


def delete_files(pathname):
    """Delete a possibly-empty list of files whose names match "pathname",
    which must be a string containing a path specification. "pathname" can be
    either absolute (like /usr/src/Python-1.5/Makefile) or relative (like
    ../../Tools/*/*.gif), and can contain shell-style wildcards."""

    print("\nDelete files", pathname)

    for f in glob(pathname):
        os.remove(f)


def remove_dir(pathname, options='@DEFAULTVALUE@'):
    """Completely remove a directory using the 'rmdir' command in Windows or
    'rm' command in Linux (useful for removing symlinks without deleting the
    source files or directory.)"""

    if os.name == 'posix':
        os_command = 'rmdirunix'
        if pathname[-1] == '/':
            pathname = pathname[0:-1]
    else:
        os_command = 'rmdirwin'

    command = metadata.commands[os_command]
    if options == '@DEFAULTVALUE@':
        options = metadata.default_options[os_command]

    subprocess.check_call(command % (options, pathname), shell=True)


def check_manifest(manifestlog='@DEFAULTVALUE@',
                   output_dir='@DEFAULTVALUE@',
                   makelog='@DEFAULTVALUE@'):
    """Produce an error if there are any .dta files in "output_dir" and all
    non-hidden sub-directories that are not in the manifest file "manifestlog",
    and produce a warning if there are .txt or .csv files not in the manifest
    along with a list of these files. All log is printed to "makelog" log
    file."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if manifestlog == '@DEFAULTVALUE@':
        manifestlog = metadata.settings['manifest_file']
    if output_dir == '@DEFAULTVALUE@':
        output_dir = metadata.settings['output_dir']
    if makelog == '@DEFAULTVALUE@':
        makelog = metadata.settings['makelog_file']

    print("\nCheck manifest log file", manifestlog)

    # Open main log file
    try:
        LOGFILE = open(makelog, 'a')
    except Exception as errmsg:
        print(errmsg)
        raise CritError(messages.crit_error_log % makelog)

    try:
        # Open manifest log file
        try:
            MANIFESTFILE = open(manifestlog, 'r')
        except Exception as errmsg:
            print(errmsg)
            raise CritError(messages.crit_error_log % manifestlog)
        manifest_lines = MANIFESTFILE.readlines()
        MANIFESTFILE.close()

        # Get file list
        try:
            file_list = []
            for i in range(len(manifest_lines)):
                if manifest_lines[i].startswith('File: '):
                    filepath = os.path.abspath(manifest_lines[i][6:].rstrip())
                    ext = os.path.splitext(filepath)[1]
                    if ext == '':
                        filepath = filepath + '.dta'
                    file_list.append(filepath)
        except Exception as errmsg:
            print(errmsg)
            raise SyntaxError(messages.syn_error_manifest % manifestlog)

        if not os.path.isdir(output_dir):
            raise CritError(messages.crit_error_no_directory % (output_dir))

        # Loop over all levels of sub-directories of output_dir
        for root, dirs, files in os.walk(output_dir, topdown=True):
            # Ignore non-hidden sub-directories
            dirs_to_keep = []
            for dirname in dirs:
                if not dirname.startswith('.'):
                    dirs_to_keep.append(dirname)
            dirs[:] = dirs_to_keep

            # Check each file
            for filename in files:
                ext = os.path.splitext(filename)[1]
                fullpath = os.path.abspath(os.path.join(root, filename))
                # non-hidden .dta file: error
                if (not filename.startswith('.')) and (ext == '.dta'):
                    print('Checking: ', fullpath)
                    if not (fullpath in file_list):
                        raise CritError(messages.crit_error_no_dta_file %
                                        (filename, manifestlog))
                # non-hidden .csv file: warning
                if (not filename.startswith('.')) and (ext == '.csv'):
                    print('Checking: ', fullpath)
                    if not (fullpath in file_list):
                        print(messages.note_no_csv_file % (filename,
                                                           manifestlog))
                        LOGFILE.write(messages.note_no_csv_file %
                                      (filename, manifestlog))
                # non-hidden .txt file: warning
                if (not filename.startswith('.')) and (ext == '.txt'):
                    print('Checking: ', fullpath)
                    if not (fullpath in file_list):
                        print(messages.note_no_txt_file % (filename,
                                                           manifestlog))
                        LOGFILE.write(messages.note_no_txt_file %
                                      (filename, manifestlog))
    except:
        print_error(LOGFILE)

    LOGFILE.close()


def list_directory(top, makelog='@DEFAULTVALUE@'):
    """List all non-hidden sub-directories of "top" and their content from top
    down. Write their names, modified times and sizes in bytes to "makelog" log
    file"""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option
    if makelog == '@DEFAULTVALUE@':
        makelog = metadata.settings['makelog_file']

    print("\nList all files in directory", top)

    # To print numbers (file sizes) with thousand separator
    locale.setlocale(locale.LC_ALL, '')

    makelog = re.sub('\\\\', '/', makelog)
    try:
        LOGFILE = open(makelog, 'a')
    except Exception as errmsg:
        print(errmsg)
        raise CritError(messages.crit_error_log % makelog)

    print('\n', file=LOGFILE)
    print('List of all files in sub-directories in', top, file=LOGFILE)

    try:
        if os.path.isdir(top):
            for root, dirs, files in os.walk(top, topdown=True):
                # Ignore non-hidden sub-directories
                dirs_to_keep = []
                for dirname in dirs:
                    if not dirname.startswith('.'):
                        dirs_to_keep.append(dirname)
                dirs[:] = dirs_to_keep

                # print out the sub-directory and its time stamp
                created = os.stat(root).st_mtime
                asciiTime = time.asctime(time.localtime(created))
                print(root, file=LOGFILE)
                print('created/modified', asciiTime, file=LOGFILE)

                # print out all the files in the sub-directories
                for name in files:
                    full_name = os.path.join(root, name)
                    created = os.path.getmtime(full_name)
                    size = os.path.getsize(full_name)
                    asciiTime = time.asctime(time.localtime(created))
                    print('%50s' % name, '--- created/modified',
                          asciiTime, '(',
                          locale.format('%d', size, 1), 'bytes )',
                          file=LOGFILE)
    except:
        print_error(LOGFILE)

    LOGFILE.write('\n')
    LOGFILE.close()


def clear_output_dirs(output_dir='@DEFAULTVALUE@',
                      temp_dir='@DEFAULTVALUE@'):
    """Create "output_dir" and "temp_dir" directories if they do not already
    exist. Delete all files in output and temp directories keeping directory
    structure (i.e. sub-directories).

    If output_dir == '' then output directory will not be created.
    If temp_dir == '' then temp directory will not be created."""

    # metadata.settings should not be part of argument defaults so that they
    # can be overwritten by make_log.set_option

    if output_dir == '@DEFAULTVALUE@':
        output_dir = metadata.settings['output_dir']
    if temp_dir == '@DEFAULTVALUE@':
        temp_dir = metadata.settings['temp_dir']

    if output_dir != '':
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        delete_all_files(output_dir)
    if temp_dir != '':
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        delete_all_files(temp_dir)


def clear_output_dirs_local(output_dir='@DEFAULTVALUE@',
                            temp_dir='@DEFAULTVALUE@',
                            output_local_dir='@DEFAULTVALUE@'):

    if output_local_dir == '@DEFAULTVALUE@':
        output_local_dir = metadata.settings['output_local_dir']

    clear_output_dirs(output_dir, temp_dir)

    if output_local_dir != '':
        if not os.path.isdir(output_local_dir):
            os.makedirs(output_local_dir)
        delete_all_files(output_local_dir)
