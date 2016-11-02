from __future__ import division
import heapq

import numpy as np
import matplotlib.pyplot as plt


class Logging:

    def __init__(self, top_p_rank):
        self.top_p_rank = top_p_rank
        self.pagerank_log = dict()
        self.experiment_results = dict() #save the experiment results using the experiment name as the key

    def save_intermediate_ranking(self, k_top_paper_indices, k_top_paper_scores, iteration, experiment_tag):
        """
        intermediate results are saved in a dict where the key is the iteration number
        and the value is a tuple containing the indices and the associated pagerank scores
        index 0: paper_index
        index 1: paper_score
        """
        print("iteration {}".format(iteration))
        print("scores {}".format(k_top_paper_scores))
        print("papers {}".format(k_top_paper_indices))
        values = (k_top_paper_indices, k_top_paper_scores)
        self.create_key_or_add_to_dict(self.experiment_results, experiment_tag, iteration, values)
        # self.experiment_results[experiment_tag][iteration] = (paper_index, paper_score)
        # self.pagerank_log[iteration] = (paper_index,paper_score)

    def create_key_or_add_to_dict(self, dictionary, key1, key2, value):
        try:
            dictionary[key1][key2] = value
        except:
            print('creating dict. key {}, key2 {}'.format(key1, key2))
            dictionary[key1] = dict()
            dictionary[key1][key2] = value

    # def save_ranking_for_experiment(self, experiment_name):
    #     final_key = sorted(self.pagerank_log.keys())[-1]
    #     print(final_key)
    #     print(self.pagerank_log[final_key])
    #     self.experiment_results[experiment_name] = self.pagerank_log[final_key]

    def print_log(self):
        for i in self.pagerank_log.keys():
            scores = zip(self.pagerank_log[i][0], self.pagerank_log[i][1])
            print("iteration {} had the following:".format(i))
            for s in scores:
                print("{}   :   {}".format(s[0],s[1]))

    def proportions_of_final_rank_per_iteration(self, experiment_name):
        final_rank = set()
        # sorted_keys = sorted(self.pagerank_log.keys())
        pagerank_iteration_keys = sorted(self.experiment_results[experiment_name].keys())
        last_iteration = pagerank_iteration_keys[-1]
        for paper in self.experiment_results[experiment_name][last_iteration][0]:
            final_rank.add(paper)
        print(final_rank)
        results = [0 for i in range(len(pagerank_iteration_keys) + 1)]
        for iteration in pagerank_iteration_keys:
            count = 0
            for paper in self.experiment_results[experiment_name][iteration][0]:
                if paper in final_rank:
                    count += 1
            results[iteration] = count/len(final_rank)
            print("iteration {} had this proportion in final ranking: {}".format(iteration, count/len(final_rank)))
        return results

    def chart_proportions(self):
        handles = []
        for experiment in self.experiment_results.keys():
            result = self.proportions_of_final_rank_per_iteration(experiment)
            plt.plot(result, label=experiment)
            handles.append(experiment)
        plt.title('proportion of final ranking present at each iteration')
        plt.xlabel('iteration #')
        plt.ylabel('proportion')
        plt.legend(loc=4)
        plt.show()

    # def chart_proportions(self, results_and_labels, alpha, tolerance, top_p_rank, beta=None):
    #     figure1 = plt.figure(1)
    #     handles = [] #tags for the chart legend
    #     for res_lab in results_and_labels:
    #         # print(res_lab)
    #         # print(res_lab[0])
    #         # print(res_lab[1])
    #         plt.plot(res_lab[0], label=res_lab[1])
    #         handles.append(res_lab[1])
    #     if beta:
    #         title_string = "beta : {}, alpha: {}, tolerance: {}, top_p_rank: {}".format(beta, alpha, tolerance, top_p_rank)
    #     else:
    #         title_string = "alpha: {}, tolerance: {}, top_p_rank: {}".format(alpha, tolerance, top_p_rank)
    #     plt.title('proportion of final ranking present at each iteration. ' + title_string)
    #     plt.xlabel('iteration #')
    #     plt.ylabel('proportion')
    #     plt.legend(loc=4)
    #     plt.show()

    # def add_chart_information_proportions_chart(self, alpha, tolerance, top_p_rank, beta=None):
    #     if beta:
    #         title_string = "beta : {}, alpha: {}, tolerance: {}, top_p_rank: {}".format(beta, alpha, tolerance, top_p_rank)
    #     else:
    #         title_string = "alpha: {}, tolerance: {}, top_p_rank: {}".format(alpha, tolerance, top_p_rank)
    #     plt.title('proportion of final ranking present at each iteration. ' + title_string)
    #     plt.xlabel('iteration #')
    #     plt.ylabel('proportion')
    #     plt.legend(loc=4)
    #
    # def show_all_charts(self):
    #     plt.show()

    def ranking(self, p_score, iteration, experiment_tag):
        """
        get intermediate pagerank and log the results
        """
        print("paper rank at iteration: {}".format(iteration))
        # unranked_list_papers = p_score.reshape(1,graph_size)[0]
        unranked_list_papers = p_score.flatten()
        indices_of_top_ranked_papers = heapq.nlargest(self.top_p_rank,
                                                      xrange(len(unranked_list_papers)),
                                                      unranked_list_papers.__getitem__)
        #get the pagerank score for each of the papers in the specified indices
        score_of_top_ranked_papers = np.take(unranked_list_papers, indices_of_top_ranked_papers)
        print("score of top ranked papers: {}".format(score_of_top_ranked_papers))
        self.save_intermediate_ranking(indices_of_top_ranked_papers, score_of_top_ranked_papers, iteration, experiment_tag)

