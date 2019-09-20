#! /usr/bin/env python

import subprocess
import os
import sys
import datetime
import time
import locale
import shutil

# ****************************************************
# MAKE.PY STARTS
# ****************************************************


def main():
    start_make_log('./log/make.log', './log/')
    os.chdir('./test/')
    run_tests('../log/make.log', '../log/test.log')
    os.chdir('../')
    end_make_log('./log/make.log')


def start_make_log(makelog, output_dir):
    # START MAKE LOG
    print("\nStart log file: ", makelog)

    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    LOGFILE = open(makelog, 'w')
    time_begin = datetime.datetime.now().replace(microsecond=0)
    # sys.stderr = LOGFILE
    working_dir = os.getcwd()
    print("\n make.py started:", time_begin, working_dir, "\n\n", file=LOGFILE)

    # LIST FILES IN ./log DIRECTORY
    print('\n', file=LOGFILE)
    print('List of all files in sub-directories in', output_dir, file=LOGFILE)
    created = os.stat(output_dir).st_mtime
    asciiTime = time.asctime(time.localtime(created))
    print(output_dir, file=LOGFILE)
    print('created/modified', asciiTime, file=LOGFILE)
    files = os.listdir(output_dir)
    for name in files:
        if not name.startswith('.'):
            full_name = os.path.join(output_dir, name)
            created = os.path.getmtime(full_name)
            size = os.path.getsize(full_name)
            asciiTime = time.asctime(time.localtime(created))
            print('%50s' % name, '--- created/modified',
                  asciiTime, '(',
                  locale.format('%d', size, 1), 'bytes )', file=LOGFILE)
            if name != 'make.log':
                os.remove(os.path.join(output_dir, name))
    LOGFILE.close()


def run_tests(makelog, test_log):
    # RUN ALL TESTS
    command = 'python run_all_tests.py'
    LOGFILE = open(makelog, 'a')
    TESTLOG = open(test_log, 'w')
    print('Executing: ', command)
    subprocess.check_call(command, shell=True, stdout=TESTLOG, stderr=TESTLOG)
    TESTLOG.close()
    print(open(test_log, 'r').read(), file=LOGFILE)
    LOGFILE.close()


def end_make_log(makelog):
    # END MAKE LOG
    print("\nEnd log file: ", makelog)
    LOGFILE = open(makelog, 'a')
    time_end = datetime.datetime.now().replace(microsecond=0)
    print('\n make.py ended:', time_end, file=LOGFILE)
    LOGFILE.close()


main()
