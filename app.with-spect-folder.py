


# import onedrivesdk
from lib.log  import conso

# https://github.com/OneDrive/onedrive-sdk-python#authentication
# https://filemanagerpro.io/article/how-can-i-get-my-microsoft-account-client-id-and-client-secret-key/

import os
import sys
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Isso evita alguns consoles do windows em não reconhecer as cores
os.system( '' )

print('\033[5m __  __ _       __  __              __  __       _\n' +
      '|  \\/  (_) __ _|  \\/  | __ _ _ __  |  \\/  | __ _| | _____\n' +
      '| |\\/| | |/ _` | |\\/| |/ _` | \'__| | |\\/| |/ _` | |/ / _ \\\n' +
      '| |  | | | (_| | |  | | (_| | |    | |  | | (_| |   <  __/\n' +
      '|_|  |_|_|\\__,_|_|  |_|\\__,_|_|    |_|  |_|\\__,_|_|\\_\\___|\n' +
      '  __         ____             _                        __\n' +
      ' / /        | __ )  __ _  ___| | ___   _ _ __          \\ \\\n' +
      '/ /         |  _ \\ / _` |/ __| |/ / | | | \'_ \\          \\ \\\n' +
      '\\ \\         | |_) | (_| | (__|   <| |_| | |_) |         / /\n' +
      ' \\_\\        |____/ \\__,_|\\___|_|\\\\_\\__,_| .__/         /_/\n' +
      '                                        |_|                \033[0m\n' )




def on_created( event ):
	conso.debug( f'O arquivo "{event.src_path}" foi criado!' )

def on_deleted( event ):
	conso.debug( f'O arquivo "{ event.src_path } foi deletado"!' )

def on_modified( event ):
	conso.debug( f'O arquivo "{ event.src_path }" foi modificado.' )

def on_moved( event ):
	conso.debug( f'O arquivo "{ event.src_path }" foi movido para "{ event.dest_path }"' )





if __name__ == '__main__':
	# https://pythonhosted.org/watchdog/api.html#watchdog.events.PatternMatchingEventHandler
	events             = PatternMatchingEventHandler([ '*' ], None, True, True )
	events.on_created  = on_created
	events.on_deleted  = on_deleted
	events.on_modified = on_modified
	events.on_moved    = on_moved
	path               = sys.argv[1] if len( sys.argv ) > 1 else '.'
	observer           = Observer()

	observer.schedule( events, path, recursive = False )
	observer.start()

	try:
		while True:
			time.sleep( 1 )

	except KeyboardInterrupt:
		observer.stop()
		observer.join()
