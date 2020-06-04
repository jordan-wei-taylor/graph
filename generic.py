from matplotlib import pyplot as plt

class Circle():
    """
    Circle class similar to plt.Circle and mpl.patches.Wedge (for two semi-circles).
    
    Parameters
    ================
        xy          : tuple, list
                      Center location of circle.
                      
        radius      : int, float
                      Radius of circle.
                      
        ec          : str, tuple, list
                      The edge colour of the circle. See https://matplotlib.org/3.1.1/tutorials/colors/colors.html for more details.
                      
        fc          : str, tuple, list
                      The face colour of the circle.
                      
        orientation : str
                      If "v" and `semi` = True, then lines drawn are relative to the north vector line.
                      
        label       : str
                      Label of circle to be used with plt.annotate.
                      
        semi        : bool, int
                      If `evaluated to not `False`, then use mpl.patches.Wedge to create two wedges to complete a circle.
                      
        kwargs      : kwargs for mpl.patches.Wedge if `semi` else plt.Circle.
        
        
    Methods
    ================
        add         : (ax,)
                      Given an axes object `ax`, calls the ax.add_patch method with annotations if `label` was provided in the init.
    """
    def __init__(self, xy, radius, ec = 'k', fc = 'none', orientation = 'v', label = None, semi = False, **kwargs):
        assert orientation in 'vh'
        if isinstance(semi, bool) and semi:
            semi = 90
        o = orientation == 'h'
        for key, value in locals().items():
            if key in ['self', '__class__']: continue
            setattr(self, key, value)
        
        if 'annot_size' in kwargs:
            del kwargs['annot_size']
            
        if semi:
            if isinstance(kwargs, dict):
                kwargs = kwargs.copy(), kwargs.copy()
        
            for var in ['label', 'ec', 'fc']:
                if not isinstance(locals().get(var), (tuple, list)):
                    for i in range(2):
                        kwargs[i][var] = locals().get(var)
                else:
                    for i in range(2):
                        kwargs[i][var] = locals().get(var)[i]
            
            self.l = plt.matplotlib.patches.Wedge(xy, radius, semi * (1 - o), (360 - semi) * (1 + o), **kwargs[0])
            self.r = plt.matplotlib.patches.Wedge(xy, radius, (360 - semi) * (1 + o), semi * (1 - o), **kwargs[1])
        else:
            self.c = plt.Circle(xy, radius, ec = ec, fc = fc, label = label, **kwargs)
            
        self.center = xy
        
    def add(self, ax):
        if self.semi:
            ax.add_patch(self.l)
            ax.add_patch(self.r)
            l      = self.center[0] - (0 if self.o else self.radius / 2), self.center[1] - (self.radius / 2 if self.o else 0)
            r      = self.center[0] + (0 if self.o else self.radius / 2), self.center[1] + (self.radius / 2 if self.o else 0)
            for i, obj in enumerate([self.l, self.r]):
                plt.annotate(obj.get_label(), [l, r][i], ha = 'center', va = 'center', size = self.annot_size)
        else:
            ax.add_patch(self.c)
            plt.annotate(self.label, self.center, ha = 'center', va = 'center', size = self.annot_size)

def arrow(x, y, dx, dy, twin = False, **kwargs):
    """ Wrapper function for plt.arrow """
    if twin == 2:
        for key, value in kwargs.copy().items():
            if not isinstance(value, (list, tuple)):
                kwargs[key] = (value, value)
        k1, k2      = [{key : kwargs[key][i] for key in kwargs} for i in range(2)] 
        head_width  = k1['head_width' ] if 'head_width' in k1 else 0.003 # plt.arrow default value
        head_length = k1['head_length'] if 'head_length' in k1 else head_width * 1.5 # plt.arrow default value
        for key in ['head_width', 'head_length']:
            for k in [k1, k2]:
                if key in k:
                    del k[key]
        plt.arrow(x, y, dx, dy, shape = 'left', head_width = head_width, head_length = head_length, **k1)
        plt.arrow(x + dx, y + dy, -dx, -dy, shape = 'right', head_width = -head_width, head_length = head_length, **k2)
    elif twin == 1:
        for key, value in kwargs.copy().items():
            if not isinstance(value, (list, tuple)):
                kwargs[key] = (value, value)
        k1, k2      = [{key : kwargs[key][i] for key in kwargs} for i in range(2)] 
        head_width  = k1['head_width' ] if 'head_width' in k1 else 0.003
        head_length = k1['head_length'] if 'head_length' in k1 else head_width * 1.5
        for key in ['head_width', 'head_length']:
            for k in [k1, k2]:
                if key in k:
                    del k[key]
        plt.arrow(x, y, dx, dy)
        d   = (dx ** 2 + dy ** 2) ** 0.5
        l   = head_length
        dx /= d
        dy /= d
        plt.arrow(x + dx * (d - l), y + dy * (d - l), l * dx, l * dy, head_width = head_width, head_length = l, **k1)
        plt.arrow(x + dx * l, y + dy *l, -l * dx, -l * dy, head_width = head_width, head_length = l, **k2)
    else:
        plt.arrow(x, y, dx, dy, **kwargs)
        
class Graph():
    """
    Simple Graph class designed to be inherited.
    
    Parameters
    =====================
        node_types       : dict
                           Expected format is {type : kwargs} where kwargs is a dictionary with key word arguments used in Circle (plt.Circle).
        
        connection_types : dict
                           Expected format is {type : kwargs} where kwargs is a dictionary with key word arguments used in arrow (plt.arrow).
                           
        rectangle_types  : dict
                           Expected format is {type : kwargs} where kwargs is a dictionary with key word arguments used in plt.Rectangle.
        
        annot            : {False, int}
                           Annotation size. If False or 0, annotations will not appear when rendered.
                           
    Methods
    =====================
        add_node         : (name, xy, node_type, **kwargs)
                           Adds the node `name` to the graph at `xy` location with `node_type` string expected in `node_types`. `kwargs` will
                           be unpacked into plt.Circle.
                           
        add_connection   : (A, B, connection_type)
                           Adds a connection from node `A` to node `B` with `connection_type` string expected in `connection_types`.
                           
        add_rectangle    : (name, xy, width, height, rectangle_type, label_position, **kwargs)
                           Addes the rectangle `name` to the graph with the bottom left corner at `xy` with `width`, and `height`. If rectangle
                           type provided, find the relating `kwargs` to unpack. If `label_position` provided, display label at `label_position`
                           otherwise the center. `kwargs` will be unpacked into plt.Rectangle.
                           
        render           : ()
                           Renders the graph.
                           
    """
    def __init__(self, node_types = dict(), connection_types = dict(), rectangle_types = dict(), annot = 20):
        
        self._set(locals())
        
        self.nodes       = {}
        self.rectangles  = {}
        self.connections = {}
        
        for d in [self.node_types, self.connection_types, self.rectangle_types]:
            d.update({None : {}})
                                    
    def _set(self, d, exceptions = ['self', '__class__']):
        """ Set attributes """
        for k, v in d.items():
            if k in exceptions: pass
            setattr(self, k, v)
            
    def _add_node(self, name, xy, node_type = None, vertical = False, connect_to = None, connect_from = None, connection_type = None, **kwargs):
        assert name not in self.nodes
        c                      = Circle(xy[::-1] if vertical else xy, **self.node_types[node_type], **kwargs)
        c.annot_size           = kwargs['annot_size'] if 'annot_size' in kwargs else self.annot # override if given
        self.nodes[name]       = c
        self.connections[name] = {}
        
        # Make iterable
        if isinstance(connect_to, str):
            connect_to   = [connect_to]
        if isinstance(connect_from, str):
            connect_From = [connect_from]
            
        # Loop both connections to and from `name`
        for order, connections in zip((1,-1), (connect_to, connect_from)):
            if connections:
                for connection in connections:
                    self._add_connection(*(connection, name)[::order], connection_type = connection_type)
        
    def _add_connection(self, A, B, connection_type = None):
        assert A in self.nodes and B in self.nodes
        self.connections[A][B] = self.connection_types[connection_type]
        
    def _add_rectangle(self, name, xy, width, height, rectangle_type = None, label_position = None, **kwargs):
        assert name not in self.rectangles
        r = plt.Rectangle(xy, width, height, **self.rectangle_types[rectangle_type], **kwargs)
        r.label_position = (xy[0] + width / 2, xy[1] + height / 2) if label_position is None else label_position
        self.rectangles[name] = r
        
    def _gen_label(self, base, *args, bold = True):
        ix = ','.join(map(str, args))
        return '$\mathbf{' + str(base) + '}_{' + ix + '}$' if bold else f'${base}_' + '{' + ix + '}$' if ix else f'${base}$'
            
    def _render(self):
        x, y = [[0, 0], [0, 0]]
        
        for r in self.rectangles.values():
            x[0] = min(x[0], r.get_x())
            x[1] = max(x[0], r.get_x() + r.get_width())
            y[0] = min(y[0], r.get_y())
            y[1] = max(y[0], r.get_y() + r.get_height())
            
        for n in self.nodes.values():
            x[0] = min(x[0], n.center[0] - n.radius)
            x[1] = max(x[1], n.center[0] + n.radius)
            y[0] = min(y[0], n.center[1] - n.radius)
            y[1] = max(y[1], n.center[1] + n.radius)
            
        fig = plt.figure(figsize = (x[1] - x[0], y[1] - y[0]))
        ax  = fig.add_subplot(aspect = 'equal')
        
        for name, rect in self.rectangles.items():
            ax.add_patch(rect)
            plt.annotate(rect.get_label(), rect.label_position, ha = 'center', va = 'center', size = self.annot)
        
        for name, node in self.nodes.items():
            node.add(ax)
            
        for A, D in self.connections.items():
            for B, kwargs in D.items():
                delta  = [b - a for a, b in zip(self.nodes[A].center, self.nodes[B].center)]
                dist   = sum(d ** 2 for d in delta) ** 0.5
                unit   = [d / dist for d in delta]
                x, y   = [z + self.nodes[A].radius * u for z, u in zip(self.nodes[A].center, unit)]
                diff   = dist - self.nodes[A].radius - self.nodes[B].radius
                dx, dy = [u * diff for u in unit] 
                arrow(x, y, dx, dy, **kwargs)
        
        ax.relim()
        ax.autoscale_view()
        ax.axis('off')
        
        self.ax = ax
        
        return self
    
    def add_node(self, name, xy, node_type = None, **kwargs):
        self._add_node(name, xy, node_type, **kwargs)
        
    def add_connection(self, A, B, connection_type = None):
        self._add_connection(A, B, connection_type)
        
    def add_rectangle(self, name, xy, width, height, rectangle_type = None, **kwargs):
        self._add_rectangle(name, xy, width, height, rectangle_type, **kwargs)
                            
    def render(self):
        return self._render()