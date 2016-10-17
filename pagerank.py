import numpy as np

"""
IDEAS:
temporal dynamics
incorporating clustering on the "content" of the article/abstract
"""

class PageRank:
    def __init__(self, graph):
        self.number_top_papers = 20
        self.n = graph.size
        self.graph = graph
        self.unranked_list_papers = self.pagerank(self.graph)
        self.rank_list_papers()
        print(len(graph.backward_citation_graph))

    def pagerank(self, g, alpha=0.85, tolerance=0.001):
        P = np.ones((self.n, 1)) / self.n
        iteration = 1
        difference = 2
        while difference > tolerance:
            P_updated = self.step(g, P, alpha)
            difference = np.sum(np.abs(P - P_updated))
            print("change for L1 norm in iteration {} is {}".format(iteration, difference))
            iteration += 1
            P = P_updated
        print(P)
        return P

    def step(self, g, P, alpha=0.85):
        V = np.zeros((self.n, 1))
        dangling_vector = sum([P[i] for i in g.dangling_papers])
        for i in xrange(1,self.n):
            paper_importance = sum([P[k] / g.number_citations[k] for k in g.backward_citation_graph[i]])
            V[i] = alpha * paper_importance + alpha * (dangling_vector/self.n) \
                   + (1-alpha)/self.n
        return V/np.sum(V)

    def rank_list_papers(self):
        print("ranking papers")
        self.unranked_list_papers = self.unranked_list_papers.reshape(1,self.n)
        self.ranked_list_papers = np.argpartition(self.unranked_list_papers, -1)[0][::-1]
        # print(max(xrange(len(self.unranked_list_papers)), key = lambda x: self.unranked_list_papers[x]))
