
from log import log
from mininet.net import Mininet, MininetWithControlNet
from mininet.node import RemoteController
from mininet.link import Link, TCLink
from mininet.cli import CLI
from mininet.clean import Cleanup
from mininet.util import irange
import sys


# Read script input
class TestNetParser:
	# Maximum number of arguments = 2
	def __init__( self ):
		self._maxArgc = 2
	# Input is valid if 2 arguments are provided (string '*/TestNet*.py' and a number)
	def validate( self, argv ):
		argc = len(argv)
		return ( argc == self._maxArgc )
	
	# Get argument
	## Get by argument index (noexcept)
	def safeGet( self, argv, argIndex, convertor = None ):
		try:
			arg = argv[argIndex]
			if not (convertor is None):
				arg = convertor(arg)
			return arg
		except Exception:
			return ''
	## Name of the executable
	def getFilename( self, argv ):
		return self.safeGet( argv, 0 )
	## Preset index
	def getIndex( self, argv ):
		return int(self.safeGet( argv, 1 ))
	## List of all arguments (noexcept)
	def getAll( self, argv ):
		# Get filename
		name = self.getFilename( argv )
		if ( self.validate( len(argv) ) ):
			# Get index if input is valid
			index = self.getIndex( argv )
			ret = ( name, index )
		else:
			# Otherwise, use default preset index 0
			return ( name, 0 )
		# Log and return both arguments
		return ( name, index )
	
	# Get all input arguments
	def parseInput( self ):
		log.DO("Parse input arguments.")
		argv = sys.argv
		(name, index) = self.getAll( argv )
		log.DONE("Parsed arguments: \n\tname = %s, \n\tpreset index = %s" % (name, index))
		return (name, index)
	
	# Wait for additional input
	def waitForInput( self ):
		try:
			return input()
		except Exception:
			return 0

# Text style
class UITextStyle:
	class Color:						# Regular text color
		black   	 = '\033[0;30m'
		red     	 = '\033[0;31m'
		green   	 = '\033[0;32m'
		yellow  	 = '\033[93m'
		blue    	 = '\033[0;34m'
		magenta 	 = '\033[35m'
		cyan    	 = '\033[0;36m'
		gray    	 = '\033[0;37m'
		lightred     = '\033[91m'
		lightcyan    = '\033[96m'
		red_bold     = '\033[1;31m'
		magenta_bold = '\033[1;35m'
	class BackgroundColor:				# Background color
		black	     = '\033[40m'
		red			 = '\033[41m'
		green		 = '\033[42m'
		orange		 = '\033[43m'
		blue		 = '\033[44m'
		purple		 = '\033[45m'
		cyan		 = '\033[46m'
		lightgrey	 = '\033[47m'
	class Format:
		underline 	 = '\033[0;4m'
		reset 		 = '\033[m'			# Reset color to default


# Convert original string to colored string
def colorize( _str, color ):
	return ( color + _str + UITextStyle.Format.reset )
def colorizeEach( strList, color ):
	ret = [ colorize( _str, color )
		for _str in strList ]
	ret.reverse()
	return ret


# Print colored message and reset color
def printColored( _str, color = UITextStyle.Format.reset ):
	print(color),
	print(_str),
	print(UITextStyle.Format.reset)
def printColoredEach( strList, color ):
	for _str in strList:
		print(color + _str + UITextStyle.Format.reset)


# Colorful title
def displayTitle( content ):
	printColored('< %s >' % content.upper(), UITextStyle.Color.magenta_bold)
# Subtitle
def displaySubtitle( content ):
	printColored(content)
# Body text
def displayText( content , indentLevel = 1 ):
	for _ in range(indentLevel):
		print('\t'),
	print(content)
# Colorful footnote
def displayFootnote( content ):
	printColored(content, UITextStyle.Color.gray)


# Display formatted blocks of text
class TestNetDisplay:
	#
	def section( self, content ):
		print('')
		displayTitle(content)
	#
	def subsection( self, content ):
		hbreak = ' ----- '
		printColored(hbreak + content + hbreak, UITextStyle.Color.magenta)
	# Default message
	def message( self, content ):
		printColored(content)
	# Input prompt
	def prompt( self, content ):
		printColored(content, UITextStyle.Color.magenta)
	# Error message
	def error( self, content ):
		printColored(content, UITextStyle.Color.lightred)
	#
	def note( self, content ):
		displayFootnote(content)
	# Highlighted block
	def highlight( self, block ):
		line = 0
		for n in range( len(block) ):
			printColored([n + 1, block[n]], UITextStyle.Color.yellow)
			print('')
	#
	def cmdHighlight( self, enable ):
		if (enable):
			print(UITextStyle.Color.yellow),
		else:
			print(UITextStyle.Format.reset)
	
	# Selection menu of available networks
	def networkSelectionMenu( self, group ):
		# Display colorized network names
		displaySubtitle('Choose a test network topology preset:')
		for i in range( 1, group.size() + 1 ):
			networkTopology = group.select(i)
			name = colorize( networkTopology.displayName, UITextStyle.Color.lightcyan )
			desc = networkTopology.info
			# Show topology information
			if ( i == group.defaultIndex ):
				name += ' (default)'
			displayText('%s. %s - %s.' % ( i, name, desc ))
		displayFootnote('(See network diagrams in the project definition.)')

class TestNetSelectionGroup:

	# Set main container
	def __init__( self, group, defaultIndex ):
		self._group = group
		self.defaultIndex = defaultIndex
	
	# Get the group of all items
	def items( self ):
		return self._group
	# Select an item by its index
	def select( self, index ):
		return self._group[ ( index - 1 )  % self.size() ]
	
	# Get the group size
	def size( self ):
		return len( self._group )
	def isEmpty( self ):
		return ( self.size() == 0 )
	
	# Selection range
	def min( self ):
		if ( self.isEmpty() ):
			return 0
		return 1
	def max( self ):
		return self.size()
	def range( self ):
		return ( self.min(), self.max() )	

# Shared TestNet instance
display = TestNetDisplay()

# Shared TestNet instance
parser = TestNetParser()
