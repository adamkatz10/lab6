"""6.009 Lab 6 -- Gift Delivery."""


from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!


class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        self.graph_class = graph_class()

    def from_list(self, adj_list, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency list as source, where the `labels` dictionary
        maps each node name to its label.

        Parameters:
            `adj_list`: adjacency list representation of a graph
                        (as a list of lists)
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        """

        for i in range(len(adj_list)):
            if labels is None:
                label = ''
            else:
                label = labels[i]
            self.graph_class.add_node(i, label)
            
        for j in range(len(adj_list)):   
            for end_node in adj_list[j]:
                self.graph_class.add_edge(j, end_node)
        
        return self.graph_class
    
    def from_dict(self, adj_dict, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency dictionary as source where the `labels`
        dictionary maps each node name its label.

        Parameters:
            `adj_dict`: adjacency dictionary representation of a graph
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        """
        for name in adj_dict:
            if labels is None:
                label = ''
            else:
                label = labels[name]
            self.graph_class.add_node(name, label)
        
        for key in adj_dict:
            for end_node in adj_dict[key]:
                self.graph_class.add_edge(key, end_node)

        return self.graph_class
    
class SimpleGraph(Graph):
    """Simple implementation of the Graph interface."""

    def __init__(self):
        self.adj_dict = {} #maps nodes to the nodes they have edges to
        self.labels = {} #maps a lavel to all of the names the encompass
        self.names = {} #maps names to their label's

    def query(self, pattern):
        """Return a list of subgraphs matching `pattern`.

        Parameters:
            `pattern`: a list of tuples, where each tuple represents a node.
                The first element of the tuple is the label of the node, while
                the second element is a list of the neighbors of the node as
                indices into `pattern`. A single asterisk '*' in place of the
                label matches any label.

        Returns:
            a list of lists, where each sublist represents a match, its items
            being names corresponding to the nodes in `pattern`.

        """
        #Looks like there will be an error when integers are used as arguments in pattern
        #representing node's label's
        
        def label_insert(label):
            if self.labels != {}:
                if label != "*":
                    return self.labels[label]
                else:
                    return_list = []
                    for l in self.labels.keys():
                        return_list.extend(self.labels[l])
                    return return_list
            else:
                return_list = []
                for key in self.adj_dict.keys():
                    return_list.append(key)
                return_list = list(set(return_list))
                return return_list
            
        def valid_path(path):
            #should I add another argument that is a dictionary - to check to see if something works/
            #doesn't work without checking
            nodes = []
            for i in range(len(path)):
                for name in path[i][1]:
                    if name not in self.adj_dict[path[i][0]]: #if no edge between start and end
                        return False, [] 
                nodes.append(path[i][0])
            return True, nodes #there is an edge between start and every end node
        
        new_pattern = duplicate(pattern) #deep copy
        new_pattern = edge_insert(new_pattern) #convert integers to their respective label strings
        for i in range(len(new_pattern)):
            new_pattern[i][0] = label_insert(new_pattern[i][0])
            for j in range(len(new_pattern[i][1])):
                new_pattern[i][1][j] = label_insert(new_pattern[i][1][j])
        paths_list = get_paths(new_pattern, [[]])
        return_list = []
        for a_path in paths_list:
            valid, add = valid_path(a_path)
            if valid:
                return_list.append(add)
        return return_list
                     
    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""
        if name not in self.adj_dict.keys(): #new node
            self.adj_dict[name] = [] 
            self.names[name] = label if label != '' else None #map name to its label in names
        else:
            raise ValueError
        if label != '':
            if label not in self.labels.keys(): #new label
                self.labels[label] = [name]
            else: #label already exists
                self.labels[label].extend([name])

    def remove_node(self, name):
        """Remove the node with name `name`."""
        try:
            del self.adj_dict[name] #remove node from adj_list      
        except:
            raise LookupError
        try:
            self.labels[self.names[name]].remove(name) #remove the value from labels
        except:
            pass
        try:    
            del self.names[name] #remove node from names
        except:
            raise LookupError


    def add_edge(self, start, end):
        """Add a edge from `start` to `end`."""
        if start in self.adj_dict.keys() and end in self.adj_dict.keys(): #if valid keys
            if end in self.adj_dict[start]:
                raise ValueError
            self.adj_dict[start].extend([end]) #add end as a value to start in the adj_dict
        else:
            raise LookupError

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        try:
            self.adj_dict[start].remove(end) #remove the edge between start and end
        except: #there's an error
            raise LookupError

class CompactGraph(Graph):
    """Graph optimized for cases where many nodes have the same neighbors."""

    def __init__(self):
        self.adj_dict = {} #maps nodes to the nodes they have edges to
        self.labels = {} #maps a lavel to all of the names the encompass

    def query(self, pattern):
        """Return a list of subgraphs matching `pattern`.

        Parameters:
            `pattern`: a list of tuples, where each tuple represents a node.
                The first element of the tuple is the label of the node, while
                the second element is a list of the neighbors of the node as
                indices into `pattern`. A single asterisk '*' in place of the
                label matches any label.

        Returns:
            a list of lists, where each sublist represents a match, its items
            being names corresponding to the nodes in `pattern`.

        """
        def label_insert(label):
            if self.labels != {}:
                if label != "*":
                    return self.labels[label]
                else:
                    return_list = []
                    for l in self.labels.keys():
                        return_list.extend(self.labels[l])
                    return return_list
            else:
                return_list = []
                for key in self.adj_dict.keys():
                    for k in key:
                        return_list.append(k)
                return_list = list(set(return_list))
                return return_list

        def valid_path(path):
            #should I add another argument that is a dictionary - to check to see if something works/
            #doesn't work without checking
            nodes = []
            for i in range(len(path)):
                for keys in self.adj_dict.keys():
                    if path[i][0] in keys:
                        special_key = keys
                        for name in path[i][1]:
                            if name not in self.adj_dict[special_key]: #if no edge between start and end
                                return False, [] 
                nodes.append(path[i][0])
            return True, nodes #there is an edge between start and every end node
        
        new_pattern = duplicate(pattern) #deep copy
        new_pattern = edge_insert(new_pattern) #convert integers to their respective label strings
        for i in range(len(new_pattern)):
            new_pattern[i][0] = label_insert(new_pattern[i][0])
            for j in range(len(new_pattern[i][1])):
                new_pattern[i][1][j] = label_insert(new_pattern[i][1][j])
        paths_list = get_paths(new_pattern, [[]])
        return_list = []
        for a_path in paths_list:
            valid, add = valid_path(a_path)
            if valid:
                return_list.append(add)
        return return_list

        
    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""
        for keys in self.adj_dict.keys():
            for key in keys:
                if key == name:
                    raise KeyError
        
        if label != '':
            if label not in self.labels.keys(): #new label
                self.labels[label] = [name]
            else: #label already exists
                self.labels[label].extend([name])        
        
        if [] not in self.adj_dict.values():
            self.adj_dict[(name,)] = []
        else:
            new_key = [name]
            for key,val in self.adj_dict.items():
                if val == []:
                    new_key.extend(list(key))
                    new_key = tuple(new_key)
                    self.adj_dict[new_key] = val  
                    del self.adj_dict[key]

    def remove_node(self, name):
        """Remove the node with name `name`."""
        node_bool = False
        for key,val in self.adj_dict.items():
            if name in key:
                node_bool = True
                special_key = key
                special_value = val
                
        if node_bool:
            new_key = list(special_key)
            new_key.remove(name)
            new_key = tuple(new_key)
            self.adj_dict[new_key] = special_value
            del self.adj_dict[special_key]
        else:
            raise LookupError

    def add_edge(self, start, end):
        """Add a edge from `start` to `end`."""
        start_bool = False
        end_bool = False
        for key, val in self.adj_dict.items():
            if start in key:
                start_bool = True
                start_key = key
                if end in val:
                    raise ValueError
                value = val
            if end in key:
                end_bool = True
        if start_bool and end_bool:
            pass
        else:
            raise LookupError
        
        new_key = list(start_key)
        new_key.remove(start)
        new_key = tuple(new_key)
        del self.adj_list[start_key]
        self.adj_list[new_key] = value
        
        new_val = list(set(value.append(end)))
        key2_in_vals = False
        special_key = None
        for key2, val2 in self.adj_dict.items():
            if val2 == new_val:
                key2_in_vals = True
                special_key = key2
        
        if key2_in_vals:
            new_key2 = list(special_key)
            new_key2.extend([start])
            new_key2 = tuple(new_key2)
            del self.adj_dict[special_key]
            self.adj_dict[new_key] = new_val
        else:
            self.adj_dict[(start,)] = new_val

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        start_bool = False
        end_edge_bool = False
        for key,val in self.adj_dict.items():
            if start in key:
                start_bool = True
                if end not in val: #I don't check to see if end exists, I think this is good enough
                    raise LookupError
                else:
                    end_edge_bool = True
                special_key = key
                special_val = val
            
        if start_bool and end_edge_bool:
            del self.adj_dict[special_key]
            new_key = list(special_key)
            new_key.remove(start)
            new_key = tuple(new_key)
            self.adj_dict[new_key] = special_val
                
                

def allocate_teams(graph, k, stations, gift_labels):
    """Compute the number of teams needed to deliver each gift.

    It is guaranteed that there is exactly one node for each gift type and all
    building nodes have the label "building".

    Parameters:
        `graph`: an instance of a `Graph` implementation
        `k`: minimum number of buildings that a cluster needs to contain for a
             delivery to be sent there
        `stations`: mapping between each node name and a string representing
                    the name of the closest subway/train station
        `gift_labels`: a list of gift labels

    Returns:
        a dictionary mapping each gift label to the number of teams
        that Santa needs to send for the corresponding gift to be delivered

    """
    raise NotImplementedError("not implemented")
    
def nested_deep_copy(list_of_tups):
    whole_return = []
    for l in list_of_tups:
        new_list = []
        for elem in l:
            new_list.append(elem)
        whole_return.append(new_list)
    return whole_return #returns a list of tuples 
    
def duplicate(pattern):
    dup_pattern = nested_deep_copy(pattern)
    return dup_pattern

def edge_insert(pattern):
    for i in range(len(pattern)):
        dive = pattern[i][1]
        for j in range(len(dive)):
            index = dive[j]
            new_val = pattern[index][0]
            pattern[i][1][j] = new_val
    return pattern #does not check to see if new_val or index is in range
            

def get_paths(list_of_lists, prev):
    #prev is a list of lists
    elements = list_of_lists[0]
    if elements != [] and type(elements[0]) == list and len(elements) > 1: #if elements is a list of lists
        new_elements = get_paths(elements, [[]])
        elements = new_elements
    new_lists = []
    for l in prev:
        if elements != []:
            for elem in elements:
                m = l.copy()
                m.extend([elem])
                new_lists.append(m)
        else:
            for elem in [[]]:
                m = l.copy()
                m.extend([elem])
                new_lists.append(m)
    if len(list_of_lists) > 1: #recrusive step
        return get_paths(list_of_lists[1:], new_lists)
    else: #base case, no more permutations to create
        return new_lists




if __name__ == '__main__':
    # Put code here that you want to execute when lab.py is run from the
    # command line, e.g. small test cases.
    pass
