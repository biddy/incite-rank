from __future__ import division
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from pagerank import PageRank
from logging import Logging

class Graph:
    """
    takes the dataset as input and creates the citation network graph
    the citation_graph is a dict() where the keys are the papers and the values are the
    citations within the paper associated with the key.

    forward_citation_graph: dict() where key: paper containing citations and value: citations within said paper.
    backward_citation_graph: dict() where key: citation and value: paper containing the citation.
    """
    def __init__(self, dataset_papers, dataset_authors, beta):
        self.beta = beta
        # self.forward_citation_graph = {}
        # self.backward_citation_graph = {}

        self.forward_citation_graph = {i:[] for i in xrange(self.key_count(dataset_papers))}
        self.backward_citation_graph = {i:[] for i in xrange(self.key_count(dataset_papers))}
        self.forward_author_graph = {i:{} for i in xrange(self.key_count(dataset_authors))}
        self.backward_author_graph = {i:{} for i in xrange(self.key_count(dataset_authors))}
        self.extract_paper_data(dataset_papers)
        self.extract_author_data(dataset_authors)
        for i in range(20):
            print(self.forward_author_graph[i])
        # self.extract_data(dataset)
        self.create_backward_citation_graph()
        self.size = len(self.forward_citation_graph)
        self.dangling_papers = set()
        self.non_dangling_papers = set()
        self.calc_dangling_papers()
        self.number_citations = {k: len(self.forward_citation_graph[k])
                                     for k in self.forward_citation_graph.keys()}
        print("forward citation graph size is {:.2f} MB".format(sys.getsizeof(self.forward_citation_graph)/1000000))
        print("backward citation graph size is {:.2f} MB".format(sys.getsizeof(self.backward_citation_graph)/1000000))

    def key_count(self, file):
        with open(file) as f:
            for i, l in enumerate(f, 1):
                pass
        return i

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

    def papers_binned_by_citation_count(self):
        citation_counts = {}
        for paper in self.forward_citation_graph.keys():
            num_citations = len(self.forward_citation_graph[paper])
            self.increment_dict(citation_counts,num_citations)
        cited_by_counts = {}
        for paper in self.backward_citation_graph.keys():
            num_c = len(self.backward_citation_graph[paper])
            self.increment_dict(cited_by_counts, num_c)
        for key in cited_by_counts.keys():
            print("{} : {}".format(key, cited_by_counts[key]))

    def extract_author_data(self, dataset_authors):
        with open(dataset_authors, "r") as f:
            f = f.readlines()
            for line_number in range(len(f)):
                line = f[line_number].strip('\n')
                if len(line) > 0:
                    words = line.split('#')
                    if len(words) != 2:
                        print("SOMETHING WRONG WITH INPUT")
                    collaborations, citations = words[0], words[1]
                    if len(collaborations) > 0:
                        collaborations = collaborations.split(",")
                    if len(citations) > 0:
                        citations = citations.split(",")
                    # for collab in collaborations:
                    #     self.forward_author_graph[line_number][collab] = [0,0]
                    # for cit in citations:
                    #     self.forward_author_graph[line_number][cit] = [0,0]
                    #
                    for collab in collaborations:
                        self.author_dict_add_create_key(self.forward_author_graph, line_number, int(collab), 0)
                    for cit in citations:
                        self.author_dict_add_create_key(self.forward_author_graph, line_number, int(cit), 1)

    def extract_paper_data(self, dataset_papers):
        with open(dataset_papers, "r") as f:
            f = f.readlines()
            for line_number in range(len(f)):
                line = f[line_number].strip('\n')
                if len(line) > 0:
                    words = line.split(',')
                    for w in words:
                        self.forward_citation_graph[line_number].append(int(w))

    def author_dict_add_create_key(self, dict, key1, key2, index):
        if key2 in dict[key1].keys():
            dict[key1][key2][index] += 1
        else:
            dict[key1][key2] = [0,0]

    def dict_add_create_key(self, dict, key, value):
        if key in dict.keys():
            dict[key].append(value)
        else:
            dict[key] = [value]

    def increment_dict(self, dict, key):
        try:
            dict[key] += 1
        except:
            dict[key] = 1

    def extract_data(self, dataset):
        """
        This is the old code for the original dataset
        """
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
    dataset_papers = "data/paper_citation"
    dataset_authors = "data/author_citation"
    alpha = 0.85
    beta = 0.5 #weight of collaboration to citations
    tolerance = 0.0001
    top_p_papers = 50

    papers_graph = Graph(dataset_papers, dataset_authors, beta)
    # g.papers_binned_by_citation_count()
    log = Logging()

    p = PageRank(papers_graph, alpha, tolerance, top_p_papers, log)
    log.print_log()
    log.proportions_of_final_rank_per_iteration()
    # print(p.indices_of_top_ranked_papers)[:top_p_papers]
    # for paper in p.indices_of_top_ranked_papers[:top_p_papers]:
    #     # print("paper {} has score {} and is cited by {}".format(paper, p.paper_score[paper], g.backward_citation_graph[paper]))
    #     print("paper {} has score {}".format(paper, p.paper_score[paper]))
