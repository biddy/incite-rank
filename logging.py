from __future__ import division
import heapq

import numpy as np
import matplotlib.pyplot as plt


class Logging:

    def __init__(self, graph, top_p_rank):
        # self.alpha = alpha
        # self.tolerance = tolerance
        self.top_p_rank = top_p_rank
        self.graph = graph
        self.handles = [] #labels for the chart legend
        self.pagerank_log = dict()

    def save_intermediate_ranking(self, paper_index, paper_score, iteration):
        """
        intermediate results are saved in a dict where the key is the iteration number
        and the value is a tuple containing the indices and the associated pagerank scores
        index 0: paper_index
        index 1: paper_score
        """
        print("iteration {}".format(iteration))
        print("scores {}".format(paper_score))
        print("papers {}".format(paper_index))
        self.pagerank_log[iteration] = (paper_index,paper_score)

    def print_log(self):
        for i in self.pagerank_log.keys():
            scores = zip(self.pagerank_log[i][0], self.pagerank_log[i][1])
            print("iteration {} had the following:".format(i))
            for s in scores:
                print("{}   :   {}".format(s[0],s[1]))

    def proportions_of_final_rank_per_iteration(self):
        final_rank = set()
        sorted_keys = sorted(self.pagerank_log.keys())
        final_key = sorted_keys[-1]
        for paper in self.pagerank_log[final_key][0]:
            final_rank.add(paper)
        print(final_rank)
        results = [0 for i in range(len(sorted_keys))]
        for key in sorted_keys[:-1]:
            count = 0
            for paper in self.pagerank_log[key][0]:
                if paper in final_rank:
                    count += 1
            results[key] = count/len(final_rank)
            print("iteration {} had this proportion in final ranking: {}".format(key, count/len(final_rank)))
        return results

    def add_result_to_chart(self, results, label):
        plt.plot(results, label=label)
        # self.handles.append(label)

    def show_chart(self, alpha, tolerance, top_p_rank, beta=None):
        if beta:
            title_string = "beta : {}, alpha: {}, tolerance: {}, top_p_rank: {}".format(beta, alpha, tolerance, top_p_rank)
        else:
            title_string = "alpha: {}, tolerance: {}, top_p_rank: {}".format(alpha, tolerance, top_p_rank)
        plt.title('proportion of final ranking present at each iteration. ' + title_string)
        plt.xlabel('iteration #')
        plt.ylabel('proportion')
        plt.legend(loc=4)
        plt.show()

    def ranking(self, p_score, iteration, log):
        """
        get intermediate pagerank and log the results
        """
        print("paper rank at iteration: {}".format(iteration))
        unranked_list_papers = p_score.reshape(1,len(self.graph))[0]
        indices_of_top_ranked_papers = heapq.nlargest(self.top_p_rank,
                                                      xrange(len(unranked_list_papers)),
                                                      unranked_list_papers.__getitem__)
        #get the pagerank score for each of the papers in the specified indices
        score_of_top_ranked_papers = np.take(unranked_list_papers, indices_of_top_ranked_papers)
        print("score of top ranked papers: {}".format(score_of_top_ranked_papers))
        self.save_intermediate_ranking(indices_of_top_ranked_papers, score_of_top_ranked_papers, iteration)

