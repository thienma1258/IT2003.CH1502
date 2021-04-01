from core.network_env import TestNetEnvironment
from core.utils import *
from simple_topo import TinyTopo
from core.dijkstra import get_routing_decision #import dijkstra algorthim for routing to update  flows table can use with different algorthim different factor
import sys

# env = TestNetEnvironment()
# display.section("Cleaning up...")
# env.clean()


def __wait__(*commandList):
    steps = len(commandList)
    for i in range(steps):
        commandList[i]()
        display.prompt('\n\nPress <Return> to continue')
        try:
            x = input('')
        except:
            x = ''


# Run the demonstration
def __run__(argc, *argv):

    # MARK: - Select Network Topology
    # 1. Create environment for creating, running, and testing
    #    network simulations from presets
    env = TestNetEnvironment(TinyTopo)
    display.section("Cleaning up...")
    env.clean()
    selectedTopoPreset = env.presetTopologies
    display.message('choose topology %s ' %
                    (selectedTopoPreset.displayName))

    # MARK: - Begin Network Simulation and do the First Test
    # 4. Initialize a new network with selected topology
    display.section("Starting network with topology preset")
    env.prepare(selectedTopoPreset)
    env.start()
    # 5. Launch the network
    display.section("Starting Configuration Interface")
    display.prompt('Input commands (optional):\n' +
                   ' (E.g., track packets with \'sudo wireshark &\', \'tcpdump\', etc.)\n' +
                   ' When you are ready to start the simulation tests, type \'exit\' or press CTRL-D.\n')
    env.startCLI()

    # 6. Test 1: Destination Host Unreachable
    display.section("Running tests...")
    (host1, host2) = env.getTestHosts()

    def do_test_1():
        test1 = env.nodeReachability(host1, host2)
        display.section("Test 1: Hosts are unreachable...")
        display.highlight(test1)
    __wait__(do_test_1)
    # 7. Get the switches and link weights
    switches = env.net.topo.switches()
    linkWeights = env.net.topo._slinks
    # 8. Run dijkstra algorthim update flow table 
    env.updateRoutes( get_routing_decision, switches, linkWeights )
    env.startCLI()

    def do_test_2():
    # 10. Test 2: Established connectivity
    	display.section("Test 2: Hosts are now connected...")
    	test2 = env.nodeReachability( host1, host2 )
    	display.highlight(test2)
    __wait__(do_test_2)
    env.startCLI()

    #MARK: - Disable one of the Links and do the Third Test
    # 11. Disable a link
    link = env.net.topo.problemLink
    display.section("Changing network conditions")
    display.message('Problem link in this simulation is {%s, %s}' % link )
    env.simulateLinkProblem(link)
    n2 = int( link[0][1:] )
    n4 = int( link[1][1:] )
    for (prev1, prev2, w) in linkWeights:
    	if ((prev1 == n2 and prev2 == n4) or (prev1 == n4 and prev2 == n2)):
    		linkWeights.remove( (prev1, prev2, w) )
    		break


    env.updateRoutes( get_routing_decision, switches, linkWeights )

    def do_test_3():
    	display.section("Test 3: Link recompute after link from s4->s2 is fail.")
    	test3 = env.nodeReachability( host1, host2 )
    	display.highlight(test3)
    __wait__(do_test_3)

    env.startCLI()
   #MARK: - Disable one of the Links and do the Third Test
    # 11. Disable a link
    link = env.net.topo.problemLink
    display.section("Changing network conditions")
    display.message('Problem link in this simulation is {%s, %s}' % link )
    env.simulateLinkProblem(link)
    n2 = int( link[0][1:] )
    n4 = int( link[1][1:] )
    for (prev1, prev2, w) in linkWeights:
    	if ((prev1 == n2 and prev2 == n4) or (prev1 == n4 and prev2 == n4)):
    		linkWeights.remove( (prev1, prev2, w) )
    		break
    # 12. Test 3: Hosts
    def do_test_3():
    	display.section("Test 3: Link failure affects optimal routes...")
    	test3 = env.nodeReachability( host1, host2 )
    	display.highlight(test3)
    __wait__(do_test_3)

    link2 = env.net.topo.increaseCostLink
    n1 = int( link2[0][1:] )
    n2 = int( link2[1][1:] )
    for (prev1, prev2, w) in linkWeights:
    	if ((prev1 == n1 and prev2 == n2) or (prev1 == n2 and prev2 == n1)):
    		linkWeights.remove( (prev1, prev2, w) )
    		break

    linkWeights.append( (str(n1), str(n2), 100) )
    #MARK: - Recompute the Least-Cost Paths and do the Fourth Test
    # when cost or weight of each switch is increase  between node 2 and node 4 is 100
    # 13.
    env.updateRoutes( get_routing_decision, switches, linkWeights )
    # 14. Test 4:
    def do_test_4():
    	display.section("Test 4: routing from h1 to h2 change afte increase s2->s4 :100 ")
    	test4 = env.nodeReachability(host1, host2)
    	display.highlight(test4)
    __wait__(do_test_4)

    #MARK: - Command Line Interface
    # 15. Start the CLI to run other tests
    display.section("Starting Command Line Interface")
    env.startCLI()

    # MARK: - Stop Network Simulation
    # 15. Stop network
    display.section("Shutting down")
    env.stop()


if __name__ == '__main__':
    argc = len(sys.argv)
    __run__(argc, sys.argv)
