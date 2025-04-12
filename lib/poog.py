# -*- coding: utf-8 -*

###
  # poog: Print, cOnsOle, loG
  # Autor: F4Jonatas
  # Version: 1.1.4

  # Inprations/Credtis
  #    https://github.com/rxi/log.lua
  #    https://github.com/Delgan/loguru
  #    https://github.com/hynek/structlog
  #    https://github.com/Textualize/rich
###



'''
import re
import os.path

from datetime import datetime





class cor:
	@staticmethod
	def extract( color ):
		tipo = type( color )

		if tipo == 3:
			return (
				str( color[0] ),
				str( color[1] ),
				str( color[2] )
			)

		elif tipo == str:
			if re.search( r'^(\s*#)', color ):
				return cor.hex2rgb( color )



	@staticmethod
	def hex2rgb( color ):
		color = color.lstrip( '#' )
		lv = len( color )
		color = tuple( int( color[ i:i + lv // 3 ], 16 ) for i in range( 0, lv, lv // 3 ))

		return (
			str( color[0] ),
			str( color[1] ),
			str( color[2] )
		)



# https://askubuntu.com/questions/528928/how-to-do-underline-bold-italic-strikethrough-color-background-and-size-i
# https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
# https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has
# https://mathspp.com/blog/til/043
# https://dmitrygolovach.com/python-logging/
###
  # Printing Template
  # suports RGB and Hexadecimal colors
  # Returns the simple string that gives the possibility to create a log
  #
  # printt(
  #  template [string/required]  Text template to print.
  #  sep      [string/optional]  Printed between objects. Default: " ".
  #  end      [string/optional]  Appended to the end of the statement. Default: "\n".
  #  file     [object/optional]  An object with write(string) method. Default: sys.stdout.
  #  flush    [boolean/optional] (Py >= 3.3) Default: False.
  # )
  #
  # Text Color: use color or c
  # printt( '<%color:#ff5555 Any Message%>' )
  #
  # Back Color: use fill or f
  # printt( '<%fill:56,56,56 Any Message%>' )
  #
  # Bold Style: use bold or b
  # Sometimes it can't be used and will be ignored
  # printt( '<%bold Any Message%>' )
  #
  # Italic Style: use italic or i
  # printt( '<%italic Any Message%>' )
  #
  # Dim Style: use dim or d
  # printt( '<%dim Any Message%>' )
  #
  # Underline Style: use underline or u
  # printt( '<%underline Any Message%>' )
  #
  # ANSI Escape Code: use @
  # printt( '<%@0;32 Any Message%>' )
  #
  # Any attribute can be combined with "-" except the ANSI escape code
  # printt( '<%u-i-f:56,56,56-c:#ff5555 Any Message%>' )
###
def printt( template: str, **args ) -> str:
	template = re.sub( '%>', chr(0), template )
	result   = template
	string   = ''


	# prepare regex
	match     = re.compile( r'(<\s*%\s*)([^\x00]*)(\x00)' )
	color     = re.compile( r'(?i)-?\b(c(olor)?\s*:\s*((#[a-f\d]+)|(\d+,\d+,\d+)))\b-?\s*' )
	fill      = re.compile( r'(?i)-?\b(f(ill)?\s*:\s*((#[a-f\d]+)|(\d+,\d+,\d+)))\b-?\s*' )
	italic    = re.compile( r'(?i)-?\b(i(talic)?)-?\s?' )
	underline = re.compile( r'(?i)-?\b(u(nderline)?)-?\s?' )
	strong    = re.compile( r'(?i)-?\b(b(old)?)-?\s?' )
	dimmy     = re.compile( r'(?i)-?\b(d(im)?)-?\s?' )
	codec     = re.compile( r'\B(@\s*([\d;]+))\s?' )

	# loop in template groups
	for find in re.finditer( match, template ):
		text  = find.group(2)
		fore  = re.search( color    , text )
		back  = re.search( fill     , text )
		talic = re.search( italic   , text )
		uline = re.search( underline, text )
		bold  = re.search( strong   , text )
		dim   = re.search( dimmy    , text )
		code  = re.search( codec    , text )

		if code:
			string = re.sub( f'(<\\s*%\\s*){ code.group(0) }\\s?', '', string if string else template )
			result = re.sub(
				r'(<\s*%\s*)?' + code.group(0) + r'\s?',
				f'\033[{ code.group(2) }m',
				result
			)


		else:
			if fore:
				# hex color
				if fore.group(4):
					string = re.sub( f'(<\\s*%\\s*)?{ fore.group(0) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*)?{ fore.group(1) }-?\\s*',
						'\033[38;2;{0[0]};{0[1]};{0[2]}m'.format( cor.hex2rgb( fore.group(4) )),
						result
					)

				# rgb color
				elif fore.group(5):
					string = re.sub( f'(<\\s*%\\s*)?{ fore.group(0) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*)?{ fore.group(1) }-?\\s*',
						'\033[38;2;{0[0]};{0[1]};{0[2]}m'.format( fore.group(5).split( ',' )),
						result
					)


			if back:
				# hex color
				if back.group(4):
					string = re.sub( f'(<\\s*%\\s*)?{ back.group(1) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*)?{ back.group(1) }-?\\s*',
						'\033[48;2;{0[0]};{0[1]};{0[2]}m'.format( cor.extract( back.group(4) )),
						result
					)

				# rgb color
				elif back.group(5):
					string = re.sub( f'(<\\s*%\\s*)?{ back.group(1) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*)?{ back.group(1) }-?\\s*',
						'\033[48;2;{0[0]};{0[1]};{0[2]}m'.format( back.group(5).split( ',' )),
						result
					)


			if bold:
				string = re.sub( f'(<\\s*%\\s*)?{ bold.group(1) }-?\\s*', '', string if string else template )
				result = re.sub( f'(<\\s*%\\s*)?{ bold.group(1) }-?\\s*', '\033[1m', result )

			if dim:
				string = re.sub( f'(<\\s*%\\s*)?{ dim.group(1) }-?\\s*', '', string if string else template )
				result = re.sub( f'(<\\s*%\\s*)?{ dim.group(1) }-?\\s*', '\033[2m', result )

			if talic:
				string = re.sub( f'(<\\s*%\\s*)?{ talic.group(1) }-?\\s*', '', string if string else template )
				result = re.sub( f'(<\\s*%\\s*)?{ talic.group(1) }-?\\s*', '\033[3m', result )

			if uline:
				string = re.sub( f'(<\\s*%\\s*)?{ uline.group(1) }-?\\s*', '', string if string else template )
				result = re.sub( f'(<\\s*%\\s*)?{ uline.group(1) }-?\\s*', '\033[4m', result )



		# clear templete
		result = re.sub( r'\s*\x00', r'\033[0m', result )

	print( result, **args )
	return re.sub( r'\s*\x00', '', string )




###
  # Class conso
###
class conso:
	# methotd: return current time
	tick  = lambda: datetime.now().strftime( '%d-%m-%Y %H:%M:%S.%f' )[:-3]


	def __init__( self, log = None ):
		self.log   = log
		self.tick  = conso.tick


	def error( self, msg ):
		inner = printt( f'<%@0;31 [ERROR { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def info( self, msg ):
		inner = printt( f'<%@0;32 [INFO  { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def warn( self, msg ):
		inner = printt( f'<%@0;33 [WARN  { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def trace( self, msg ):
		inner = printt( f'<%@0;34 [TRACE { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def fatal( self, msg ):
		inner = printt( f'<%@0;35 [FATAL { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )

	def debug( self, msg ):
		inner = printt( f'<%@0;36 [DEBUG { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def print( self, msg ):
		inner = printt( msg )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )




	class group:
		def __init__( self, inner: str, tab: int = 0, log = None ):
			self._inner = inner
			self.tab    = tab
			self.log    = log


		def repeat( self, word: str, length: int ) -> str:
			result = ''

			for i in range( length ):
				result = result + word

			return result



		def print( self, msg: str, prefix: str = '├', tab: int = 0 ):
			tab = tab if tab > 0 else self.tab
			if tab > 0:
				tab = self.repeat( '   ', tab )
			else:
				tab = ''

			return conso.group( printt( f'{ tab }{ prefix }  { msg }', log = self.log ))



		def close( self, msg: str, prefix: str = '└─', tab: int = 0 ):
			tab = tab if tab > 0 else self.tab
			if tab > 0:
				tab    = self.repeat( '│  ', tab )
			else:
				tab = ''

			return printt( f'{ tab }{ prefix } { msg }' )
			# self.tab += 1






class logg:
	def __init__( self, filepath: str = 'logg.log' ):
		self.file = open( filepath, 'a' )


	def close( self ):
		self.file.close()


	def append( self, txt: str ):
		self.file.write( txt + '\n' )



	def error( self, msg: str ):
		self.append( f'[ERROR { conso.tick() }] { msg }' )


	def info( self, msg: str ):
		self.append( f'[INFO  { conso.tick() }] { msg }' )


	def warn( self, msg: str ):
		self.append( f'[WARN  { conso.tick() }] { msg }' )


	def trace( self, msg: str ):
		self.append( f'[TRACE { conso.tick() }] { msg }' )


	def fatal( self, msg: str ):
		self.append( f'[FATAL { conso.tick() }] { msg }' )


	def debug( self, msg: str ):
		self.append( f'[DEBUG { conso.tick() }] { msg }' )






# Testes

# log = logg()
# log.append( printt( f'<%@0;33 [WARN  { conso.tick() }]%> Teste war' ))
# log.warn( 'Teste warn' )
'''



# -*- coding: utf-8 -*

###
  # poog: Print, cOnsOle, loG
  # Autor: F4Jonatas
  # Version: 1.1.4

  # Inprations/Credtis
  #    https://github.com/rxi/log.lua
  #    https://github.com/Delgan/loguru
  #    https://github.com/hynek/structlog
  #    https://github.com/Textualize/rich
###




import re
import os.path

from datetime import datetime





class cor:
	@staticmethod
	def extract( color ):
		tipo = type( color )

		if tipo == 3:
			return (
				str( color[0] ),
				str( color[1] ),
				str( color[2] )
			)

		elif tipo == str:
			if re.search( r'^(\s*#)', color ):
				return cor.hex2rgb( color )



	@staticmethod
	def hex2rgb( color ):
		color = color.lstrip( '#' )
		lv = len( color )
		color = tuple( int( color[ i:i + lv // 3 ], 16 ) for i in range( 0, lv, lv // 3 ))

		return (
			str( color[0] ),
			str( color[1] ),
			str( color[2] )
		)



# https://askubuntu.com/questions/528928/how-to-do-underline-bold-italic-strikethrough-color-background-and-size-i
# https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
# https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has
# https://mathspp.com/blog/til/043
# https://dmitrygolovach.com/python-logging/
##
 # Printing Template
 # suports RGB and Hexadecimal colors
 # Returns the simple string that gives the possibility to create a log
 #
 # printt(
 #  template [string/required]  Text template to print.
 #  sep      [string/optional]  Printed between objects. Default: " ".
 #  end      [string/optional]  Appended to the end of the statement. Default: "\n".
 #  file     [object/optional]  An object with write(string) method. Default: sys.stdout.
 #  flush    [boolean/optional] (Py >= 3.3) Default: False.
 # )
 #
 # Text Color: use color or c
 # printt( '<%color:#ff5555 Any Message%>' )
 #
 # Back Color: use fill or f
 # printt( '<%fill:56,56,56 Any Message%>' )
 #
 # Bold Style: use bold or b
 # Sometimes it can't be used and will be ignored
 # printt( '<%bold Any Message%>' )
 #
 # Italic Style: use italic or i
 # printt( '<%italic Any Message%>' )
 #
 # Dim Style: use dim or d
 # printt( '<%dim Any Message%>' )
 #
 # Underline Style: use underline or u
 # printt( '<%underline Any Message%>' )
 #
 # ANSI Escape Code: use @
 # printt( '<%@0;32 Any Message%>' )
 #
 # Any attribute can be combined with "-" except the ANSI escape code
 # printt( '<%u-i-f:56,56,56-c:#ff5555 Any Message%>' )
##



# prepare regex
match     = re.compile( r'(<\s*%\s*[^\x00]*)(\x00)' )
color     = re.compile( r'(?i)-?(?<=%)\s*(c(olor)?\s*:\s*((#[a-f\d]+)|(\d+,\d+,\d+)))\b-?\s*' )
fill      = re.compile( r'(?i)-?(?<=%)\s*(f(ill)?\s*:\s*((#[a-f\d]+)|(\d+,\d+,\d+)))\b-?\s*' )
italic    = re.compile( r'(?i)-?(?<=%)\s*(i(talic)?)-?\s?' )
underline = re.compile( r'(?i)-?(?<=%)\s*(u(nderline)?)-?\s?' )
strong    = re.compile( r'(?i)-?(?<=%)\s*(b(old)?)-?\s?' )
dimmy     = re.compile( r'(?i)-?(?<=%)\s*(d(im)?)-?\s?' )
codec     = re.compile( r'\B(@\s*([\d;]+))\s?' )
keys      = re.compile( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*' )


sub      = '(<\\s*%\\s*)(u(nderline)?-?)?{}-?\\s*'



def printt( template: str, **args ) -> str:
	template = re.sub( '%>', chr(0), template )
	result   = template
	string   = ''


	# loop in template groups
	for find in re.finditer( match, template ):
		text  = find.group(1)
		cmd   = re.search( keys   , text )
		fore  = re.search( color    , text )
		back  = re.search( fill     , text )
		dim   = re.search( dimmy    , text )
		code  = re.search( codec    , text )
		print( 'text::', text, "'"+ find.group(1) +"'" )
		print( 'find::', find )
		print( 'cmd::' , cmd )

		if code:
			string = re.sub( f'(<\\s*%\\s*){ code.group(0) }\\s?', '', string if string else template )
			result = re.sub(
				r'(<\s*%\s*)?' + code.group(0) + r'\s?',
				f'\033[{ code.group(2) }m',
				result
			)


		else:
			if fore:
				# hex color
				if fore.group(4):
					string = re.sub( f'(<\\s*%\\s*){ fore.group(0) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*){ fore.group(1) }-?\\s*',
						'\033[38;2;{0[0]};{0[1]};{0[2]}m'.format( cor.hex2rgb( fore.group(4) )),
						result
					)

				# rgb color
				elif fore.group(5):
					string = re.sub( f'(<\\s*%\\s*){ fore.group(0) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*){ fore.group(1) }-?\\s*',
						'\033[38;2;{0[0]};{0[1]};{0[2]}m'.format( fore.group(5).split( ',' )),
						result
					)


			if back:
				# hex color
				if back.group(4):
					string = re.sub( f'(<\\s*%\\s*){ back.group(1) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*){ back.group(1) }-?\\s*',
						'\033[48;2;{0[0]};{0[1]};{0[2]}m'.format( cor.extract( back.group(4) )),
						result
					)

				# rgb color
				elif back.group(5):
					string = re.sub( f'(<\\s*%\\s*){ back.group(1) }-?\\s*', '', string if string else template )
					result = re.sub(
						f'(<\\s*%\\s*){ back.group(1) }-?\\s*',
						'\033[48;2;{0[0]};{0[1]};{0[2]}m'.format( back.group(5).split( ',' )),
						result
					)


			bold = re.search( r'(?i)-?b(old)?', cmd.group(0) )
			if bold:
				string = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*-?\s*(b(old)?)\s*-?\s*([italcundermbol-]*)', r'\1\3', string if string else template )
				result = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*-?\s*(b(old)?)\s*-?\s*([italcundermbol-]*)', r'\1\3\033[1m', result )

			if dim:
				string = re.sub( f'(<\\s*%\\s*){ dim.group(1) }-?\\s*', '', string if string else template )
				result = re.sub( f'(<\\s*%\\s*){ dim.group(1) }-?\\s*', '\033[2m', result )

			talic = re.search( r'(?i)-?\s*i(talic)?', cmd.group(0) )
			if talic:
				string = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*-?\s*(i(talic)?)\s*-?\s*([italcundermbol-]*)', r'\1\3', string if string else template )
				result = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*-?\s*(i(talic)?)\s*-?\s*([italcundermbol-]*)', r'\1\3\033[3m', result )
				print(result)

			uline = re.search( r'(?i)-?\s*u(nderline)?', cmd.group(0) )
			if uline:
				string = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*', r'', string if string else template )
				result = re.sub( r'(?i)(?<=%)\s*([italcundermbol-]*)\s*', r'\033[4m', result )



		# clear templete
		result = re.sub( r'\s*\x00', '\033[0m', result )
		string = re.sub( r'\s*\x00', '', string )
		result = re.sub( r'<\s*%-*', '', result )
		string = re.sub( r'<\s*%-*', '', string )

	print( result, **args )
	return string




##
 # Class conso
##
class conso:
	# methotd: return current time
	tick  = lambda: datetime.now().strftime( '%d-%m-%Y %H:%M:%S.%f' )[:-3]


	def __init__( self, log = None ):
		self.log   = log
		self.tick  = conso.tick


	def error( self, msg ):
		inner = printt( f'<%@0;31 [ERROR { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def info( self, msg ):
		inner = printt( f'<%@0;32 [INFO  { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def warn( self, msg ):
		inner = printt( f'<%@0;33 [WARN  { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def trace( self, msg ):
		inner = printt( f'<%@0;34 [TRACE { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def fatal( self, msg ):
		inner = printt( f'<%@0;35 [FATAL { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )

	def debug( self, msg ):
		inner = printt( f'<%@0;36 [DEBUG { self.tick() }]%> { msg }' )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )


	def print( self, msg ):
		inner = printt( msg )
		if self.log:
			self.log.append( inner )

		return self.group( inner, log = self.log )




	class group:
		def __init__( self, inner: str, tab: int = 0, log = None ):
			self._inner = inner
			self.tab    = tab
			self.log    = log


		def repeat( self, word: str, length: int ) -> str:
			result = ''

			for i in range( length ):
				result = result + word

			return result



		def print( self, msg: str, prefix: str = '├', tab: int = 0 ):
			tab = tab if tab > 0 else self.tab
			if tab > 0:
				tab = self.repeat( '   ', tab )
			else:
				tab = ''

			return conso.group( printt( f'{ tab }{ prefix }  { msg }', log = self.log ))



		def close( self, msg: str, prefix: str = '└─', tab: int = 0 ):
			tab = tab if tab > 0 else self.tab
			if tab > 0:
				tab    = self.repeat( '│  ', tab )
			else:
				tab = ''

			return printt( f'{ tab }{ prefix } { msg }' )
			# self.tab += 1






class logg:
	__prefix = [
		'[ERROR {}] {}',
		'[INFO  {}] {}',
		'[WARN  {}] {}',
		'[TRACE {}] {}',
		'[FATAL {}] {}',
		'[DEBUG {}] {}'
	]



	def __init__( self, filepath: str = 'logg.log' ):
		self.file = open( filepath, 'a' )


	def close( self ):
		self.file.close()


	def append( self, msg: str ) -> str:
		self.file.write( msg + '\n' )
		return msg


	def error( self, msg: str ) -> str:
		self.append( self.__prefix[0].format( conso.tick(), msg ))
		return msg


	def info( self, msg: str ) -> str:
		self.append( self.__prefix[1].format( conso.tick(), msg ))
		return msg


	def warn( self, msg: str ) -> str:
		self.append( self.__prefix[2].format( conso.tick(), msg ))
		return msg


	def trace( self, msg: str ) -> str:
		self.append( self.__prefix[3].format( conso.tick(), msg ))
		return msg


	def fatal( self, msg: str ) -> str:
		self.append( self.__prefix[4].format( conso.tick(), msg ))
		return msg


	def debug( self, msg: str ) -> str:
		self.append( self.__prefix[5].format( conso.tick(), msg ))
		return msg






# Testes
if __name__ == '__main__':
	print( printt( 'Encontrado: <%u-b-i 14 %> backup\'s' ))
