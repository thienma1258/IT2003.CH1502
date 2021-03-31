from core.module import *


#MARK: - Tiny Preset
# Tiny Topology (Example Network 1)
# Network with 4 switches,1 controller, with 5 bidirectional links.
#
# One-directional links (10):
#   s1 <-> (s2, s3, s4)
#   s2 <-> (s1, s4)
#   s3 <-> (s1, s4)
#   s4 <-> (s1, s2, s3)
#
# Link costs:
#   s1-s2:  6
#   s1-s3:  1
#   s1-s4:  2
#   s2-s4:  3
#   s3-s4:  3
class TinyTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	info = 'simple network with 4 switches and 5 links'
	
	def build( self ):
		switches = 4
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 6), ((1, 3), 1), ((1, 4), 2),
			((2, 4), 3),
			((3, 4), 3)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )



#MARK: - Tiny Preset
# Small network with some switch is hard to reach(Example Network 1)
# Network with 4 switches,1 controller, with 5 bidirectional links.
#
# One-directional links (10):
#   s1 <-> (s2, s3, s4)
#   s2 <-> (s1, s4)
#   s3 <-> (s1, s4)
#   s4 <-> (s1, s2, s3)
#
# Link costs:
#   s1-s2:  6
#   s1-s3:  1
#   s1-s4:  2
#   s2-s4:  3
#   s3-s4:  3
class TinyTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	info = 'simple network with 4 switches and 5 links'
	
	def build( self ):
		switches = 4
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 6), ((1, 3), 1), ((1, 4), 2),
			((2, 4), 3),
			((3, 4), 3)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )