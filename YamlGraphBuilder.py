import os
from graphviz import Digraph
import sys


class GraphNode:
    def __init__(self, id, name, in_put, out_put, dependent=None):
        self.id = id
        self.name = name
        self.in_put = in_put
        self.out_put = out_put
        self.dependent = dependent


def build_graph(filename):
    # store all graph nodes
    graph_list = []
    # store all edges info
    edges_list = []
    # store all dependent edges info
    dependent_edges_list = []
    # store all input data info
    input_list = []

    # read and parser yaml file
    with open(os.getcwd() + "/yaml/" + filename) as f:
        model_info = f.read().split("model:")[-1]
        layer_info = model_info.split("-")
        for i in range(len(layer_info)):
            layer_info[i] = layer_info[i].split("\n")
        for i in range(len(layer_info)):
            for j in range(len(layer_info[i])):
                if "#" in layer_info[i][j]:
                    layer_info[i][j] = layer_info[i][j][:layer_info[i][j].index("#")]
                if ":" not in layer_info[i][j]:
                    layer_info[i][j] = ""
                layer_info[i][j] = layer_info[i][j].replace(" ", "")
        new_layer_info = []
        for i in range(len(layer_info)):
            tmp = []
            for j in range(len(layer_info[i])):
                if layer_info[i][j]:
                    tmp.append(layer_info[i][j])
            new_layer_info.append(tmp)
        count = 1
        for i in range(len(new_layer_info)):
            dict1 = {}
            for j in range(len(new_layer_info[i])):
                if ":" in new_layer_info[i][j]:
                    key = new_layer_info[i][j].split(":")[0]
                    value = new_layer_info[i][j].split(":")[1]
                    if key not in dict1 and (key == "input"
                                             or key == "output" or key == "module" or key == "dependent"):
                        dict1[key] = eval(value)
            new_layer_info[i] = dict1
            if dict1:
                if 'output' not in dict1:
                    dict1['output'] = dict1['input']
                if type(dict1['input']) is not list:
                    dict1['input'] = [dict1['input']]
                if 'dependent' in dict1 and type(dict1['dependent']) is not list:
                    dict1['dependent'] = [dict1['dependent']]
                # if 'dependent' in dict1:
                #     dict1['input'].extend(dict1['dependent'])
                tmp_node = GraphNode(id=count, name=dict1['module'], in_put=dict1['input'],
                                     out_put=dict1['output'])
                if 'dependent' in dict1:
                    tmp_node.dependent = dict1['dependent']
                graph_list.append(tmp_node)
                count += 1
        # print("After text transformation, the following structure has been extracted from yaml file:")
        # print(new_layer_info)
        print("All nodes in the graph:")
        for i in graph_list:
            print(i.name)
        # generate all edges
        output_dict = {}
        for i in range(len(graph_list)):
            is_head = False
            for j in graph_list[i].in_put:
                if j not in output_dict:
                    is_head = True
                    input_list.append(graph_list[i])
                    break
            if is_head:
                output_dict[graph_list[i].out_put] = graph_list[i]
                continue
            if not is_head:
                for j in graph_list[i].in_put:
                    edges_list.append((output_dict[j], graph_list[i]))
                if graph_list[i].dependent:
                    for j in graph_list[i].dependent:
                        dependent_edges_list.append((output_dict[j], graph_list[i]))
            # update output_dict
            output_dict[graph_list[i].out_put] = graph_list[i]
    # Upper letters for module nodes and lower letters for input data
    dot = Digraph(comment='The Recurrent Neural Network Graph')
    # dot.graph_attr.update(label=filename.split('.')[0])
    for node in graph_list:
        dot.node(chr(node.id+64), node.name, fontcolor="white", style="filled", fillcolor="blue")
    # draw the input data on NN graph.
    for node in input_list:
        count = 1
        for input_str in node.in_put:
            input_node_name = chr(node.id+96)+str(count)
            dot.node(input_node_name, input_str, shape="box", fontcolor="white", style="filled", fillcolor="red")
            dot.edge(input_node_name, chr(node.id+64), color="red")
            # dot.edge_attr.update(style="dashed")
            count += 1
    edges_showed = []
    for i in edges_list:
        dot.edge(chr(i[0].id + 64), chr(i[1].id + 64), color="blue")
        tmp_showed = i[0].name + "-" + i[1].name
        edges_showed.append(tmp_showed)
    for i in dependent_edges_list:
        dot.edge(chr(i[0].id + 64), chr(i[1].id + 64), color="blue", style="dashed")
        tmp_showed = i[0].name + "-" + i[1].name
        edges_showed.append(tmp_showed)
    print("All edges in the graph:")
    print(edges_showed)
    dot.view('graph-output/' + filename)

if __name__ == '__main__':
    build_graph(str(sys.argv[1]))
