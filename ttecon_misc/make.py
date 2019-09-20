#! /usr/bin/env python
#****************************************************
# GET LIBRARY
#****************************************************
import sys
from make.py.make_log import *
from make.py.run_program import *
from make.py.dir_mod import *

#****************************************************
# MAKE.PY STARTS
#****************************************************

# DEFINE FILE/DIRECTORY LOCATIONS
set_option(makelog='log/make.log', output_dir='log', temp_dir='')

clear_output_dirs()
start_make_logging()

# RUN ALL TESTS
run_stata(program='test/test_testgood.do', changedir=True, executable='statase')
run_stata(program='test/test_testbad.do', changedir=True, executable='statase')
run_stata(program='test/test_save_data.do', changedir=True, executable='statase')
run_stata(program='test/test_preliminaries.do', changedir=True, executable='statase')
run_stata(program='test/test_select_observations.do', changedir=True, executable='statase')
run_stata(program='test/test_build_recode_template.do', changedir=True, executable='statase')
run_stata(program='test/test_insert_tag.do', changedir=True, executable='statase')
run_stata(program='test/test_load_and_append.do', changedir=True, executable='statase')

end_make_logging()

raw_input('\n Press <Enter> to exit.')
