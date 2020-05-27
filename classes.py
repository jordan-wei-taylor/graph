from generic import Graph, plt

arrow_kwargs  = dict(head_width = 0.2, fc = 'k', length_includes_head = True)
input_kwargs  = dict(ec = 'k', fc = 'tab:green')
hidden_kwargs = dict(ec = 'k', fc = 'tab:blue')
output_kwargs = dict(ec = 'k', fc = 'tab:orange')
bias_kwargs   = dict(alpha = 0.5, ls = (0, (5, 5)))

class FCGraph(Graph):
    """
    Fully-Connected Neural Network (FCNN) Graph (Graph)
    
    Parameters
    ==================
        n_input       : int
                        No. of inputs units.
                        
        n_hidden      : list of ints
                        No. of hidden units in each hidden layer
                        
        n_output      : int
                        No. of output units.
                        
        v_space       : float
                        Vertical space between node centers.
                        
        h_space       : float
                        Horizontal space between node centers.
                        
        radius        : float
                        Radius of all units.
                        
        annot         : {False, int}
                        Annotation size. If False or 0, annotations will not appear when rendered.
                           
        bias          : bool
                        If True, adds bias units.
                        
        input_kwargs  : dict
                        Dictionary describing how the input units should be drawn using plt.Circle.
                        
        hidden_kwargs : dict
                        Dictionary describing how the hidden units should be drawn using plt.Circle.
                        
        output_kwargs : dict
                        Dictionary describing how the output units should be drawn using plt.Circle.
                        
        arrow_kwargs  : dict
                        Dictionary describing how the arrows should be drawn using plt.arrow.
                        
        bias_kwargs   : dict
                        Dictionary describint the modifications of how bias units should be drawn using plt.Circle.
                        
    Methods
    ==================
        add_nodes     : (base, n, m, node_type, P, **kwargs)
                        Adds a layer of a FCNN to the graph with shared base name and `n` units belonging to `node_type`.
                        `m` describes the hidden index and `P` is used if connecting a previous layer to the current layer.
    """
    def __init__(self, n_input = 3, n_hidden = [3, 3], n_output = 5, v_space = 3, h_space = 5, radius = 1, annot = 20, bias = False,
                 input_kwargs = input_kwargs, hidden_kwargs = hidden_kwargs, output_kwargs = output_kwargs, arrow_kwargs = arrow_kwargs,
                 bias_kwargs = bias_kwargs):
        
        self._set(locals())
        
        xb_kwargs  = input_kwargs.copy(); xb_kwargs.update(bias_kwargs)
        hb_kwargs  = hidden_kwargs.copy(); hb_kwargs.update(bias_kwargs)
        node_types = {'input' : input_kwargs, 'hidden' : hidden_kwargs, 'output' : output_kwargs, 'input_bias' : xb_kwargs, 'hidden_bias' : hb_kwargs}
        connection_types = {'normal' : arrow_kwargs}
        
        super().__init__(node_types = node_types, connection_types = connection_types, annot = annot)
        
        self._m = m = max([n_input, *n_hidden, n_output])
        
        P  = self.add_nodes('x', n_input, 0, 'input', radius = radius)
        for i, hidden in enumerate(n_hidden, 1):
            P = self.add_nodes('h', hidden, i, 'hidden', P = P, radius = radius)
        P = self.add_nodes('y', n_output, len(n_hidden) + 1, 'output', P = P, radius = radius)

        self.render         = self._render
        
    def add_nodes(self, base, n, m, node_type = None, P = None, **kwargs):
        bias = self.bias * (base != 'y')
        Q    = []
        for j in range(n):
            args  = (m, (j + 1)) if base == 'h' else (j + 1,)
            name  = f'{base}-{m}-{j}' if base == 'h' else f'{base}-{j}'
            label = self._gen_label(base, *args)
            self._add_node(name,
                           (m * self.h_space, self.v_space * (j + (self._m - n - bias) / 2)),
                           node_type = node_type,
                           label = label,
                           **kwargs)
            if P:
                for p in P:
                    self._add_connection(p, name, 'normal')
            Q.append(name)
        if bias:
            j    += 1
            name  = f'b-{m}-{j}' if base == 'h' else f'b-{j}'
            label = self._gen_label('b', m, bold = False)
            self._add_node(name,
                           (m * self.h_space, self.v_space * (j + (self._m - n - bias) / 2)),
                           node_type = node_type + '_bias',
                           label = label,
                           **kwargs)
            Q.append(name)
        return Q
    

data_kwargs = dict(ec = 'k', fc = 'silver')
variable_kwargs = dict(ec = 'k', fc = 'none', ls = (0, (5, 5)))
function_kwargs = dict(ec = 'k', fc = 'none')
arrow_kwargs = dict(head_width = 0.2, length_includes_head = True, fc = 'k')

class GraphicalModel(Graph):
    """
    Graphical Model Class (Graph)
    
    Parameters
    ====================
        data_kwargs     : dict
                          Dictionary describing how the 'data' units should be drawn using plt.Circle.
                          
        variable_kwargs : dict
                          Dictionary describing how the 'variable' units should be drawn using plt.Circle.
                          
        function_kwargs : dict
                          Dictionary describing how the 'function' units should be drawn using plt.Circle.
                          
        arrow_kwargs    : dict
                          Dictionary describing how the connections should be drawn using plt.arrow
                          
        radius          : float
                          Radius of all units.
                          
        annot           : {False, int}
                          Annotation size. If False or 0, annotations will not appear when rendered.
                          
    Methods
    ===================
        add_nodes       : (name, xy, node_type, **kwargs)
                          Adds the node `name` to the graph at `xy` location with `node_type` string expected in `node_types`.
                          `kwargs` will be unpacked into plt.Circle.
                          
        add_connection  : (A, B, connection_type)
                          Adds a connection from node `A` to node `B`.
    """
    def __init__(self, data_kwargs = data_kwargs, variable_kwargs = variable_kwargs, function_kwargs = function_kwargs,
                 arrow_kwargs = arrow_kwargs, radius = 0.8, annot = 20):
        
        self._set(locals())
        
        node_types = dict(data = data_kwargs, variable = variable_kwargs, function = function_kwargs)
        connection_types = {'normal' : arrow_kwargs}
        
        super().__init__(node_types = node_types, connection_types = connection_types, annot = annot)
        
        self.render = self._render
        
    def add_node(self, name, xy, node_type, bold = True, **kwargs):
        label = self._gen_label(name, bold = bold)
        self._add_node(name, xy, node_type, radius = self.radius, label = label, **kwargs)
        
    def add_connection(self, A, B):
        self._add_connection(A, B, 'normal')
