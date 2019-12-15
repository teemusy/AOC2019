import networkx as nx
import matplotlib.pyplot as plt


def main():
    f = open("../14_input.txt", "r")
    reactions = f.readlines()
    f.close()

    # create objects for reactions
    reaction_list = []
    #print(reactions)

    G = nx.Graph()

    G.add_edge(1, 2, weight=4.7)
    G.add_edges_from([(3, 4), (4, 5)], color='red')
    G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
    G[1][2]['weight'] = 4.7
    G.edges[3, 4]['weight'] = 4.2

    nx.draw(G, with_labels=True, font_weight='bold')
    #nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()



if __name__ == '__main__':
    main()