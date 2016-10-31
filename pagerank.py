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
    def __init__(self, graph, alpha, tolerance, top_p_papers, logging):
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
        self.M = graph.size_a
        # self.M_authors = graph.size_a
        self.graph = graph
        self.paper_rank = self.pagerank_paper(self.graph)
        # self.author_rank = self.pagerank_author(self.graph)
        # self.rank_papers(self.paper_rank, "finished")
        print(len(graph.backward_graph))

    def pagerank_paper(self, g):
        """
        adapted from http://michaelnielsen.org/blog/using-your-laptop-to-compute-pagerank-for-millions-of-webpages/
        TODO: vectorized version
        :param g:
        :param alpha:
        :param tolerance:
        :return:
        """
        P_score = np.ones((self.M, 1)) / self.M #paper scores initialised to 1 vector
        iteration = 1
        difference = self.tolerance*10
        while difference > self.tolerance:
            P_score_updated = self.step_paper(g, P_score)
            difference = np.sum(np.abs(P_score - P_score_updated)) #TODO: experiment: difference measured over top-ranked papers
            print("change in iteration {} is {}".format(iteration, difference))
            P_score = P_score_updated
            self.rank_papers(P_score,iteration)
            iteration += 1
        print(P_score)
        return P_score

    def step_paper(self, g, P_score):
        V = np.zeros((self.M, 1))
        dangling_paper_contribution = self.alpha * sum([P_score[i] for i in g.dangling_authors])/self.M
        teleportation_contribution = (1-self.alpha)/self.M
        for i in xrange(self.M):
            citation_contribution = self.alpha * sum([P_score[k] / g.number_citations_author[k] for k in
                                                      g.backward_graph[i]])
            V[i] = citation_contribution + dangling_paper_contribution + teleportation_contribution
        return V
        # np.sum(V)
        # return V/np.sum(V)

    # def pagerank_author(self, g):
    #     """
    #     adapted from http://michaelnielsen.org/blog/using-your-laptop-to-compute-pagerank-for-millions-of-webpages/
    #     TODO: vectorized version
    #     :param g:
    #     :param alpha:
    #     :param tolerance:
    #     :return:
    #     """
    #     P_score = np.ones((self.M_authors, 1)) / self.M_authors #paper scores initialised to 1 vector
    #     iteration = 1
    #     difference = self.tolerance*10
    #     while difference > self.tolerance:
    #         P_score_updated = self.step_author(g, P_score)
    #         difference = np.sum(np.abs(P_score - P_score_updated)) #TODO: experiment: difference measured over top-ranked papers
    #         print("change in iteration {} is {}".format(iteration, difference))
    #         P_score = P_score_updated
    #         self.rank_author(P_score,iteration)
    #         iteration += 1
    #     print(P_score)
    #     return P_score
    #
    # def step_author(self, g, P_score):
    #     V = np.zeros((self.M_authors, 1))
    #     dangling_paper_contribution = self.alpha * sum([P_score[i] for i in g.dangling_papers])/self.M_authors
    #     self.apply_collaboration_citation_weights(P_score)
    #     teleportation_contribution = (1-self.alpha)/self.M_authors
    #     for author in xrange(self.M_authors):
    #         # citation_contribution = self.apply_collaboration_citation_weights(author, P_score)
    #         citation_contribution = self.alpha * sum([P_score[k] / g.number_citations[k] for k in
    #                                                   g.backward_citation_graph[author]])
    #         V[author] = citation_contribution + dangling_paper_contribution + teleportation_contribution
    #     return V
    #
    # # def apply_collaboration_citation_weights(self, author, P_score):
    # #     total_collaborations =
    # #     collaboration = self.
    # #     citation_contribution = self.alpha * sum([P_score[k] / g.number_citations[k] for k in
    # #                                               g.backward_citation_graph[author]])


    # def apply_weights(self, P_score):
    #     beta = 2
    #     collaboration = self.graph.number_citations
    #     citation_contribution = self.alpha * sum([P_score[k] / g.number_citations[k] for k in g.backward_citation_graph[i]])


    def rank_papers(self, paper_score, iteration):
        """
        get intermediate pagerank and log the results
        """
        print("paper rank at iteration: {}".format(iteration))
        unranked_list_papers = paper_score.reshape(1,self.M)[0]
        indices_of_top_ranked_papers = heapq.nlargest(self.top_p_papers,
                                                           xrange(len(unranked_list_papers)),
                                                           unranked_list_papers.__getitem__)

        #get the pagerank score for each of the papers in the specified indices
        score_of_top_ranked_papers = np.take(unranked_list_papers, indices_of_top_ranked_papers)
        print(score_of_top_ranked_papers)
        self.log.save_intermediate_ranking(indices_of_top_ranked_papers, score_of_top_ranked_papers, iteration)

