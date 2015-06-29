
__author__ = 'irelos'


import random
import networkx
import heapq


# Information diffusion models: currently only for SIR type model
# General inputs:
# 1. Graph (undirected or directed, weighted)
# 2. Source node list
# 3. Stopping rules
#   3.1 Default stop: infects all nodes
#   3.2 Stop by number of ever infected nodes
#   3.3 Stop by time slot(discrete time model) or time upper bound(continuous time model)
# 4. Diffusion time distribution
# General outputs:
# 1. The states of all nodes when the stopping rules are satisfied
# 2. Infection time and recovery time for all nodes


# To be implemented models
# 1. Continuous Time SI model with supplied pdf for each edge, weighted edge to adopt heterogeneous
# 2. Continuous Time SIR model with supplied pdf for each edge, weighted edge to adopt heterogeneous

def con_time_SI(g, source, stopRule = 0, stopParam = 0, homo = True, randompdf = random.random,*args):
    """
    :param g: graph
    :param source: list of sources
    :param stopRule: stop rules: 1 stop by time, stopParam = up_to_time , 2 stop by size, stopParam = number of infected
     nodes
    :param stopParam: Param associating with stop rules
    :param homo: True Homogeneous model, False Heterogeneous Model
    :param randompdf: the infection time distribution for the edges
    :param args: the supplied arguments for randompdf,
    For homo geneous case:
        eg.
            import networkx
            g = networkx.florentine_families_graph()
            source = [g.nodes()[0],g.nodes()[1]]
            res = con_time_SI(g, source,0, 0, True, random.uniform,0,1)

    For heterogeneous case:
        eg.
            import networkx
            g = networkx.florentine_families_graph()
            source = [g.nodes()[0],g.nodes()[1]]
            for edg in g.edges():
                g.edge[edg[0]][edg[1]]['q'] = 0
                g.edge[edg[0]][edg[1]]['p'] = 1

            res = con_time_SI(g, source,0, 0, False, random.uniform,'q','p')
    :return: Infection Time Dic, key: node id, item: infection time
    """

    #check inputs
    random.seed()
    directed = (type(g) == type(networkx.DiGraph()))
    if ~directed:
        assert(type(g) == type(networkx.Graph()))

    if len(source) == 0:
        raise ValueError('No source provided!')


    infectTimeDic = {}
    infectNodeSet = set()
    activeNodeList = [] # nodes who is the neighbor of the infected nodes

    for s in source:
        heapq.heappush(activeNodeList,[0.0, s])

    globalTime = 0.0


    while (1):
        # identify the next infected nodes
        while(1):
            if len(activeNodeList) != 0:
                nextInfNode = heapq.heappop(activeNodeList)
            else:
                nextInfNode=[]
                break
            if nextInfNode[1] not in infectNodeSet:
                break

        if len(nextInfNode) == 0:
            print 'no active node, infects all nodes by default'
            break



        # judge the output according to stopping rules
        if stopRule == 1: #stop by time, stopParam = up_to_time
            if stopParam < nextInfNode[0]:
                break
        elif stopRule == 2: #stop by size, stopParam = number of infected nodes
            if len(infectNodeSet) >= stopParam:
                break

        # set the node with min infection time to be infected
        infectTimeDic[nextInfNode[1]] = nextInfNode[0]
        infectNodeSet.add(nextInfNode[1])
        globalTime = nextInfNode[0]

        # finds the neighbor of the infected nodes
        l = []
        if directed:
            l = g.successors(nextInfNode[1])
        else:
            l = g.neighbors(nextInfNode[1])

        addedNode = [nn for nn in l if nn not in infectNodeSet]


        # set the delay time on the edge of the newly infected nodes

        activeTime = []
        for nd in addedNode:
            if homo:
                tmpT = randompdf(*args)
            else:
                newargs = []
                for ss in args:
                    newargs.append(g.edge[nextInfNode[1]][nd][ss])
                tmpT = randompdf(*newargs)
                if tmpT <= 0.0:
                    print 'Warning: pdf has supports in negative range! Negative value will be truncated to 0!'
                    tmpT = 0.0
            activeTime.append(tmpT)

        # add the new active nodes to the list
        for ii in range(0, len(addedNode)):
            heapq.heappush(activeNodeList,[activeTime[ii] + globalTime, addedNode[ii]])
    return infectTimeDic



