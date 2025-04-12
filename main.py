# -*- coding: UTF-8 -*-

# https://stackoverflow.com/questions/43777106/program-made-with-pyinstaller-now-seen-as-a-trojan-horse-by-avg
# https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184
# https://stackoverflow.com/questions/5180440/how-to-capture-a-command-prompt-window-close-event-in-python

###
  # Descrição                                      | Arguments
  #  Diretório do arquivo que será feito o backuo  | --filename = [string/required ] Arquivo que vai ser feito o backup
  #  Regexp para procurar o arquivo existente      | --regexp   = [string/optional ] Procura e excluí o backup mais antigo
  #  Nome do usuário para logar no Mega.nz         | --login    = [string/optional ] Defalt is compiled
  #  Senha do usuário para logar no Mega.nz        | --passw    = [string/optional ] Defalt is compiled
  #  Delete local file after upload                | --delfile  = [boolean/optional] Default is True
###


import os
import sys
import re
from datetime import datetime


from lib.meganz import meganz
from lib.poog   import logg
from lib.github import github, issue



# organize sys.argv to dict
# --my_arg_name=my_arg_value
# --my_arg_name: return True
def args( prefix: str = '--' ) -> dict:
	args = {}
	index = 0
	for farg in sys.argv:
		find = re.search( prefix + r'([^=]+)(\s*=\s*(.*))?', farg )

		if not find:
			index += 1
			args[ index ] = farg

		else:
			if find.group( 1 ) and ( not find.group( 2 ) or find.group( 3 )) == '':
				args[ find.group( 1 )] = True
			else:
				args[ find.group( 1 )] = find.group( 3 )

	return args





###
  # Get image path after compiled (pyinstaller) or not.
###
def resource_path( relative_path ):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath( '.' )

	return os.path.join( base_path, relative_path )





def exiting( issue ):
	if not issue.exist():
		issue.create()
	else:
		issue.send()

	sys.exit()








def tryupload( account, file: str, limit: int = 2, attempt: int = 1 ):
	try:
		return account.upload( file )

	except Exception as err:
		if attempt < limit:
			issue.comment( '`{}` {}'.format( issue.tick, log.fatal( f'Erro inesperado!\t{ err }' )), True )
			issue.comment( f'`{ issue.tick }` { log.info( "Tentando fazer o upload novamente" ) }', True )
			return tryupload( account, file, limit, attempt + 1 )

		issue.comment( '`{}` {}'.format( issue.tick, log.fatal( f"Erro inesperado!\t{ err }" )), True )
		issue.comment( '`{}` {}'.format(
			issue.tick,
			log.debug( f'Foi feito { attempt } tentativa{ "s" if attempt > 1 else "" } de upload sem sucesso\n' )
		), True )

		exiting( issue )







args     = args()
log      = logg( 'UploadBD.log' )
filename = args.get( 'filename' )
# exit     = False
git      = github( token = '8d1d5dd4aqm', repo = 'F4Jonatas/UploadBD' )
issue    = git.issue( title = 'Miamar-Make' )





if not filename:
	issue.comment( f'`{ issue.tick }` { log.error( "O comando não foi passado corretamente" ) }', True )
	exiting( issue )


else:
	filename = os.path.join( filename )
	if not filename:
		issue.comment( f'`{ issue.tick }` { log.error( "O arquivo não foi encontrado" ) }', True )
		exiting( issue )





issue.comment( f'`{ issue.tick }` { log.info( "Iniciando sessão" ) }', True )
usr = meganz(
	args.get( 'login', 'ti@miamarmake.com.br' ),
	args.get( 'passw', '@s6$5vdJKMs' )
)



# O site só está suportando 2 arquivos,
# então antes tem que deletar um deles que será o mais antigo.
# Isso é porque o backup está quase 8GB e no Mega só suporta 20GB.
issue.comment( '`{}` {}'.format( issue.tick, log.info( 'Procurando backup\'s anteriores' )), True )
olds = usr.find( regex = args.get( 'regexp', r'IdeiaERP_\d+\.zip' ))


if olds:
	issue.comment( '`{}` {}'.format( issue.tick, log.info( f"Encontrado: { len( olds )} backup's" ) ), True )

	if len( olds ) >= 2:
		issue.comment( f'`{ issue.tick }` { log.warn( "Deletando permanentemente o backup mais antigo" ) }', True )
		usr.destroy( olds[0][ 'id' ] )
		issue.comment(
			'`{}` {}'.format(
				issue.tick,
				log.warn( 'Deletado "{}"{}'.format( olds[0][ 'name' ], ' da lixeira' if olds[0][ 'excluded' ] else '' )
			)
		), True )




issue.comment( f'`{ issue.tick }` { log.info( "Fazendo upload do backup" ) }', True )
attempt = tryupload( usr, filename, 2 )
if isinstance( attempt, dict ):
	issue.comment( f'`{ issue.tick }` { log.info( "Upload feito corretamente" ) }', True )

	if args.get( 'delfile', 'true' ) == 'true':
		issue.comment( f'`{ issue.tick }` { log.warn( "Deletando o backup local" ) }', True )
		os.remove( filename )
		issue.comment( '`{}` {}'.format( issue.tick, log.warn( f'Deletado "{ filename }"\n' )), True )

else:
	for err in attempt:
		issue.comment( f'`{ issue.tick }` { log.error( err ) }', True )


exiting( issue )



# [FATAL 06-04-2024 07:25:51.733] Erro inesperado!	HTTPConnectionPool(host='gfs270n170.userstorage.mega.co.nz', port=80): Max retries exceeded with url: /ul/muS_PPsN20gpLAKn-FkX_OMJ6-NiVO6tnRxqATqC8y9daQXXLCyc0dDehOoeFhBmO3Zb6hdN-kwP77P80ClGxA/4408737792 (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x000002D8433ED6D0>: Failed to resolve 'gfs270n170.userstorage.mega.co.nz' ([Errno 11001] getaddrinfo failed)"))
