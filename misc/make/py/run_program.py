#! /usr/bin/env python

import os
import shutil
import pyparsing

import make.py.private.metadata as metadata
from make.py.private.runprogramdirective import RunProgramDirective, \
    RunCommandDirective, RunRPackageDirective
from make.py.private.preliminaries import add_error_to_log

###############################################################
# Run Stata, Matlab, Perl, Python, StatTransfer
# Mathematica, RInstall, RBatch, TeX
###############################################################


def run_stata(**kwargs):
    """Run Stata program with log file

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('stata')

        # Set option
        option = run.option
        if not option:
            if run.osname.startswith('win'):
                option = metadata.default_options['statawin']
            else:
                option = metadata.default_options['stataunix']

        # Set executable
        executable = run.executable
        if not executable:
            if run.osname.startswith('win'):
                executable = metadata.default_executables['statawin']
            elif run.osname.startswith('linux'):
                executable = metadata.default_executables['statalinux']
            else:
                executable = metadata.default_executables['statamac']

        # Set default_log
        if run.changedir:
            program = '"' + run.program + '"'
            default_log = os.path.join(run.program_path,
                                       run.program_name + '.log')
        else:
            program = '"' + os.path.join(run.program_path, run.program) + '"'
            default_log = os.path.join(os.getcwd(), run.program_name + '.log')

        command = metadata.commands['stata'] % (executable, option, program)
        run.execute_run(command)

        run.move_log(default_log)
    except:
        add_error_to_log(run.makelog)


def run_matlab(**kwargs):
    """Run Matlab program with log file

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('matlab')
        run.changedir = True

        # Get option
        option = run.option
        if not run.option:
            if run.osname.startswith('win'):
                option = metadata.default_options['matlabwin']
            else:
                option = metadata.default_options['matlabunix']
        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['matlab']

        program = run.program_name
        default_log = os.path.join(run.program_path, run.program_name + '.log')
        command = metadata.commands['matlab'] % (executable, program,
                                                 run.program_name + '.log',
                                                 option)

        run.execute_run(command)
        run.move_log(default_log)
    except:
        add_error_to_log(run.makelog)


def run_perl(**kwargs):
    """Run Perl program

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('perl')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['perl']

        command = metadata.commands['perl'] % (executable, run.option,
                                               program, run.args)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_python(**kwargs):
    """Run Python program

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('python')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['python']

        command = metadata.commands['python'] % (executable, run.option,
                                                 program, run.args)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_mathematica(**kwargs):
    """Run Mathematica program

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('math')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'
        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['math']

        # Get executable
        executable = run.executable
        if not run.executable:
            if run.osname.startswith('darwin'):
                executable = metadata.default_executables['mathunix']
            else:
                executable = metadata.default_executables['mathnonunix']

        command = metadata.commands['math'] % (executable, program, option)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_stc(**kwargs):
    """Run StatTransfer .stc program

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('stc')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['st']

        command = metadata.commands['st'] % (executable, program)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_stcmd(**kwargs):
    """Run StatTransfer .stcmd program

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('stcmd')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['st']

        command = metadata.commands['st'] % (executable, program)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_lyx(**kwargs):
    """Run Lyx export to Pdf

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('lyx')
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['lyx']

        command = metadata.commands['lyx'] % (executable, program, run.option)

        run.execute_run(command)

        # Move PDF output
        pdfname = os.path.join(run.program_path, run.program_name + '.pdf')
        pdfout = run.pdfout
        if '.pdf' not in pdfout:
            pdfout = os.path.join(pdfout, run.program_name + '.pdf')
        if os.path.abspath(pdfname) != os.path.abspath(pdfout):
            shutil.copy2(pdfname, pdfout)
            os.remove(pdfname)

    except:
        add_error_to_log(run.makelog)


def run_rbatch(**kwargs):
    """Run R batch program with log file

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('rbatch')

        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['rbatch']
        if run.changedir:
            program = '"' + run.program + '"'
            default_log = os.path.join(run.program_path,
                                       run.program_name + '.Rout')
        else:
            program = '"' + os.path.join(run.program_path, run.program) + '"'
            default_log = os.path.join(os.getcwd(), run.program_name + '.Rout')

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['rbatch']

        command = metadata.commands['rbatch'] % (executable, option, program,
                                                 run.program_name + '.Rout')

        run.execute_run(command)
        run.move_log(default_log)
    except:
        add_error_to_log(run.makelog)


def run_rinstall(**kwargs):
    """Install R package

    """

    run = RunRPackageDirective(kwargs)
    try:
        run.error_check('rinstall')

        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['rinstall']

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['rinstall']

        command = metadata.commands['rinstall'] % (executable, option,
                                                   run.lib, run.package)

        run.execute_run(command)
    except:
        add_error_to_log(run.makelog)


def run_sas(**kwargs):
    """Run SAS script

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('sas')

        # Get option
        option = run.option
        if not run.option:
            if run.osname != 'posix':
                option = metadata.default_options['saswin']

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['sas']

        # Get log, lst, and program
        if run.changedir:
            program = '"' + run.program + '"'
            default_log = os.path.join(run.program_path,
                                       run.program_name + '.log')
            default_lst = os.path.join(run.program_path,
                                       run.program_name + '.lst')
        else:
            program = '"' + os.path.join(run.program_path, run.program) + '"'
            default_log = os.path.join(os.getcwd(), run.program_name + '.log')
            default_lst = os.path.join(os.getcwd(), run.program_name + '.lst')

        if run.osname == 'posix':
            command = metadata.commands['sas'] % (executable, option, program)
        else:
            command = metadata.commands['sas'] % (executable, program, option)

        run.execute_run(command)
        run.move_log(default_log)
        run.move_lst(default_lst)
    except:
        add_error_to_log(run.makelog)


def run_tex(**kwargs):
    """Run latexmk to convert .tex to .pdf

    """

    run = RunProgramDirective(kwargs)
    try:
        run.error_check('tex')
        run.changedir = True

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['tex']

        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['tex']
            option = option + ' -output-directory=temp'

        prog_tex = run.program_name + metadata.extensions['tex']
        prog_tilde_tex = run.program_name + '_tilde' + \
            metadata.extensions['tex']
        file_path = os.path.join(run.program_path, prog_tex)
        file_path_tilde = os.path.join(run.program_path, prog_tilde_tex)

        add_tilde(file_path, file_path_tilde)
        check_for_multiple_periods(file_path_tilde, run.makelog)

        program = '"' + prog_tilde_tex + '"'
        command = metadata.commands['tex'] % (executable, option, program)

        run.execute_run(command)

        out_dir = metadata.settings['output_dir']
        print(os.path.abspath(out_dir))
        try:
            shutil.copy2(file_path_tilde, out_dir)
            os.remove(file_path_tilde)
        except:
            pass

        pdf_tilde = os.path.join(run.program_path, 'temp',
                                 run.program_name + '_tilde.pdf')
        pdf = os.path.join(run.program_path, 'temp', run.program_name + '.pdf')
        os.rename(pdf_tilde, pdf)

        try:
            shutil.copy2(pdf, out_dir)
        except:
            print('error')
        shutil.rmtree(os.path.join(run.program_path, 'temp'))
    except:
        add_error_to_log(run.makelog)
        try:
            prog_tilde_tex = run.program_name + '_tilde' + \
                metadata.extensions['tex']
            file_path_tilde = os.path.join(run.program_path, prog_tilde_tex)
            os.remove(file_path_tilde)
        except OSError:
            pass


def add_tilde(input_file, output_file):

    f = open(input_file)
    contents = f.read()
    f.close()
    new_contents = contents.replace(' $', '~$')
    f = open(output_file, 'w')
    f.write(new_contents)
    f.close()


def check_for_multiple_periods(filepath, logfile):
    """Check for multiple periods"""

    file = open(filepath, 'r')
    line_number = 0
    for line in file:
        number_of_periods = 0
        line_number += 1
        line = '{' + line + '}'
        line = line.replace("'", "")
        try:
            parens = pyparsing.nestedExpr('{', '}', content=None)
            parsed = parens.parseString(line)
            parsed = parsed[0]
            for i in range(len(parsed)):
                if (type(parsed[i]) == str):
                    parsed[i] = parsed[i].split(r'\footnote')[0]
                    if (parsed[i][-1] == "."):
                        number_of_periods += 1
        except:
            add_syntax_error_to_log(logfile, line_number)
        if number_of_periods > 1:
            add_period_error_to_log(logfile, line_number)
    file.close()


def add_syntax_error_to_log(makelog, line_number):
    LOGFILE = open(makelog, 'a')

    print('\n', file=LOGFILE)
    print('Check syntax on line ' + str(line_number), file=LOGFILE)

    print('\n')
    print('Check syntax on line ' + str(line_number))

    LOGFILE.flush()
    LOGFILE.close()


def add_period_error_to_log(makelog, line_number):
    LOGFILE = open(makelog, 'a')

    print('\n', file=LOGFILE)
    print('Check periods on line ' + str(line_number), file=LOGFILE)

    print('\n')
    print('Check periods on line ' + str(line_number))

    LOGFILE.flush()
    LOGFILE.close()


def run_command(**kwargs):
    """Run a Shell command

    """

    run = RunCommandDirective(kwargs)
    try:
        run.error_check('other')
        run.execute_run(run.command)
    except:
        add_error_to_log(run.makelog)
