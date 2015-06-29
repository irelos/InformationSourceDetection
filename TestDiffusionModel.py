__author__ = 'irelos'

from DiffusionModels import con_time_SI


# test default function
import networkx
import random

# test one sources case, default setting
g = networkx.florentine_families_graph()
source = [g.nodes()[0]]
res = con_time_SI(g, source)
print res

#test three sources case, default setting
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SI(g, source, 0, 0, True, random.random)
print res


#test two sources case, heterogeneous model
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1]]
for edg in g.edges():
    g.edge[edg[0]][edg[1]]['q'] = 0
    g.edge[edg[0]][edg[1]]['p'] = 1
res = con_time_SI(g, source,1, 0.5, False, random.uniform,'q','p')
print res


#test supplied function in scipy
from scipy.stats import expon
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SI(g, source, 0, 0, True, expon.rvs,0.0,1.0)
print res

#test stopping rule 2
from scipy.stats import expon
g = networkx.florentine_families_graph()
source = [g.nodes()[0],g.nodes()[1],g.nodes()[2]]
res = con_time_SI(g, source, 2, 10, True, expon.rvs,0.0,1.0)
print res

#heavy load test
g = networkx.erdos_renyi_graph(5000,0.0005)
source = [g.nodes()[0]]
res = con_time_SI(g, source)
print len(res)