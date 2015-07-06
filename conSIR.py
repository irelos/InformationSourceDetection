__author__ = 'irelos'
import random
import networkx
import heapq

def con_time_SIR(g, source, stopRule = 0, stopParam = 0, homo = True, infRandompdf = random.random,recRandompdf = random.random, *args):
    """
    :param g: graph
    :param source: list of sources
    :param stopRule: stop rules: 1 stop by time, stopParam = up_to_time , 2 stop by size, stopParam = number of infected
     nodes
    :param stopParam: Param associating with stop rules
    :param homo: True Homogeneous model, False Heterogeneous Model
    :param infRandompdf: the infection time distribution for the edges
    :param recRandompdf: the recovery time distribution for the nodes
    :param args: the supplied arguments for infRandompdf and recRandompdf, args=[number of args for infRandompdf, ...]
    For homo geneous case:
        eg.
            import networkx
            g = networkx.florentine_families_graph()
            source = [g.nodes()[0],g.nodes()[1]]
            res = con_time_SIR(g, source,0, 0, True, random.uniform, random.uniform,2,0,1,0,1)
            print len(res)
    For heterogeneous case:
        eg.
            import networkx
            g = networkx.florentine_families_graph()
            source = [g.nodes()[0],g.nodes()[1]]
            for edg in g.edges():
                g.edge[edg[0]][edg[1]]['q'] = 0
                g.edge[edg[0]][edg[1]]['p'] =  random.random()
            for nd in g.nodes():
                g.node[nd]['rl'] = 0
                g.node[nd]['ru'] = random.random()

            res =  con_time_SIR(g, source, 0,  0, False, random.uniform,random.uniform, 2,'q','p','rl','ru')
            print len(res)

            res = con_time_SI(g, source,0, 0, False, random.uniform,'q','p')
    :return: Infection Time Dic, key: node id, item: [infection time, recovered time]
    """

    #check inputs
    [infArgs,recArgs] = separateArgs(args)
    random.seed()
    directed = (type(g) == type(networkx.DiGraph()))
    if ~directed:
        assert(type(g) == type(networkx.Graph()))

    if len(source) == 0:
        raise ValueError('No source provided!')


    infectTimeDic = {}
    infectRecNodeSet = set()
    activeNodeList = [] # nodes who is the neighbor of the infected nodes

    for s in source:
        tmpT = generateRandomTime(homo, False, recRandompdf, g, s, [], *recArgs)
        heapq.heappush(activeNodeList,[0.0, tmpT, s])

    globalTime = 0.0


    while (1):
        # identify the next infected nodes
        while(1):
            if len(activeNodeList) != 0:
                nextInfNode = heapq.heappop(activeNodeList)
            else:
                nextInfNode=[]
                break

            if (nextInfNode[2] not in infectRecNodeSet) and (nextInfNode[1] > nextInfNode[0]):
                break

        if len(nextInfNode) == 0:
            print 'no active node, infects all nodes by default'
            break



        # judge the output according to stopping rules
        if stopRule == 1: #stop by time, stopParam = up_to_time
            if stopParam < nextInfNode[0]:
                break
        elif stopRule == 2: #stop by size, stopParam = number of infected nodes
            if len(infectRecNodeSet) >= stopParam:
                break

        # set the node with min infection time to be infected
        recoverTime = nextInfNode[0]+generateRandomTime(homo, False, recRandompdf, g, nextInfNode[2], [], *recArgs)
        infectTimeDic[nextInfNode[2]] = [nextInfNode[0], recoverTime]

        infectRecNodeSet.add(nextInfNode[2])
        globalTime = nextInfNode[0]

        # finds the neighbor of the infected nodes
        l = []
        if directed:
            l = g.successors(nextInfNode[2])
        else:
            l = g.neighbors(nextInfNode[2])

        addedNode = [nn for nn in l if nn not in infectRecNodeSet]


        # set the delay time on the edge of the newly infected nodes

        activeTime = []
        for nd in addedNode:
            tmpT = generateRandomTime(homo, True, infRandompdf, g, nextInfNode[2], nd, *infArgs)
            activeTime.append(tmpT)

        # add the new active nodes to the list
        for ii in range(0, len(addedNode)):
            heapq.heappush(activeNodeList,[activeTime[ii] + globalTime, recoverTime, addedNode[ii]])
    return infectTimeDic

def separateArgs(args):
    if len(args) == 0:
        return [[],[]]
    numInfArg = args[0]
    assert(type(numInfArg) == type(1))
    infArgs = []
    recArgs = []
    for i in range(1,len(args)):
        if(i <= numInfArg):
            infArgs.append(args[i])
        else:
            recArgs.append(args[i])
    return [infArgs,recArgs]


def generateRandomTime(homo, infOrNot, randompdf, g, nd1, nd2, *args):
    if homo:
        tmpT = randompdf(*args)
    else:
        newargs = []
        for ss in args:
            if infOrNot:
                newargs.append(g.edge[nd1][nd2][ss])
            else:
                newargs.append(g.node[nd1][ss])
        tmpT = randompdf(*newargs)
        if tmpT <= 0.0:
            print 'Warning: pdf has supports in negative range! Negative value will be truncated to 0!'
            tmpT = 0.0
    return tmpT