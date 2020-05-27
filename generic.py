from   matplotlib import pyplot as plt

class Graph():
    """
    Simple Graph class designed to be inherited.
    
    Parameters
    =====================
        node_types       : dict
                           Expected format is {type : kwargs} where kwargs is a dictionary with key word arguments used in plt.Circle.
        
        connection_types : dict
                           Expected format is {type : kwargs} where kwargs is a dictionary with key word arguments used in plt.arrow.
        
        annot            : {False, int}
                           Annotation size. If False or 0, annotations will not appear when rendered.
                           
    Methods
    =====================
        add_node         : (name, xy, node_type, **kwargs)
                           Adds the node `name` to the graph at `xy` location with `node_type` string expected in `node_types`.
                           `kwargs` will be unpacked into plt.Circle.
                           
        add_connection   : (A, B, connection_type)
                           Adds a connection from node `A` to node `B` with `connection_type` string expected in `connection_types`.
                           
        render           : ()
                           Renders the graph.
                           
    """
    def __init__(self, node_types = dict(), connection_types = dict(), annot = 20):
        
        self._set(locals())
        
        self.nodes       = {}
        self.connections = {}
        
        self.node_types.update({None : {}})
        self.connection_types.update({None : {}})
        
    def _set(self, d, exceptions = ['self', '__class__']):
        """ Set attributes """
        for k, v in d.items():
            if k in exceptions: pass
            setattr(self, k, v)
            
    def _add_node(self, name, xy, node_type = None, **kwargs):
        assert name not in self.nodes
        self.nodes[name]       = plt.Circle(xy, **self.node_types[node_type], **kwargs)
        self.connections[name] = {}
        
    def _add_connection(self, A, B, connection_type = None):
        assert A in self.nodes and B in self.nodes
        self.connections[A][B] = self.connection_types[connection_type]
        
    def _gen_label(self, base, *args, bold = True):
        ix = ','.join(map(str, args))
        return '$\mathbf{' + str(base) + '}_{' + ix + '}$' if bold else f'${base}_' + '{' + ix + '}$' if ix else f'${base}$'
    
    def _render(self):
        x, y = [[0, 0], [0, 0]]
        for node in self.nodes.values():
            x[0] = min(x[0], node.center[0] - node.radius)
            x[1] = max(x[1], node.center[0] + node.radius)
            y[0] = min(y[0], node.center[1] - node.radius)
            y[1] = max(y[1], node.center[1] + node.radius)
            
        fig = plt.figure(figsize = (x[1] - x[0], y[1] - y[0]))
        ax  = fig.add_subplot(111)
        
        for name, node in self.nodes.items():
            ax.add_patch(node)
            ax.annotate(node.get_label(), node.center, ha = 'center', va = 'center', size = self.annot)
            
        for A, D in self.connections.items():
            for B, kwargs in D.items():
                delta  = [b - a for a, b in zip(self.nodes[A].center, self.nodes[B].center)]
                dist   = sum(d ** 2 for d in delta) ** 0.5
                unit   = [d / dist for d in delta]
                x, y   = [z + self.nodes[A].radius * u for z, u in zip(self.nodes[A].center, unit)]
                diff   = dist - self.nodes[A].radius - self.nodes[B].radius
                dx, dy = [u * diff for u in unit] 
                plt.arrow(x, y, dx, dy, **kwargs)
        
        ax.relim()
        ax.autoscale_view()
        ax.axis('off')
        
    def add_node(self, name, xy, node_type = None, **kwargs):
        self._add_node(self, name, xy, node_type = None, **kwargs)
        
    def add_connection(self, A, B, connection_type = None):
        self._add_connection(self, A, B, connection_type = None)
        
    def render(self):
        self._render()
