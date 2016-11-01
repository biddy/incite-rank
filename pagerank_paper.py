from __future__ import division
import sys
import numpy as np
import heapq

from pagerank import *
from logging import Logging



if len(sys.argv) != 2:
    print('need dataset')
    sys.exit(-1)

cit_graph = []
print('reading dataset')
count = 0.0
with open(sys.argv[1]) as f:
    for line in f:
        d = {}
        line = line.strip()
        citations = []
        if len(line) > 0:
            citations = [int(val) for val in line.split(',')]
            count += len(citations)
        for c in citations:
            if c in d:
                d[c] = d[c] + 1
            else:
                d[c] = 1
        cit_graph.append(d)

nodes = len(cit_graph)
print('graph density: ' + str(count/(nodes*nodes)))

print('dataset size: ' + str(len(cit_graph)))
print('normalizing graph')
normalize(cit_graph)

# tolerances = [0.1,0.01,0.001]
# results = [[] for i in range(len(tolerances))]
# for i in range(len(tolerances)):
#     # tolerance = 0.01
#     alpha = 0.85
#     top_p_rank = 50
#     #logging
#     log = Logging(cit_graph, tolerances[i], alpha, top_p_rank)
#
#     print('calling pagerank')
#     rank = pagerank(cit_graph, log, alpha=0.85, tolerance=tolerances[i], debug=True)
#     print('done!')
#     results[i] = log.proportions_of_final_rank_per_iteration()
#     log.chart_proportions(results[i])
#
# log.show_chart()

alphas = [0.75,0.80]
results = [[] for i in range(len(alphas))]
top_p_rank = 50
log = Logging(cit_graph, top_p_rank)

for alpha in range(len(alphas)):
    tolerance = 0.001
    # alpha = 0.85
    #logging

    print('calling pagerank')
    rank = pagerank(cit_graph, log, alpha=alphas[alpha], tolerance=tolerance, debug=True)
    print('done!')
    results[i] = log.proportions_of_final_rank_per_iteration()
    label = "alpha : {}".format(alphas[alpha])
    log.add_result_to_chart(results[i], label)
log.show_chart(alphas[alpha], tolerance, top_p_rank)

# print(heapq.nlargest(50, range(len(rank)), key=rank.__getitem__))
# log.print_log()
# log.proportions_of_final_rank_per_iteration()