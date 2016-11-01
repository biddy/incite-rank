from __future__ import division
import sys
import numpy as np
import heapq

def dict_sum(dt):
    total = 0.0
    for k in dt:
        total += dt[k]
    return total

def dict_normalize(dt):
    row_sum = dict_sum(dt)
    #print(row_sum)
    for k in dt:
        dt[k] = dt[k] / row_sum

def normalize(graph):
    """assumes input is a list of row-dictionaries, returns same dictionaries but row-normalized"""
    for n in graph:
        dict_normalize(n)

def add_datasets(d1, d2, beta = 1.0):
    if len(d1) != len(d2):
        return None
    print('combining datasets')
    dataset = []
    for dt in d1:
        dataset.append(dt.copy())
    for i in range(len(d2)):
        dt1 = dataset[i]
        dt2 = d2[i]
        for k in dt2:
            if k in dt1:
                dt1[k] = dt1[k] + (dt2[k]*beta)
            else:
                dt1[k] = dt2[k]*beta
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

def pagerank_iteration(reverse_graph, dangling, p, alpha = 0.85, debug = False):
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
        # if debug and column % 100000 == 0:
        #     print('nodes completed: ' + str(column))
    return p_prime

def find_pagerank(graph, dangling_nodes, nodes, log, alpha = 0.85, tolerance = 0.0001, debug = False):
    # nodes = len(graph)
    m = 1/nodes
    if debug: print('building initial probability')
    p = np.full(nodes, m)
    if debug: print('iteration: 1')
    # p_new = pagerank_iteration(graph, dangling_nodes, p, alpha, debug)
    # diff = np.sum(np.absolute(p - p_new))
    # if debug: print('diff: ' + str(diff))
    # p = p_new
    iterations = 1
    diff = 2
    while(diff > tolerance):
        if debug: print('iteration: ' + str(iterations))
        p_new = pagerank_iteration(graph, dangling_nodes, p, alpha, debug)
        diff = np.sum(np.absolute(p - p_new))
        p = p_new
        log.ranking(p, iterations, log)
        if debug: print('diff: ' + str(diff))
        iterations += 1
    if debug: print("iterations required: " + str(iterations))
    return p

def pagerank(forward_graph, log, alpha=0.85, tolerance=0.0001, debug=False):
    graph_size = len(forward_graph)
    if debug: print('building reverse graph')
    graph_backward, graph_dangling = create_backward_graph(forward_graph)
    print(alpha, tolerance)
    if debug: print('initiating pagerank calculation... this may take a while!')
    return find_pagerank(graph_backward, graph_dangling, graph_size, log, alpha, tolerance, debug)

