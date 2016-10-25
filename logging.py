from __future__ import division


class Logging:

    def __init__(self):
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
            print("interation {} had the following:".format(i))
            for s in scores:
                print("{}   :   {}".format(s[0],s[1]))

    def proportions_of_final_rank_per_iteration(self):
        final_rank = set()
        sorted_keys = sorted(self.pagerank_log.keys())
        final_key = sorted_keys[-1]
        for paper in self.pagerank_log[final_key][0]:
            final_rank.add(paper)
        print(final_rank)
        for key in sorted_keys[:-1]:
            count = 0
            for paper in self.pagerank_log[key][0]:
                if paper in final_rank:
                    count += 1
            print("iteration {} had this proportion in final ranking: {}".format(key, count/len(final_rank)))


