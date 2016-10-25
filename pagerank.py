import numpy as np
import bottleneck
import heapq

"""
IDEAS:
author -> author pagerank rather than paper -> paper
temporal dynamics
incorporating clustering on the "content" of the article/abstract
empirical study showing/visualising the "effect" of various tuning parameters
"""

class PageRank:
    def __init__(self, graph, alpha=0.85, tolerance=0.01, top_p_papers=20, logging):
        """
        :param graph: The graph we are running pagerank on
        :param alpha:
        :param tolerance:
        :param top_p_papers:
        :param logging: Logging module to save intermediate results and handle visualisation etc
        :return:
        """
        self.log = logging
        self.alpha = alpha
        self.tolerance = tolerance
        self.top_p_papers = top_p_papers
        self.n = graph.size
        self.graph = graph
        self.paper_rank = self.pagerank(self.graph)
        self.rank_papers(self.paper_rank, "finished")
        print(len(graph.backward_citation_graph))

    def pagerank(self, g):
        """
        adapted from http://michaelnielsen.org/blog/using-your-laptop-to-compute-pagerank-for-millions-of-webpages/
        TODO: vectorized version
        :param g:
        :param alpha:
        :param tolerance:
        :return:
        """
        P = np.ones((self.n, 1)) / self.n
        iteration = 1
        difference = 2
        while difference > self.tolerance:
            P_updated = self.step(g, P)
            difference = np.sum(np.abs(P - P_updated))
            print("change for L1 norm in iteration {} is {}".format(iteration, difference))
            P = P_updated
            self.rank_papers(P,iteration)
            iteration += 1
        print(P)
        return P

    def step(self, g, P):
        V = np.zeros((self.n, 1))
        dangling_vector = sum([P[i] for i in g.dangling_papers])
        for i in xrange(self.n):
            paper_importance = sum([P[k] / g.number_citations[k] for k in g.backward_citation_graph[i]])
            V[i] = self.alpha * paper_importance + self.alpha * (dangling_vector/self.n) \
                   + (1-self.alpha)/self.n
            # V[i] = alpha*sum([P[k]/g.number_citations[k]
            #               for k in g.backward_citation_graph[i]])+ alpha*dangling_vector/self.n+(1-alpha)/self.n
        return V/np.sum(V)

    def rank_papers(self, paper_score, iteration):
        print("paper rank at iteration: {}".format(iteration))
        unranked_list_papers = paper_score.reshape(1,self.n)[0]
        indices_of_top_ranked_papers = heapq.nlargest(self.top_p_papers,
                                                           xrange(len(unranked_list_papers)),
                                                           unranked_list_papers.__getitem__)

        #get the pagerank score for each of the papers in the specified indices
        self.score_of_top_ranked_papers = np.take(unranked_list_papers, indices_of_top_ranked_papers)
        print(self.score_of_top_ranked_papers)
        self.log.save_intermediate_ranking(indices_top_papers, iteration)

        # print(self.unranked_list_papers)
        # self.unranked_list_papers_temp = self.unranked_list_papers.reshape(1,self.n)[0]
        # print(self.unranked_list_papers_temp)
        # self.ranked_list_papers = np.argpartition(self.unranked_list_papers_temp, -1)[::-1]
        # print(self.ranked_list_papers)

        # self.unranked_list_papers_temp = self.paper_score.reshape(1,self.n)[0]
        # self.indices_of_top_ranked_papers = bottleneck.argpartsort(-self.unranked_list_papers_temp,
        #                                                          self.top_p_papers)[:self.top_p_papers]
        # self.values_of_top_ranked_papers = np.argpartition(-self.unranked_list_papers_temp, self.top_p_papers)
        # self.unranked_list_papers_temp = self.paper_score.reshape(1,self.n)[0]
        # self.ranked_list_papers = np.argpartition(-self.unranked_list_papers_temp, self.number_top_papers)#[::-1]
        # print(np.partition(-self.unranked_list_papers_temp, self.number_top_papers)[:self.number_top_papers])


        # print(max(xrange(len(self.unranked_list_papers)), key = lambda x: self.unranked_list_papers[x]))
