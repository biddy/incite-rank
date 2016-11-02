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

betas = [0.5,1]
tolerance = 0.001
alpha = 0.85
results = [[] for i in range(len(betas))]
top_p_rank = 50

citation_graph = add_datasets(citation_data, collaboration_data, beta=1)
log = Logging(citation_graph, top_p_rank)

iteration = 1
for beta in betas:
    cit_graph = add_datasets(citation_data, collaboration_data, beta=beta)
    normalize(cit_graph)
    # tolerance = 0.001
    # alpha = 0.85
    #logging

    print('calling pagerank')
    rank = pagerank(cit_graph, log, alpha=alpha, tolerance=tolerance, debug=True)
    print('done!')
    results[i] = log.proportions_of_final_rank_per_iteration()
    # label = "alpha : {}".format(alphas[alpha])
    label = "beta : {}".format(beta)
    log.add_result_to_chart(results[i], label)

log.show_chart(alpha, tolerance, top_p_rank, beta)


print('dataset size: ' + str(len(cit_graph)))
print('normalizing graph')
normalize(cit_graph)
print('calling pagerank')
rank = pagerank(cit_graph, log, alpha=0.85, tolerance=0.01, debug=True)
print('done!')
# print(heapq.nlargest(50, range(len(rank)), key=rank.__getitem__))
log.print_log()
log.proportions_of_final_rank_per_iteration()
