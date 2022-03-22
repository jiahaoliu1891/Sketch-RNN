from genericpath import exists
import os, sys
import numpy as np
import pandas as pd
import networkx as nx
import pickle
from collections import defaultdict

'''
global variabke
'''
CENTER_X = 256//2
CENTER_Y = 256//2
GRAPH_PATH = "./data/graph/"
NUMPY_PATH = "./data/numpy/"



'''
FULLY CONNECTED GRAPH MODEL
-------------------------------
DEF: class to construct graph for each sketch
INPUT: one sketch
OUTPUT: the graph for the sketch
'''
class Graph:
    def __init__(self, sketch):
        self.stroke_list = sketch
        self.node_num = len(sketch)+1 # number of strokes in sketch + hyper node
        self.edge_num = self.node_num*(self.node_num-1) # number of strokes in sketch: directed
        self.nodes = self.form_nodes() # node np array, [node_num, 2]
        self.edges = self.form_edges() # edge dict, {from_node: {to_node: [offset_x, offset_y]}}
        self.adj_matrix = self.form_adj_matrix() # adjacent matrix, np array, [node_num, node_num, offset_dim]

    def form_nodes(self):
        nodes = np.zeros((self.node_num, 2))
        for idx, stroke in enumerate(self.stroke_list):
            nodes[idx] = np.mean(stroke, axis = 1)
        nodes[-1] = np.array([CENTER_X, CENTER_Y])
        return nodes

    def form_edges(self):
        edge_dict = defaultdict(dict)
        for node1_idx in range(self.node_num):
            for node2_idx in range(node1_idx+1, self.node_num):
                edge_dict[node1_idx][node2_idx] = self.nodes[node1_idx] - self.nodes[node2_idx]
                edge_dict[node2_idx][node1_idx] = self.nodes[node2_idx] - self.nodes[node1_idx]
        return edge_dict

    def form_adj_matrix(self):
        adj_matrix = np.zeros((self.node_num, self.node_num, 2))
        for node1_idx in range(self.node_num):
            for node2_idx in range(node1_idx+1, self.node_num):
                adj_matrix[node1_idx][node2_idx] = self.edges[node1_idx][node2_idx]
                adj_matrix[node2_idx][node1_idx] = self.edges[node2_idx][node1_idx]
        return adj_matrix

    def get_node_num(self):
        return self.node_num
    
    def get_edge_num(self):
        return self.edge_num

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def get_adj_matrix(self):
        return self.adj_matrix


def load_numpy(category):
    with open(f'data/numpy/{category}', 'rb') as f:
        cur_list = pickle.load(f)
    return cur_list


def store_graph_data(category_list):
    graph_dict = defaultdict(list)

    for cate in category_list[1:]:
        sketchs = load_numpy(cate)
        cate = cate[:-4]
        for sketch in sketchs:
            graph = Graph(sketch)
            graph_dict[cate].append({"adj_matrix":graph.get_adj_matrix(), "nodes":graph.get_nodes()})
        with open(f'{GRAPH_PATH}/{cate}_graph.npy', 'wb') as f:
            pickle.dump(graph_dict[cate], f)
    f.close()


def main(argv):
    category_list = os.listdir(NUMPY_PATH)

    # graph not exists: construct the graph
    if len(os.listdir(GRAPH_PATH)) <= 1:
        store_graph_data(category_list)

    # graph exist: get your target graph
    with open(f'data/graph/bench_graph.npy', 'rb') as f:
        graph_list = pickle.load(f)
    
    # information explanation: use bench as exm
    print(f'# Nodes in the 1st sketch is {graph_list[0]["nodes"]}, with shape {graph_list[0]["nodes"].shape}.')
    print(f'# Adj Matrix in the 1st sketch is {graph_list[0]["adj_matrix"]}, with shape {graph_list[0]["adj_matrix"].shape}.')
    print(f'# Offset of 1st node to center point is {graph_list[0]["adj_matrix"][0][-1]}')

    

if __name__ == "__main__":
    main(sys.argv)

