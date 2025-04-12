# -*- mode: python ; coding: utf-8 -*-

import pyinstaller_versionfile
import os
import re

from subprocess import check_output



###
  # fpid: Exe name or PID number
  # https://ss64.com/nt/tasklist.html
  # https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tasklist
  #
  # Se usar o argumento /v tem mais detalhes, mas deixa mais leto
  # Se usar o argumento /fi "username eq { os.getenv( "computername" ) }\\{ os.getlogin() }" fitra o usuário atula e pega menos processo, mas deixa mais lento
###
def process_exists( fpid, filter: str = 'imagename' ):
	call = check_output( f'tasklist /nh /fo csv' )
	arr  = []

	for line in call.splitlines():
		line   = line.decode( 'utf-8' )

		if isinstance( fpid, str ) and re.search( fpid, line ):
			values = line.split( ',' )
			# remove double quotes
			values = [ item[ 1:-1 ] for item in values ]
			# pass list to dict
			arr.append({
				'name'   : values[0],
				'pid'    : int( values[1] ),
				'session': values[2],
				'status' : values[3],
				'memory' : values[4]
			})

	return None if len( arr ) == 0 else arr




versionfile = 'version.txt'
company     = 'Miamar Make'
appname     = 'UploadBD'




###
  # If a process is running, it must be closed before compiling.
  # Otherwise the compilation will give an error when saving the file.
  # signal.SIGINT = 2
###
process = process_exists( appname )
if process:
	print( 'It is necessary to close the running process before compilation.' )
	for prcs in process:
		print( f'Closing process PID: { prcs[ "pid" ] }' )
		os.kill( prcs[ 'pid' ], 2 )




# Check if files exist before compiling
filelist = [
	# icon to exectable
	'img/ico.ico',

	# icons to notification
	# 'img/logo.png',
	# 'img/picture.jpg'
]

# for file in filelist:
	# if not os.path.isfile( file ):
		# print( f'Failed compilation. File doesn\'t exist: "{ file }".' )
		# exit()




# https://stackoverflow.com/questions/14624245/what-does-a-version-file-look-like
pyinstaller_versionfile.create_versionfile(
	output_file       = versionfile,
	version           = '1.7.3',
	company_name      = company,
	file_description  = 'Safaly Database.',
	internal_name     = 'Simple App2',
	legal_copyright   = f'© { company }. All rights reserved.',
	original_filename = f'{ appname }.exe',
	product_name      = f'{ company } { appname }'
)


a = Analysis(
	[ 'main.py' ],
	pathex        = [],
	binaries      = [],
	hiddenimports = [],
	hookspath     = [],
	hooksconfig   = {},
	runtime_hooks = [],
	datas         = [],
	noarchive     = False,

	excludes      = [
		'PyInstaller',
		'pyinstaller_versionfile',
		'pip'
	]
)


pyz = PYZ( a.pure )
exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.datas,
	[],
	name                       = appname,
	debug                      = False,
	bootloader_ignore_signals  = False,
	strip                      = False,
	upx                        = True,
	upx_exclude                = [],
	runtime_tmpdir             = None,
	console                    = None,
	disable_windowed_traceback = False,
	argv_emulation             = False,
	target_arch                = None,
	codesign_identity          = None,
	entitlements_file          = None,
	version                    = versionfile,
	icon                       = [ filelist[0] ],
)


os.remove( versionfile )
os.system( 'pip freeze > requirements.txt' )
