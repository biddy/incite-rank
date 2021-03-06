from __future__ import division

from pagerank import *
from pagerank_logging import Logging

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

alphas = [0.25, 0.5, 0.75, 0.85, 0.95]
tolerance = 0.001
top_p_rank = 50
log = Logging(top_p_rank)

for alpha in alphas:
    experiment_tag = 'alpha:{}#tolerance:{}'.format(alpha,tolerance)
    print('calling pagerank')
    rank = pagerank(cit_graph, log, experiment_tag, alpha=alpha, tolerance=tolerance, debug=True)
    print('done!')

log.chart_proportions()
