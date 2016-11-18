from __future__ import division
import numpy as np

def dict_sum(dt):
    total = 0.0
    for k in dt:
        total += dt[k]
    return total

def dict_normalize(dt):
    row_sum = dict_sum(dt)
    for k in dt:
        dt[k] = dt[k] / row_sum

def normalize(graph):
    """assumes input is a list of row-dictionaries, returns same dictionaries but row-normalized"""
    for n in graph:
        dict_normalize(n)

def add_datasets(citations, collaborations, beta = 1.0):
    """
    this combines the citations and collaborations into a single dataset using the specified beta parameter
    """
    if len(citations) != len(collaborations):
        return None
    print('combining datasets')
    dataset = []
    for dt in citations:
        d_temp = dt.copy()
        for k in d_temp:
            d_temp[k] = d_temp[k]*beta
        dataset.append(d_temp)
    for i in range(len(collaborations)):
        dt1 = dataset[i]
        dt2 = collaborations[i]
        for k in dt2:
            if k in dt1:
                dt1[k] = dt1[k] + (dt2[k]*(1-beta))
            else:
                dt1[k] = dt2[k]*(1-beta)
    return dataset

def create_backward_graph(forward_graph):
    nodes = len(forward_graph)
    general_p = 1/nodes
    reverse_graph = {}
    dangling_nodes = []
    for k in range(len(forward_graph)):
        values = forward_graph[k]
        for value in values:
            rev = None
            if value in reverse_graph:
                rev = reverse_graph[value]
            else:
                rev = {}
                reverse_graph[value] = rev
            rev[k] = values[value]
        if len(values) == 0:
            dangling_nodes.append(k)
    return reverse_graph, dangling_nodes

def pagerank_common_factor(p, alpha):
    multiplier = (1-alpha)/len(p)
    return np.sum(p*multiplier)

def pagerank_iteration(reverse_graph, dangling, p, alpha, debug):
    nodes = len(p)
    general_p = 1/nodes
    factor = pagerank_common_factor(p, alpha)
    for row in dangling:
        factor += alpha*general_p*p[row]
    if debug: print('factor: ' + str(factor))
    p_prime = np.zeros(nodes)
    for column in range(nodes):
        p_temp = factor
        if column in reverse_graph:
            reverse_map = reverse_graph[column]
            for row in reverse_map:
                p_temp += alpha*reverse_map[row]*p[row]
        p_prime[column] = p_temp
    return p_prime

def find_pagerank(graph, dangling_nodes, nodes, log, experiment_tag, alpha, tolerance, debug):
    m = 1/nodes
    p = np.full(nodes, m)
    iterations = 1
    diff = 2
    if debug: print('executing pagerank using alpha: {} , tolerance: {}'.format(alpha, tolerance))
    if debug: print('building initial probability')
    if debug: print('iteration: 1')
    while(diff > tolerance):
        if debug: print('iteration: ' + str(iterations))
        p_new = pagerank_iteration(graph, dangling_nodes, p, alpha, debug)
        diff = np.sum(np.absolute(p - p_new))
        p = p_new
        log.ranking(p, iterations, experiment_tag)
        if debug: print('diff: ' + str(diff))
        iterations += 1
    if debug: print("iterations required: " + str(iterations-1))
    return p

def pagerank(forward_graph, log, experiment_tag, alpha=0.85, tolerance=0.01, debug=False):
    graph_size = len(forward_graph)
    if debug: print('building reverse graph')
    graph_backward, graph_dangling = create_backward_graph(forward_graph)
    if debug: print('initiating pagerank calculation... this may take a while!')
    return find_pagerank(graph_backward, graph_dangling, graph_size, log, experiment_tag, alpha, tolerance, debug)

