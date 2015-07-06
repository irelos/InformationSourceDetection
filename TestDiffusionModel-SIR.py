__author__ = 'irelos'

from conSIR import con_time_SIR


# test default function
import networkx
import random

# test one sources case, default setting
g = networkx.florentine_families_graph()
source = [g.nodes()[0]]
res = con_time_SIR(g, source)
print len(res)

#test three sources case, default setting
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SIR(g, source)
print len(res)


#test two sources case, heterogeneous model
import networkx
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1]]
for edg in g.edges():
    g.edge[edg[0]][edg[1]]['q'] = 0
    g.edge[edg[0]][edg[1]]['p'] =  random.random()
for nd in g.nodes():
    g.node[nd]['rl'] = 0
    g.node[nd]['ru'] = random.random()

res = con_time_SIR(g, source, 1,  0.5, False, random.uniform,random.uniform, 2,'q','p','rl','ru')
print len(res)


#test supplied function in scipy
from scipy.stats import expon
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SIR(g, source, 0, 0, True, expon.rvs,expon.rvs,2,0.0,1.0,0.0,1.0)
print len(res)

#test stopping rule 2
from scipy.stats import expon
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SIR(g, source, 2, 10, True, expon.rvs,expon.rvs,2,0.0,1.0,0.0,1.0)
print len(res)

#heavy load test
g = networkx.erdos_renyi_graph(5000,0.002)
source = [g.nodes()[0]]
res = con_time_SIR(g, source, 0, 0, True, expon.rvs, random.uniform,2,0.0,1.0,0.0,1)
print len(res)



