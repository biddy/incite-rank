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

    def temporal_statistics(self, experiment_name):
        #generate dummy data as a standin
        # np.random.seed(0)
        # mean_year = np.random.randint(100, size=(1,640000))[0] + 1900
        # np.random.seed(1)
        # pub_subtraction = np.random.randint(30, size=(1,640000))[0]
        # pub_year = mean_year - pub_subtraction
        # np.random.seed(2)
        # num_cit = np.random.randint(100, size=(1,640000))[0]+ 1900
        # z = zip(mean_year,pub_year,num_cit)
        # dummy_dict = {i: {"my":z[i][0],"py":z[i][1],"nc":z[i][2]} for i in range(640000)}
        #create arrays to hold these statistics for each node in the top_p_rank
        mean_year_citation = []
        pub_year = []
        num_in_citation = []
        last_iteration = sorted(self.experiment_results[experiment_name].keys())[-1]
        for node in self.experiment_results[experiment_name][last_iteration][0]:
            #These will be passed in as a dict where the node is the key
            mean_year_citation.append(self.dataset_info_temporal[node][0])
            pub_year.append(self.dataset_info_temporal[node][1])
            num_in_citation.append(self.dataset_info_temporal[node][2])
            # mean_year_citation.append(dummy_dict[node]["my"])
            # pub_year.append(dummy_dict[node]["py"])
            # num_in_citation.append(dummy_dict[node]["nc"])
        avg_my = sum(mean_year_citation)/len(mean_year_citation)
        avg_py = sum(pub_year)/len(pub_year)
        avg_nc = sum(num_in_citation)/len(num_in_citation)
        print(avg_my, avg_py, avg_nc)
        return avg_my, avg_py, avg_nc

    def academic_statistics(self, experiment_name):
        np.random.seed(0)
        num_in_citation = np.random.randint(100, size=(1,640000))[0]
        np.random.seed(1)
        num_in_collaboration = np.random.randint(100, size=(1,640000))[0]
        z = zip(num_in_citation,num_in_collaboration)
        dummy_dict = {i: {"ci":z[i][0],"co":z[i][1]} for i in range(640000)}
        mean_citations = []
        mean_collaborations = []
        last_iteration = sorted(self.experiment_results[experiment_name].keys())[-1]
        for node in self.experiment_results[experiment_name][last_iteration][0]:
            #These will be passed in as a dict where the node is the key
            mean_citations.append(dummy_dict[node]["ci"])
            mean_collaborations.append(dummy_dict[node]["co"])
        avg_ci = sum(mean_citations)/len(mean_citations)
        avg_co = sum(mean_collaborations)/len(mean_collaborations)
        return avg_ci, avg_co

    def chart_academic(self):
        chart = {}
        handles = []
        names = ["number_in_citation", "number_in_collbaroation"]
        for experiment in self.experiment_results.keys():
            num_in_citation, num_in_collaboration = self.academic_statistics(experiment)
            beta = float(experiment.split("#")[0].split(":")[1]) #this is manually hacked in. Figure out a more
            # elegant method if we have time: experiment_name in the following form beta:foo_num#tolerance:bar_num
            chart[beta] = [num_in_citation, num_in_citation]
        for i in range(2):
            data = {"x":[], "y":[], "label":[]}
            for key, coord in chart.items():
                data["x"].append(key)
                data["y"].append(coord[i])
            plt.plot(data["x"], data["y"], label=names[i])
            handles.append(names[i])
        plt.legend()
        plt.title("academic")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def chart_temporal(self, dataset_info_temporal):
        self.dataset_info_temporal = dataset_info_temporal
        chart = {}
        handles = []
        names = ["avg_year_cit", "avg_pub_year", "avg_num_in_citation"]
        for experiment in self.experiment_results.keys():
            avg_mean_year_cit, avg_pub_year, avg_num_in_citation = self.temporal_statistics(experiment)
            gamma = float(experiment.split("#")[0].split(":")[1])
            chart[gamma] = [avg_mean_year_cit, avg_pub_year, avg_num_in_citation]
            print(gamma, avg_mean_year_cit, avg_pub_year, avg_num_in_citation)
        plot_one = plt.figure(1)
        for i in range(2):
            data = {"x":[], "y":[], "label":[]}
            for key in sorted(chart.keys()):
                data["x"].append(key)
                data["y"].append(chart[key][i])
            plt.plot(data["x"], data["y"], label=names[i])
            handles.append(names[i])
        plt.title("average year of citations and average published year")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plot_one.show()
        plot_two = plt.figure(2)
        data = {"x":[], "y":[], "label":[]}
        for key in sorted(chart.keys()):
            data["x"].append(key)
            data["y"].append(chart[key][2])
        plt.plot(data["x"], data["y"], label=names[2])
        handles.append(names[2])
        plt.title("average number in citation")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plot_two.show()
        plt.show()

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

