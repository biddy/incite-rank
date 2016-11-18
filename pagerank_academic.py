from __future__ import division

from pagerank import *
from pagerank_logging import Logging

if len(sys.argv) != 2:
    print('need dataset')
    sys.exit(-1)

collaboration_data = []
citation_data = []

logging_dataset = {}
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
            count_dict = None
            if c in logging_dataset:
                count_dict = logging_dataset[c]
            else:
                count_dict = {'col': 0, 'cit': 0}
                logging_dataset[c] = count_dict
            count_dict['col'] = count_dict['col'] + 1

        if len(ci) > 0:
            citation_list = [int(val) for val in ci.split(',')]
        for c in citation_list:
            if c in ci_d:
                ci_d[c] = ci_d[c] + 1
            else:
                ci_d[c] = 1
            count_dict = None
            if c in logging_dataset:
                count_dict = logging_dataset[c]
            else:
                count_dict = {'col': 0, 'cit': 0}
                logging_dataset[c] = count_dict
            count_dict['cit'] = count_dict['cit'] + 1

        collaboration_data.append(co_d)
        citation_data.append(ci_d)

print('combining datasets to create a single graph')

betas = [0.01,0.25,0.5,0.75,0.99]
tolerance = 0.01
alpha = 0.85
top_p_rank = 50

log = Logging(top_p_rank)

for beta in betas:
    experiment_tag = 'beta:{}#alpha:{}'.format(beta,alpha)
    cit_graph = add_datasets(citation_data, collaboration_data, beta=beta)
    normalize(cit_graph)
    print('calling pagerank')
    rank = pagerank(cit_graph, log, experiment_tag, alpha=alpha, tolerance=tolerance, debug=True)
    print('done with experiment : {}'.format(experiment_tag))

print(log.experiment_results)
log.chart_proportions()
log.chart_academic(logging_dataset)

