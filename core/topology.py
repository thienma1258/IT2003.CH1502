from mininet.topo import Topo
import __builtin__
from mininet.util import irange


# defined raw link with weight between 2 nodes(2 switches) in production could modify to n different factor but in this case just use weight for dijkstra
class RawWeightedLink( __builtin__.object ):
	def __init__( self, nodes, weight ):
		(self.src, self.dst) = nodes
		self.nodes = nodes
		self.weight = weight
	
	def nodes( self ):
		return ( self.src, self.dst )
	
	def toString( self ):
		return '((%s, %s), %s)' % (self.src, self.dst, self.weight)


# A weighted link
def wlink( nodes, weight ):
	return RawWeightedLink( nodes, weight )

# List of weighted links
def wlinks( *wlinkList ):
	return [ wlink(n, w)
		for (n, w) in wlinkList ]

class SuperTopo( Topo ):
	displayName = '< Super >'
	info = '< SuperClass >'
	# Build the topology
	def build( self, n, k, *_args, **_kwargs ):
		Topo.build( self, _args, _kwargs )
		self.n = n
		self.k = k
	# Description
	def shortDescription( self ):
		return self.info
	def longDescription( self ):
		return (( 'Topology Name: %s.\n' % self.displayName ) +
			( 'Total number of switches: %s\n' % self.nSwitches() ) +
			( '                   hosts: %s\n' % self.nHosts() ) +
			( '  switch-to-switch links: %s (each link has a weight)\n' % len(self._slinks) ) +
			(  '    switch-to-host links: %s (no weights)\n' % len(self._hlinks) ))
	# Number of nodes
	def nHosts( self ):
		return len( self.hosts() )
	def nSwitches( self ):
		return len( self.switches() )
	def nLinks( self ):
		return len(self._slinks) + len(self._hlinks)
	#MARK: DEBUG
	# Link input at start
	def printLinkInput( self, _wlinks ):
		print('Printing links weights for input:')
		for w in _wlinks:
			print('\t' + w.toString())
		self.printLinkCosts( _wlinks )
	# Created links at end
	def printLinkCosts( self, _wlinks ):
		print('\n')
		for weightedLink in _wlinks:
			(i, j) = weightedLink.nodes
			w = weightedLink.weight
			print('\tCost of link (s%s <-> s%s): %s' % (i, j, w))
		print('\n\n')
	def debugLinks( self, _wlinks ):
		self.printLinkInput( _wlinks )
		self.printLinkCosts( _hlinks )

#MARK: - Link Topology
# LinkTopo is a base topology with weighted links depend on the rule .
#   n:      swtiches
#   k:      hosts per every switch
#  _wlinks: weighted links from every switch to its
#           directly connected switches
class LinkTopo( SuperTopo ):
	displayName = '< Link >'
	info = '< BaseClass >'
	problemLink = ('s1', 's2')
	
	def build( self, n, k, _wlinks, *_args, **_kwargs ):
		#MARK: Switches
		# Get switch by index: s(1) = <Switch s1>
		def s( index ):
			return self.switches()[index - 1]
		# Create n switches
		def addSwitches():
			return [ self.addSwitch( 's%s' % i )
				for i in irange( 1, n ) ]
		# Create all links between switches (with cost)
		def addSwitchLinks():
			switchLinks = []
			for weightedLink in _wlinks:
				(i, j) = weightedLink.nodes
				w = weightedLink.weight
				switchLinks.append( self.addLink(s(i), s(j), key = (i, j, w)) )
			return switchLinks
		#MARK: Hosts
		# Get host by index: h(1) = <Host h1>
		def h( index ):
			return self.hosts()[index - 1]
		# Create (n * k) hosts
		def addHosts():
			h = n * k
			return [ self.addHost( 'h%s' % i )
				for i in irange( 1, h ) ]
		# Create k links from each host to connected switch (no cost)
		def addHostLinks():
			hostLinks = []
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					hostLinks.append( self.addLink( s(i), h(j), key = ( i, j, 0 ) ) )
			return hostLinks
		# Add all nodes and links
		SuperTopo.build( self, n, k, _args, _kwargs )
		addSwitches()
		self._slinks = addSwitchLinks()
		addHosts()
		self._hlinks = addHostLinks()
