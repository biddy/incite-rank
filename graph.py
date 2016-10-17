from __future__ import division
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from pagerank import PageRank

class Graph:
    """
    takes the dataset as input and creates the citation network graph
    the citation_graph is a dict() where the keys are the papers and the values are the
    citations within the paper associated with the key.

    forward_citation_graph: dict() where key: paper containing citations and value: citations within said paper.
    backward_citation_graph: dict() where key: citation and value: paper containing the citation.
    """
    def __init__(self, dataset, length):
        self.forward_citation_graph = {i:[] for i in xrange(length)}
        self.backward_citation_graph = {i:[] for i in xrange(length)}
        self.extract_data(dataset)
        self.create_backward_citation_graph()
        self.size = len(self.forward_citation_graph)
        self.dangling_papers = set()
        self.non_dangling_papers = set()
        self.calc_dangling_papers()
        self.number_citations = {k: len(self.forward_citation_graph[k])
                                     for k in self.forward_citation_graph.keys()}
        print("forward citation graph size is {:.2f} MB".format(sys.getsizeof(self.forward_citation_graph)/1000000))
        print("backward citation graph size is {:.2f} MB".format(sys.getsizeof(self.backward_citation_graph)/1000000))
        self.analytics()
        #sanity check to see the citation graph for the highest ranked paper.
        # print(self.backward_citation_graph[232309])

    def calc_dangling_papers(self):
        for key in self.forward_citation_graph.keys():
            if len(self.forward_citation_graph[key]) == 0:
                self.dangling_papers.add(key)
            else:
                self.non_dangling_papers.add(key)
        print("# of DANGLER papers is {}".format(len(self.dangling_papers)))
        print("# of NORMAL papers is {}".format(len(self.non_dangling_papers)))

    def create_backward_citation_graph(self):
        for k in self.forward_citation_graph.keys():
            values = self.forward_citation_graph[k]
            for value in values:
                self.backward_citation_graph[value].append(k)
                # try:
                #     self.backward_citation_graph[value].append(k)
                # except:
                #     self.backward_citation_graph[value] = [k]

    def analytics(self):
        citation_counts = {}
        for paper in self.forward_citation_graph.keys():
            num_citations = len(self.forward_citation_graph[paper])
            self.increment_dict(citation_counts,num_citations)
            # citation_counts[num_citations] += 1
        # for key in citation_counts.keys():
            # print("{} : {}".format(key, citation_counts[key]))
        cited_by_counts = {}
        for paper in self.backward_citation_graph.keys():
            num_c = len(self.backward_citation_graph[paper])
        #     print(num_c)
            self.increment_dict(cited_by_counts, num_c)
        for key in cited_by_counts.keys():
            print("{} : {}".format(key, cited_by_counts[key]))
        #     cited_by_counts[num_c] += 1
        # for i in range(len(cited_by_counts)):
        #     print("{} : {}".format(i, cited_by_counts[i]))

    def increment_dict(self, dict, key):
        try:
            dict[key] += 1
        except:
            dict[key] = 1


    def extract_data(self, dataset):
        with open(dataset, "r") as f:
            f = f.readlines()
            check_citation = False
            for word in f:
                # if word == "":
                if word[0:6] == "#index" and check_citation is False:
                    node = int(word[6:])
                    # print("node value is {}".format(node))
                    # self.forward_citation_graph[node] = []
                    check_citation = True
                    continue
                if check_citation is True:
                    if word[0:2] != "#%":
                        check_citation = False
                    else:
                        target = int(word[2:])
                        # print("connection between {} and {}".format(node, target))
                        self.forward_citation_graph[node].append(target)
                        # self.add_connection(node, target)

if __name__ == "__main__":
    # dataset = "/Users/iain/development/datasets/pagerank/outputacm_medium.txt"
    dataset = "/Users/iain/development/datasets/pagerank/outputacm.txt"
    dataset_length = 629813
    g = Graph(dataset, dataset_length)
    p = PageRank(g)
    print(p.ranked_list_papers)[:10]
    for paper in p.ranked_list_papers[:10]:
        print("{} is cited by {}".format(paper, g.backward_citation_graph[paper]))
