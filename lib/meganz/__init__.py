import re
import random
import os.path
import logging
import requests

from Crypto.Cipher import AES
from Crypto.Util   import Counter
from datetime      import datetime

# https://github.com/odwyersoftware/mega.py
from mega          import Mega
from mega.crypto   import (
	a32_to_base64,
	encrypt_key,
	base64_url_encode,
	encrypt_attr,
	a32_to_str,
	get_chunks,
	str_to_a32,
	makebyte
)



logger = logging.getLogger( __name__ )

# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
# def pretty_size( size, precision = 2 ):
# 	suffixes    = [ 'B', 'KB', 'MB', 'GB', 'TB' ]
# 	suffixIndex = 0

# 	while size > 1024 and suffixIndex < 4:
# 		suffixIndex += 1             # increment the index of the suffix
# 		size         = size / 1024.0 # apply the division

# 	return "%.*f%s"%( precision, size, suffixes[ suffixIndex ])






###
  # Class Mega Extends
  # Adding functions and improving some existing ones
  # https://github.com/MiyakoYakota/MegaPy
###
class meganz( Mega ):

	def __file_extends( self, item ) -> dict:
		return {
			'id'      : item[0],
			'name'    : item[1][ 'a' ][ 'n' ],
			'excluded': self._trash_folder_node_id == item[1][ 'p' ],
			'isfolder': True if item[1][ 't' ] else False,
			'date'    : datetime.fromtimestamp( item[1][ 'ts' ] ).strftime( '%d/%m/%Y' ),
			'base'    : item
		}



	###
		# Create an instance of Mega.py
		#   meganz()
		#
		# Create an instance of Mega.py and Login to Mega
		#   meganz( email, passwd )
	###
	def __init__( self, email: str = '', passwd: str = '' ):
		# init Mega class
		super().__init__()

		# clone method
		self.orig_find   = getattr( self, 'find' )
		self.orig_upload = getattr( self, 'upload' )


		if email and passwd:
			usr = self.login( email, passwd )




	###
		# Find experts
		#   Returns tuple if it finds all files and returns None if it finds nothing.
		#   The result is modified for better readability and the original result is put into the "base" key
		#   If you want to use the Class default function, use orig_find()
		#
		# mega.find( 'myfile.txt' )
		# mega.find( regex = r'myfile*' )
	##
	def find( self, filename: str = '', regex: str = '', exclude_deleted: bool = False, readability: bool = True ) -> list | None:
		array = []
		files = self.get_files()

		for file in list( files.items() ):
			# ignore excluded
			if ( exclude_deleted and self._trash_folder_node_id == file[1][ 'p' ]):
					continue

			if ( file[1][ 'a' ]):
				# find with regex
				if regex and re.search( regex, file[1][ 'a' ][ 'n' ] ):
					file = self.__file_extends( file )
					array.append( file )

				# find with filename
				elif filename and file[1][ 'a' ][ 'n' ] == filename:
					file = self.__file_extends( file )
					array.append( file )


		return None if len( array ) == 0 else array




	###
	  # Adição de callback para acompanhar o envio.
	  # https://github.com/odwyersoftware/mega.py/blob/0823f39b500034c0725bc0ebc3ebde905e477e67/src/mega/mega.py#L748
	###
	def upload( self, filename: str, dest = None, dest_filename = None, callback = None, timeout: int = 220 ):
		# determine storage node
		if dest is None:
			# if none set, upload to cloud drive node
			if not hasattr( self, 'root_id' ):
				self.get_files()
			dest = self.root_id

		# request upload url, call 'u' method
		with open( filename, 'rb' ) as input_file:
			file_size = os.path.getsize( filename )
			ul_url = self._api_request({ 'a': 'u', 's': file_size })[ 'p' ]

			# generate random aes key (128) for file
			ul_key = [ random.randint( 0, 0xFFFFFFFF ) for _ in range(6) ]
			k_str  = a32_to_str( ul_key[:4] )
			count  = Counter.new( 128, initial_value = (( ul_key[4] << 32 ) + ul_key[5] ) << 64 )
			aes    = AES.new( k_str, AES.MODE_CTR, counter = count )

			upload_progress        = 0
			completion_file_handle = None

			mac_str       = '\0' * 16
			mac_encryptor = AES.new( k_str, AES.MODE_CBC, mac_str.encode( 'utf8' ))
			iv_str        = a32_to_str([ ul_key[4], ul_key[5], ul_key[4], ul_key[5] ])

			if file_size > 0:
				for chunk_start, chunk_size in get_chunks( file_size ):
					chunk            = input_file.read( chunk_size )
					upload_progress += len( chunk )
					encryptor        = AES.new( k_str, AES.MODE_CBC, iv_str )

					for i in range( 0, len( chunk ) - 16, 16 ):
						block = chunk[ i:i + 16 ]
						encryptor.encrypt( block )

					# fix for files under 16 bytes failing
					if file_size > 16:
						i += 16
					else:
						i = 0

					block = chunk[ i:i + 16 ]
					if len( block ) % 16:
						block += makebyte( '\0' * ( 16 - len( block ) % 16 ))
					mac_str = mac_encryptor.encrypt( encryptor.encrypt( block ))

					# encrypt file and upload
					# https://stackoverflow.com/questions/46188295/python-httpconnectionpool-failed-to-establish-a-new-connection-errno-11004-ge
					chunk                  = aes.encrypt( chunk )
					output_file            = requests.post( ul_url + '/' + str( chunk_start ), data = chunk, timeout = timeout )
					completion_file_handle = output_file.text
					logger.info( '%s of %s uploaded', upload_progress, file_size )

					if callback:
						callback( self, upload_progress, file_size )
						# print( f'{ upload_progress } of { file_size } uploaded' )

			else:
				output_file            = requests.post( ul_url + "/0", data = '', timeout = timeout )
				completion_file_handle = output_file.text

			logger.info( 'Chunks uploaded' )
			logger.info( 'Setting attributes to complete upload' )
			logger.info( 'Computing attributes' )
			file_mac = str_to_a32( mac_str )

			# determine meta mac
			meta_mac = ( file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3] )

			dest_filename = dest_filename or os.path.basename( filename )
			attribs       = { 'n': dest_filename }

			encrypt_attribs = base64_url_encode( encrypt_attr( attribs, ul_key[:4] ))
			key             = [
				ul_key[0] ^ ul_key[4], ul_key[1] ^ ul_key[5],
				ul_key[2] ^ meta_mac[0], ul_key[3] ^ meta_mac[1], ul_key[4],
				ul_key[5], meta_mac[0], meta_mac[1]
			]

			encrypted_key = a32_to_base64( encrypt_key( key, self.master_key ))
			logger.info( 'Sending request to update attributes' )

			# update attributes
			data = self._api_request({
				'a': 'p',
				't': dest,
				'i': self.request_id,
				'n': [{
					'h': completion_file_handle,
					't': 0,
					'a': encrypt_attribs,
					'k': encrypted_key
				}]
			})

			logger.info( 'Upload complete' )
			return data