from core.topology import *

# Tiny Topology (Example Network 1)
# Network with 4 switches,1 controller
#
#
# Link costs:
#   s1-s2:  6
#   s1-s3:  1
#   s1-s4:  2
#   s2-s4:  3
#   s3-s4:  3
#   s3-s2:  5

class TinyTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	info = 'simple network with 4 switches '
	
	def build( self ):
		switches = 4
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 6), ((1, 3), 1), ((1, 4), 2),
			((2, 4), 3),
			((3, 4), 3),
			((3, 2), 5),
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
