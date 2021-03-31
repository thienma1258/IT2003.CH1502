from mininet.clean import cleanup
from mininet.util import irange

from log import log
from cli import (  TestNetEnvCLI )
from net_launcher import (TestNetLauncher)
from utils import (  TestNetSelectionGroup,
							  parser, display )

# OpenFlow flow tables
# Provides interface to start networks, control,
#   and test simulated networks
class TestNetEnvironment:
	def __init__( self ):
		self.launcher = TestNetLauncher()
		# self.presetTopologies = defaultPresetGroup()
	
	# Remove previous mininet data
	def clean( self ):
		cleanup()
		log.infoln('Cleaned up old files')
	
	# Update Routing Tables
	def updateRoutes( self, lsAlgorithm, switches, linkWeights ):
		
		display.section("Adding Flow table entries...")
		log.infoln('Switch\t Protocols\t Dst-Address\t Actions')
		log.infoln('-------------------------------------------------------')
		weights = [ ( 's'+str(i[0]), 's'+str(i[1]), i[2] )
			for i in linkWeights ]
		# For each switch
		for sourceSwitch in switches:
			routes = lsAlgorithm( sourceSwitch, weights )
			# Compute the least cost route for each destination
			for route in routes:
				# Least cost paths to destinations
				dstSwitch = last(route)
				dstHost = 'h%s' % dstSwitch[1:]
				dstAddress = self.IP(dstHost)
				## Switches to the connected host flows
				srcHost = 'h%s' % sourceSwitch[1:]
				srcAddress = self.IP(srcHost)
				(iPort, oPort) = self.connectionPorts( srcHost, sourceSwitch )
				log.debugln('Source:', (sourceSwitch, srcHost, srcAddress, oPort))
				log.debugln('Destination', (dstSwitch, dstHost, dstAddress, oPort))
				self.flows.add( sourceSwitch, srcAddress, oPort )
				## Switches to switches flows
				prev = sourceSwitch
				for i in range( 1, len(route) ):
					current = route[i]
					(iPort, oPort) = self.connectionPorts( prev, current )
					self.flows.add( prev, dstAddress, iPort )
					prev = current
	
	
	
	# Node instances
	def getNode( self, name ):
		return self.net.nameToNode[name]
	
	def getNodes( self, *names ):
		return [ self.net.nameToNode[name]
			for name in names ]
	
	def IP( self, name ):
		node = self.getNode( name )
		if (node is None):
			return None
		return node.IP()
	
	# Output port from node with name1
	def connectionPorts( self, name1, name2 ):
		node1 = self.getNode( name1 )
		node2 = self.getNode( name2 )
		conn = node1.connectionsTo( node2 )
		if (len(conn) == 0):
			return ( None, None )
		(intf1, intf2) = conn[0]
		return ( intf1.node.ports[intf1], intf2.node.ports[intf2] )
		
	
	# Initialize network and flow tables
	def prepare( self, preset ):
		self.net = self.launcher.prepareNetwork( preset )
		self.launcher.reassignAddresses( self.net )
		self.flows = TestNetEnvironment.FlowTableManager( self.net.controllers[0] )
		
	# Start simulation
	def start( self ):
		self.launcher.startNetwork( self.net )
	
	# Stop simulation
	def stop( self ):
		self.launcher.stopNetwork( self.net )
	
	# Interact
	def startCLI( self ):
		self.CLI = TestNetEnvCLI( self.net, self )
	
	
	
	# OpenFlow
	class FlowTableManager:
		shell = 'sh'
		program = 'sudo ovs-ofctl'
		protocols = ['ARP', 'IP']
		
		def __init__( self, controller ):
			self.controller = controller
		
		def do( self, ofCommand ):
			shCommand = ' '.join( [self.program, ofCommand] )
			return self.controller.cmd( shCommand )
		
		# Display all flows
		def dump( self, switch ):
			return self.do( 'dump-flows %s' % switch )
		
		# Add a new flow
		def add( self, switch, dstAddress, oPort ):
			# Log example: 's1  ARP, IP  192.168.1.1  output:3'
			log.infoln('%s\t\t %s\t %s\t output:%s' % (switch, ', '.join(self.protocols), dstAddress, oPort))
			return [ self.do( 'add-flow %s %s,nw_dst=%s,actions=output:%s' % (switch, protocol.lower(), dstAddress, oPort) )
				for protocol in self.protocols ]
		
		# Delete all flows
		def clear( self, switch ):
			return self.do( 'del-flows %s' % switch )
		
		def size( self, switch ):
			return self.do( 'dump-flows %s | grep "table" -c' % switch )
		
	
	# Two test hosts (h1, h2)
	def getTestHosts( self ):
		return [ self.net.nameToNode[name]
			for name in ['h1', 'h2'] ]
	
	# Testing network
	def nodeReachability( self, n1, n2 ):
		return ( ping(n1, n2), ping(n2, n1) )
	
	# Get the index
	def getNetworkTopologyIndex( self, argv ):
		(min, max) = self.presetTopologies.range()
		default = self.presetTopologies.defaultIndex
		index = default
		if ( parser.validate(argv) ):
			# If arguments are valid, get the index
			index = parser.getIndex( argv )
		else:
			# If network was not chosen on script start,
			#   show the list of preset networks, and
			#   ask to choose one.
			display.networkSelectionMenu( self.presetTopologies )
			display.prompt('Input the index (%s to %s) of a network you want to test: ' % (min, max))
			index = parser.waitForInput()
			# If input is invalid, then choose the first
			#   network in the list (starts at index 1).
			if not ( inRange(index, (min, max)) ) :
				display.error('Index %s is out of range. Resetting index to default.' % (index))
				index = default
		return index
		
	
	# Disable the link between node1 and node2
	def simulateLinkProblem( self, link ):
		(name1, name2) = link
		(node1, node2) = self.getNodes( name1, name2 )
#		link = self.net.link(node1, node2)#[0] #link.stop()
#		log.infoln('Link between nodes %s and %s has been disabled' % (link))
#		return link
