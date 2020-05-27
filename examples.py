import os, sys

sys.path.insert(0, os.path.abspath('..'))

os.makedirs('examples', exist_ok = True)

from classes import FCGraph, GraphicalModel, plt


# FCNN
g = FCGraph(n_hidden = [4, 4], bias = True)
g.render()

plt.savefig('examples/fcnn-graph.png')


# Graphical Model (Gaussian Process)
g = GraphicalModel()

g.add_node('X', (0, 0), node_type = 'data')
g.add_node(r'\theta', (3, 3), node_type = 'variable', bold = False)
g.add_node('f', (3, 0), node_type = 'function', bold = False)
g.add_node('T', (6, 0), node_type = 'data')
g.add_node('\sigma^2', (6, 3), node_type = 'variable', bold = False)

g.add_connection('X', 'f')
g.add_connection(r'\theta', 'f')
g.add_connection('f', 'T')
g.add_connection(r'\sigma^2', 'T')

g.render()

plt.savefig('examples/graphical-model-graph.png', dpi = 100)

