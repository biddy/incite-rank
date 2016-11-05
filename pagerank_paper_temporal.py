from __future__ import division
import sys
import numpy as np
import heapq

from pagerank import *
from logging import Logging

def mean_citation_year(citation_years):
# finding the mean of list of years cited for each paper in "citation_years"
    for paper in citation_years:
        year_list = citation_years[paper]
        if len(year_list) > 0:
            citation_years[paper] = sum(year_list)/len(year_list)
        else:
            citation_years[paper] = 0

def temporal_adjustment(graph, published, citation_years, gamma=0.5):
    temporal_cit_graph = graph
    for index in range(len(temporal_cit_graph)):     # for each row of graph
        citations_list = temporal_cit_graph[index]        # .. grab the out-citation dictionary
        for paper in citations_list:         # for each out cited paper for paper with given index
# if that out-cited paper has a mean citation year
            if paper in citation_years and citation_years[paper] != 0 and (citation_years[paper] - published[index]) != 0:
                citations_list[paper] = (abs(citation_years[paper] - published[index])**gamma)*citations_list[paper]
    return temporal_cit_graph

if len(sys.argv) != 3:
    print('arguments needed: <paper citation dataset> <paper publication year dataset>')
    sys.exit(-1)

debug = True
cit_graph = []
pub_year = {}       # map from paper index to year of publication

# map (initially) from paper index to list of years of papers that it has been cited by
years_cited = {}


print('reading publication date dataset')
index = 0
with open(sys.argv[2]) as f:
    for line in f:
        pub_year[index] = int(line.strip())
        index += 1


print('reading citation dataset')
count = 0.0
index = 0
with open(sys.argv[1]) as f:
    for line in f:
        d = {}
        line = line.strip()
        citations = []
        if len(line) > 0:
            citations = [int(val) for val in line.split(',')]
            count += len(citations)
            year = pub_year[index]
        for c in citations:
            if c in d:
                d[c] = d[c] + 1
            else:
                d[c] = 1

            # adding the year of the current paper to the list of years for its cited papers
            year_list = None
            if c in years_cited:
                year_list = years_cited[c]
            else:
                year_list = []
                years_cited[c] = year_list
            year_list.append(year)
        index += 1
        cit_graph.append(d)


nodes = len(cit_graph)
print('graph density: ' + str(count/(nodes*nodes)))

print('dataset size: ' + str(len(cit_graph)))


gammas = [0.5,1,2]
tolerance = 0.01
alpha = 0.8
top_p_rank = 50

log = Logging(top_p_rank)
mean_citation_year(years_cited)

for gamma in gammas:
    experiment_tag = 'gamma:{}#alpha:{}'.format(gamma,alpha)
    print('adding temporal weights')
    temporal_cit_graph = temporal_adjustment(cit_graph, pub_year, years_cited, gamma=gamma)
    print('normalizing graph')
    normalize(temporal_cit_graph)

    print('calling pagerank')
    # rank = pagerank(cit_graph, debug=True)
    rank = pagerank(temporal_cit_graph, log, experiment_tag, alpha=alpha, tolerance=tolerance, debug=True)
print('done!')
# print(heapq.nlargest(50, range(len(rank)), key=rank.__getitem__))
log.chart_proportions()
log.chart_temporal()
