from __future__ import division
import sys
import numpy as np
import heapq

from pagerank import *
from logging import Logging



if len(sys.argv) != 2:
    print('need dataset')
    sys.exit(-1)

collaboration_data = []
citation_data = []
print('reading datasets')
with open(sys.argv[1]) as f:
    for line in f:
        co_d = {}
        ci_d = {}
        co, ci = line.strip().split('#')
        collaboration_list = []
        citation_list = []

        if len(co) > 0:
            collaboration_list = [int(val) for val in co.split(',')]
        for c in collaboration_list:
            if c in co_d:
                co_d[c] = co_d[c] + 1
            else:
                co_d[c] = 1

        if len(ci) > 0:
            citation_list = [int(val) for val in ci.split(',')]
        for c in citation_list:
            if c in ci_d:
                ci_d[c] = ci_d[c] + 1
            else:
                ci_d[c] = 1
        collaboration_data.append(co_d)
        citation_data.append(ci_d)

#print(len(collaboration_data))
#print(len(citation_data))
print('combining datasets to create a single graph')

# for i in len(experiment_size):

#is experiments run on beta, make sure this is part oft he loop. Otherwise it can be separate

#logging
# log = Logging(cit_graph, tolerance, alpha, top_p_rank)

betas = [0.1,1]
tolerance = 0.01
alpha = 0.8
top_p_rank = 50

log = Logging(top_p_rank)

for beta in betas:
    experiment_tag = 'beta{}#alpha{}'.format(beta,alpha)
    cit_graph = add_datasets(citation_data, collaboration_data, beta=beta)
    normalize(cit_graph)
    print('calling pagerank')
    rank = pagerank(cit_graph, log, experiment_tag, alpha=alpha, tolerance=tolerance, debug=True)
    print('done with experiment : {}'.format(experiment_tag))

print(log.experiment_results)
log.chart_proportions()

