from .generic import Graph, plt

_arrow_kwargs  = dict(head_width = 0.2, fc = 'k', length_includes_head = True)
_input_kwargs  = dict(ec = 'k', fc = 'tab:green')
_hidden_kwargs = dict(ec = 'k', fc = 'tab:blue')
_output_kwargs = dict(ec = 'k', fc = 'tab:orange')
_bias_kwargs   = dict(alpha = 0.5, ls = (0, (5, 5)))

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
                        
        vertical      : bool
                        If True, renders a bottom-up visualisation instead of left-right.
                        
        labels        : list, str
                        Should contain three elements describing the input, hidden, and output labels.
                        
    Methods
    ==================
        add_nodes     : (base, n, m, node_type, P, **kwargs)
                        Adds a layer of a FCNN to the graph with shared base name and `n` units belonging to `node_type`.
                        `m` describes the hidden index and `P` is used if connecting a previous layer to the current layer.
    """
    def __init__(self, n_input = 3, n_hidden = [3, 3], n_output = 5, v_space = 3, h_space = 5, radius = 1, annot = 20, bias = False,
                 input_kwargs = _input_kwargs, hidden_kwargs = _hidden_kwargs, output_kwargs = _output_kwargs, arrow_kwargs = _arrow_kwargs,
                 bias_kwargs = _bias_kwargs, vertical = False, labels = 'xhy'):
        
        self._set(locals())
        
        xb_kwargs  = input_kwargs.copy(); xb_kwargs.update(bias_kwargs)
        hb_kwargs  = hidden_kwargs.copy(); hb_kwargs.update(bias_kwargs)
        node_types = {'input' : input_kwargs, 'hidden' : hidden_kwargs, 'output' : output_kwargs, 'input_bias' : xb_kwargs, 'hidden_bias' : hb_kwargs}
        connection_types = {'normal' : arrow_kwargs}
        
        super().__init__(node_types = node_types, connection_types = connection_types, annot = annot)
        
        self._m  = max([n_input, *n_hidden, n_output])
        self.__P = []
        
        kwargs   = dict(radius = radius, vertical = vertical)
        self.add_nodes(labels[0], n_input, 0, 'input', **kwargs)
        for i, hidden in enumerate(n_hidden, 1):
            self.add_nodes(labels[1], hidden, i, 'hidden', **kwargs)
        self.add_nodes(labels[2], n_output, len(n_hidden) + 1, 'output', **kwargs)
        
    def add_nodes(self, base, n, m, node_type = None, **kwargs):
        bias = self.bias * (base != self.labels[2])
        P    = []
        for j in range(n):
            args  = (m, (j + 1)) if base == self.labels[1] else (j + 1,)
            name  = f'{base}-{m}-{j}' if base == self.labels[1] else f'{base}-{j}'
            label = self._gen_label(base, *args, bold = False)
            self._add_node(name,
                           (m * self.h_space, self.v_space * (j + (self._m - n - bias) / 2)),
                           node_type = node_type,
                           label = label,
                           **kwargs)
            if self.__P:
                for p in self.__P:
                    self._add_connection(p, name, 'normal')
            P.append(name)
        if bias:
            j    += 1
            name  = f'b-{m}-{j}' if base == self.labels[1] else f'b-{j}'
            label = self._gen_label('b', m, bold = False)
            self._add_node(name,
                           (m * self.h_space, self.v_space * (j + (self._m - n - bias) / 2)),
                           node_type = node_type + '_bias',
                           label = label,
                           **kwargs)
            P.append(name)
        self.__P = P
    

_data_kwargs = dict(ec = 'k', fc = 'silver')
_variable_kwargs = dict(ec = 'k', fc = 'none', ls = (0, (5, 5)))
_function_kwargs = dict(ec = 'k', fc = 'none')
_arrow_kwargs = dict(head_width = 0.2, length_includes_head = True, fc = 'k')

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
    def __init__(self, data_kwargs = _data_kwargs, variable_kwargs = _variable_kwargs, function_kwargs = _function_kwargs,
                 arrow_kwargs = _arrow_kwargs, radius = 0.8, annot = 20):
        
        self._set(locals())
        
        node_types = dict(data = data_kwargs, variable = variable_kwargs, function = function_kwargs)
        connection_types = {'normal' : arrow_kwargs}
        
        super().__init__(node_types = node_types, connection_types = connection_types, annot = annot)
        
    def add_node(self, name, xy, node_type, bold = True, **kwargs):
        label = self._gen_label(name, bold = bold)
        self._add_node(name, xy, node_type, radius = self.radius, label = label, **kwargs)