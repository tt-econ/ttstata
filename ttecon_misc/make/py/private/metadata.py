#! /usr/bin/env python

######################################################
# Define Metadata
######################################################

makelog_started = False

# Settings (directory keys must end in 'dir' and file keys must end in 'file')
settings = {
    'external_dir'      : '../external/',
    'links_dir'         : '../external_links/',
    'externalslog_file' : './get_externals.log',
    'linkslog_file'     : './make_links.log',
    'output_dir'        : '../output/',
    'output_local_dir'  : '../output_local/',
    'temp_dir'          : '../temp/',
    'makelog_file'      : '../output/make.log',
    'manifest_file'     : '../output/data_file_manifest.log',
    'link_logs_dir'     : '../log/',
    'link_stats_file'   : 'link_stats.log',
    'link_heads_file'   : 'link_heads.log',
    'link_orig_file'    : 'link_orig.log',
    'stats_file'        : 'stats.log',
    'heads_file'        : 'heads.log'
}

# Commands
commands = {
    'makelinkwin'  :  'mklink %s \"%s%s\" \"%s%s\"',
    'makelinkunix' :  'ln -s \"%s%s\" \"%s%s\"',
    'rmdirwin'     :  'rmdir %s \"%s\"',
    'rmdirunix'    :  'rm %s \"%s\"',
    'stata'        :  '%s %s do %s',
    'matlab'       :  '%s -r %s -logfile %s %s',
    'perl'         :  '%s %s %s %s',
    'python'       :  '%s %s %s %s',
    'math'         :  '%s -script %s %s',
    'st'           :  '%s %s',
    'lyx'          :  '%s -e pdf2 %s %s',
    'rbatch'       :  '%s %s %s %s',
    'rinstall'     :  '%s %s %s %s',
    'sas'          :  '%s %s %s',
    'tex'          :  '%s %s %s'
}

default_options = {
    'rmdirwin'   : '/s /q',
    'rmdirunix'  : '-rf',
    'matlabunix' : '-nodisplay -nosplash',
    'matlabwin'  : '-noFigureWindows -wait -automation',
    'statawin'   : '/e /q',
    'stataunix'  : '-b -q',
    'rbatch'     : '--no-save',
    'rinstall'   : '--no-multiarch',
    'saswin'     : '-nosplash',
    'math'       : '-noprompt',
    'tex'        : '-pdf -ps- -f -quiet'
}

option_overlaps = {
    'matlab' :     {'log': '-logfile'},
    'sas'    :     {'log': '-log', 'lst': '-print'}
}

default_executables = {
    'statawin'    :  '%STATAEXE%',
    'statamac'    :  'stata-mp',
    'statalinux'  :  'stata-mp',
    'matlab'      :  'matlab',
    'perl'        :  'perl',
    'python'      :  'python',
    'mathnonunix' :  'MathKernel',
    'mathunix'    :  'MathematicaScript',
    'st'          :  'st',
    'lyx'         :  'lyx',
    'rbatch'      :  'R CMD BATCH',
    'rinstall'    :  'R CMD INSTALL',
    'sas'         :  'sas',
    'tex'         :  'latexmk'
}

extensions = {
    'stata'    : '.do',
    'matlab'   : '.m',
    'perl'     : '.pl',
    'python'   : '.py',
    'math'     : '.m',
    'stc'      : '.stc',
    'stcmd'    : '.stcmd',
    'lyx'      : '.lyx',
    'rbatch'   : '.r',
    'rinstall' : '',
    'sas'      : '.sas',
    'tex'      : '.tex',
    'other'    : ''
}

option_start_chars = ['-', '+']

# Locals
file_loc = {
}
