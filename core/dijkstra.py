
def node_with_least_cost(unvisited_switches_dic):
	cost = float('inf')
	node = ""
	for i in (unvisited_switches_dic):
		if unvisited_switches_dic[i]<cost:
			cost = unvisited_switches_dic[i]
			node = i
	return node


def find_all_other_swtiches( link_and_weight):
	result =[]
	for i in link_and_weight:
		if i[0] not in result:
			result.append(i[0])
		if i[1] not in result:
			result.append(i[1])
	return result


def remove_duplicate(link_and_weight):#('switch1', 'switch2, weight)
	result = []
	for i in range(len(link_and_weight)):
		j = 0
		while 1:
			if j < len(link_and_weight[i][0]) and j< len(link_and_weight[i][1]):
				if link_and_weight[i][0][j]>link_and_weight[i][1][j]:
					if(link_and_weight[i] not in result):
						result.append(link_and_weight[i])
					break
				elif link_and_weight[i][0][j]<link_and_weight[i][1][j]:
					tuple = (link_and_weight[i][1],link_and_weight[i][0],link_and_weight[i][2])
					if tuple not in result:
						result.append(tuple)
					break
				else:
					j = j + 1
			else:# s1 is longer in length
				if len(link_and_weight[i][0]) > len(link_and_weight[i][1]):
					if (link_and_weight[i] not in result):
						result.append(link_and_weight[i])
					break
				else: #s2 is longer in length
					tuple = (link_and_weight[i][1], link_and_weight[i][0], link_and_weight[i][2])
					if tuple not in result:
						result.append(tuple)
					break
	return result






def get_route(start_node,end_node,predecessors):
	temp = []
	if end_node not in predecessors:
#		print(str(start_node)+" --> "+str(end_node)+" node not reachable")
		return []
	pred = predecessors[end_node]

	temp.append(end_node)
	temp.append(pred)
	while pred !=start_node:
			pred = predecessors[pred]
			temp.append(pred)
	temp.reverse()

	return temp

def convert_to_string(link_and_weight):
	result = []
	for i in link_and_weight:
		tuple = (str(i[0]),str(i[1]), i[2])
		result.append(tuple)
	return result

def get_route_cost(routes):
	result = 0 # ""
	global converted_link_and_weight
	for route in routes:
		if route != []:
			cost = 0
			prompt = str(route[0]) + " --> " + str(route[len(route) - 1]) + " cost: "
			for i in range(len(route)-1):
				node1 = route[i]
				node2 = route[i+1]
				for j in converted_link_and_weight:
					if j[0]==node1 and j[1]==node2:
						cost = cost + j[2]
						break
					if j[1]==node1 and j[0]==node2:
						cost = cost + j[2]
						break
			result = cost # result+prompt+str(cost)+'\n'
	return result





# perseudo code
#  1  function Dijkstra(Graph, source):
#  2
#  3      create vertex set Q
#  4
#  5      for each vertex v in Graph:            
#  6          dist[v] <- INFINITY                 
#  7          prev[v] <- UNDEFINED                
#  8          add v to Q                     
#  9      dist[source] <- 0                       
# 10     
# 11      while Q is not empty:
# 12          u <- vertex in Q with min dist[u]   
# 13                                             
# 14          remove u from Q
# 15         
# 16          for each neighbor v of u:           // only v that are still in Q
# 17              alt <- dist[u] + length(u, v)
# 18              if alt <- dist[v]:              
# 19                  dist[v] <- alt
# 20                  prev[v] <- u
# 21
# 22      return dist[], prev[]
## get routing from start node with link and weight tabls


def get_routing_decision(start_node, link_and_weight, end_node = ""):#link_and_weight: (node, node, weight)
	#do a remove duplicate here
	link_and_weight = convert_to_string(link_and_weight)
	link_and_weight = remove_duplicate(link_and_weight)
	global converted_link_and_weight
	converted_link_and_weight = link_and_weight

	start_node = str(start_node)
	end_node = str(end_node)
	#print(link_and_weight)

	visited_switches_dic = {}  # node:cost
	unvisited_switches_dic = {} #unvisited node
	all_switches = find_all_other_swtiches(link_and_weight) #total number of hosts
	predecessors= {}  # predecesor dics
	for i in all_switches:  #initialize all nodes except the start node to have a cost of inifinity
		if i!=start_node:
			unvisited_switches_dic[i] = float('inf')
		else:
			unvisited_switches_dic[i] = 0

	while len(visited_switches_dic)!=len(all_switches): #start to calculate least cost path to every node
		current_node = node_with_least_cost(unvisited_switches_dic) #get the least node with least cost
		visited_switches_dic[current_node] = unvisited_switches_dic[current_node] #set this node to be visited
		unvisited_switches_dic.pop(current_node) # and remove this node from unvisited
		disconnected_graph = True
		for i in range(len(link_and_weight)):
			# find all links from current_node to adjacent nodes
			if link_and_weight[i][0] == current_node and link_and_weight[i][1] in unvisited_switches_dic:
				disconnected_graph = False
				if visited_switches_dic[current_node] + link_and_weight[i][2] < unvisited_switches_dic[link_and_weight[i][1]]:
					predecessors[link_and_weight[i][1]] = current_node
					unvisited_switches_dic[link_and_weight[i][1]] = visited_switches_dic[current_node] + link_and_weight[i][2]

			if link_and_weight[i][1] == current_node and link_and_weight[i][0] in unvisited_switches_dic:
				disconnected_graph = False
				if visited_switches_dic[current_node] + link_and_weight[i][2] < unvisited_switches_dic[link_and_weight[i][0]]:
					predecessors[link_and_weight[i][0]] = current_node
					unvisited_switches_dic[link_and_weight[i][0]] = visited_switches_dic[current_node] + link_and_weight[i][2]

		if disconnected_graph == True:
			break
	if end_node == "":
		routes = []
		for i in all_switches:
			if i!= start_node:
				routes.append(get_route(start_node,i,predecessors))
		return routes
	else:
		return get_route(start_node,end_node,predecessors)