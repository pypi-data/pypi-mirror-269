# Import Libraries
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.integrate import odeint, solve_ivp
import itertools
import random
from itertools import combinations
from networkx import *
from ortools.linear_solver import pywraplp
import os
import pyEDM
from tqdm import tqdm
import shutil
import warnings

# Class Definition
class FrustrationDynamiX(object):
    
    def __init__(self, time_series_df, is_normalized = False):
        """
        Initialize the class
        time_series is a pandas dataframe file with first column as time, and header is t, x1, x2, ..., xn
        """
        df = time_series_df
        list_var = df.columns.to_list()
        self.time_series = df
        self.duration = len(df)
        self.num_var = len(list_var) - 1
        self.time_var = list_var[0]
        self.dynamic_var = list_var[1:]
        self.time = df[self.time_var]
        self.time_vector = None
        self.is_normalized = is_normalized
        self.triadic_balance = None
        self.balanced_triangles = None
        self.unbalanced_triangles = None
        self.edge_deletion = None
        self.frustration = None
        self.cohesiveness = None
        self.divisiveness = None     
        
    
    def plot_series(self, xlabel = "Time", ylabel = "Variables", title = "Time series", save_plot = None):
        """
        Function to plot the time series with legend and labels
        """
        for col in self.dynamic_var:
            plt.plot(self.time, self.time_series[col], label=col)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        if save_plot != None:
            assert type(save_plot) == str, "save_plot variable should have type string, type " + str(type(save_plot)) + " was given instead"
            plt.savefig(save_plot)
        plt.show()
    
    def round_series(self, number_figures):
        """
        Function to round the time series up to the number_figures using the df.round(number_figures)
        """
        df = self.time_series.round(number_figures)
        return FrustrationDynamiX(df, is_normalized = self.is_normalized)
    
    def normalize_series_max(self):
        """
        Function to normalize the time series by dividing by the maximum
        of the union of all series so that all values are between -1 and 1
        """
        df = self.time_series[self.dynamic_var]
        abs_df = df.abs()
        max_val = df.max().max()
        normalized_df = df/max_val
        normalized_df.insert(0, self.time_var, self.time)
        return FrustrationDynamiX(normalized_df, is_normalized = True)
    
    def normalize_series_constant(self, constant):
        """
        Function to normalize the time series by dividing by a user defined constant
        The constant must be real and positive
        """
        df = self.time_series[self.dynamic_var]
        normalized_df = df/constant
        normalized_df.insert(0, self.time_var, self.time)
        return FrustrationDynamiX(normalized_df, is_normalized = True)
    
    def smooth_series(self):
        """
        Function that smoothens the time series in case data comes from real noisy data
        """
    
    def jacobian_smap(self, window_size = None, showPlot = True):
        """
        Function to infer the Jacobian coeffiecients of the time series for given window_size
        Window_size by default must be (number of variables of the series) + 2, 
        and must return an error if specified by user to be less
        User must specify if error plots must be shown, and if errors must be stored somewhere
        """
        if window_size == None:
            window_size = self.num_var + 2
        J = np.zeros((self.num_var,self.num_var,len(range(1,self.duration-window_size,window_size)))) #Define empty jacobian
        
        #Define the empty variables
        T_ind = 0
        time_vector = []
        
        #Loop over variables
        for t in tqdm(range(1,self.duration-window_size,window_size)):
            for u in range(self.num_var): #1 loop for each variable
                result = pyEDM.SMap(dataFrame = self.time_series, lib = [t,t+window_size], pred = [t,t+window_size], 
                                    embedded = True, columns = self.dynamic_var, target = self.dynamic_var[u], showPlot= showPlot)
                var = result['coefficients'].columns[2:]
                for v in range(len(var)):
                    if u != v:
                        J[u,v,T_ind] = result['coefficients'][var[v]][window_size//2]
                        
            #Update iterators
            T_ind += 1
            time_vector += [self.time[t + window_size//2]]

        return np.nan_to_num(J), time_vector
   
    @staticmethod
    def saveas_coo(jacobian_matrix, path):
        """
        Function to save the Jacobian coefficients as csv files in COO format
        User must specify the path of daving the folder
        If this function is called, self variable must be marked as False, ie do not delete output file
        """
        # Create the folder
        os.makedirs(path, exist_ok=True)

        # Iterate over each time step 't' to create and save a CSV file for each Jacobian matrix
        for t in range(1,jacobian_matrix.shape[2]):
            # Prepare the data for COO format: lists of src, dst, and val
            src = []
            dst = []
            val = []
            for i in range(jacobian_matrix.shape[0]):  # Iterate over rows
                for j in range(jacobian_matrix.shape[1]):  # Iterate over columns
                    # Add the edge to the COO format data
                    if i != j:
                        src.append(i)
                        dst.append(j)
                        val.append(jacobian_matrix[i, j, t])

            # Create a DataFrame from the COO format data
            df_coo = pd.DataFrame({'src': src, 'dst': dst, 'val': val})

            # Save the DataFrame to a CSV file
            csv_file_path = os.path.join(path, f"J_{t}.csv")
            df_coo.to_csv(csv_file_path, index=False)
            
    @staticmethod
    def temp_coo(jacobian_matrix):
        """
        Function to generate COO files that must be deleted after analysis in case user
        does not wish to use the saved files
        Back-end function that gets called to be passed to frustration computation
        calls the save_as function with a path called ./temp
        If this function is called, self variable must be marked as True, ie do delete output file
        """
        FrustrationDynamiX.saveas_coo(jacobian_matrix, "./temp")
        
    @staticmethod
    def read_graph(path):
        """
        Helper function to read the graphs of the specified path 
        """
        G = nx.DiGraph()
        with open(path, newline='') as f:
            edgelist = list(csv.reader(f))[1:]
        for u, v, w in edgelist:
            if float(w) > 0:
              G.add_edge(int(u), int(v), weight=float(w), sign=1)
            elif float(w) < 0:
              G.add_edge(int(u), int(v), weight=float(w), sign=-1)
        return G
    
    @staticmethod
    def get_directed_triads(triads):
        """
        Helper function to help compute the triadic frustration
        """
        for candidate_edges in combinations(triads.items(), 3):
            unique_edges = set([tuple(sorted(k)) for k,v in candidate_edges])
            if len(unique_edges) == 3:
                yield dict(candidate_edges)
    
    @staticmethod
    def search_triangles(G, nodes = None):
        """
        Helper function to help compute the triadic frustration
        """
        if nodes is None:
            nodes_nbrs = G.adj.items()
        else:
            nodes_nbrs = ((n, G[n]) for n in G.nbunch_iter(nodes))
        for v, v_nbrs in nodes_nbrs:
            vs = set(v_nbrs) - {v}
            for w in vs:
                xx = vs & (set(G[w]) - {w})
                yield [ set(x) for x in list(zip(itertools.repeat(v), itertools.repeat(w), list(xx))) ]
        
    @staticmethod
    def compute_triad_balance(G_new):
        """
        Function to compute triadic balance
        """
        triad_dict = {}
        triad_class = {}
        all_triads = []
        non_transitive_census = ['003','012', '102', '021D', '021C', '021U', '021', '111U', '111D', '201', '030C', '120C', '210']
        iter_g = FrustrationDynamiX.search_triangles(G_new)

        for iter_t in iter_g:
            for ta in list(iter_t):
                tt = ",".join([str(x) for x in sorted(set(ta))])
                triad_dict[tt] = True

        for val in triad_dict.keys():
            nodes = [int(x) for x in val.split(",")]
            subgraph = G_new.subgraph(nodes)
            if subgraph:
                census = [k for k, v in nx.triads.triadic_census(subgraph).items() if v]
                if census and census[0] not in non_transitive_census:
                    sign = nx.get_edge_attributes(subgraph, 'weight')
                    triad_class[val] = [census[0], sign]

        for key, value in triad_class.items():
            all_directed_triads = list(FrustrationDynamiX.get_directed_triads(value[1]))
            all_triads.append([all_directed_triads, value[0]])

        balances = []
        imbalances = []
        for items in all_triads:
            balance_list = []
            if items[1] == '300':
                for triangle in items[0]:
                    node = []
                    for edge in triangle:
                        if edge[0] not in node:
                            node.append(edge[0])
                    if len(node) != 3:
                        balance = 1
                        for edge in triangle:
                            balance *= triangle[edge]
                        balance_list.append(balance)
            else:
                for item in items[0]:
                    balance = 1
                    for edge in item:
                        balance *= item[edge]
                    balance_list.append(balance)
            neg = [n for n in balance_list if n <= 0]
            if neg:
                imbalances.append(items)
            else:
                balances.append(items)

        balance_ratio = (len(balances)/(len(balances) + len(imbalances))) if (len(balances) + len(imbalances)) > 0 else None
        return balance_ratio, len(balances), len(imbalances)
    
    @staticmethod
    def compute_cohesiveness_divisiveness(nx_graph, solution):
        """
        Helper function to compute the cohesiveness and divisiveness ratios in macroscale
        """
        Ei_pos = 0  # Number of internally cohesive edges within positive edges
        Ee_neg = 0  # Number of externally divisive edges within negative edges
        Ei = 0      # Total number of internal edges
        Ee = 0      # Total number of external edges

        # Iterate over all edges in the graph
        for u, v, data in nx_graph.edges(data=True):
            color_u = solution[u].solution_value()
            color_v = solution[v].solution_value()
            # Check if the edge is positive
            if data.get('sign', 1) > 0:
                if color_u == color_v:
                    Ei_pos += 1
                    Ei += 1
                else:
                    Ee += 1
            # Check if the edge is negative
            elif data.get('sign', -1) < 0:
                if color_u != color_v:
                    Ee_neg += 1
                    Ee += 1
                else:
                    Ei += 1

        # Calculate cohesiveness and divisiveness
        C = Ei_pos / Ei if Ei != 0 else 0  # Cohesiveness
        D = Ee_neg / Ee if Ee != 0 else 0  # Divisiveness

        return C, D
        
    @staticmethod
    def plot_colored_graph(G, solution, color_0 = "red", color_1 = "blue"):
        """
        Helper function to plot the colored partitioned graph based on ILP solution
        """
        color_map = [color_0 if solution.get(node, 0).solution_value() == 1 else color_1 for node in G.nodes()]

        # Draw the graph
        plt.figure(figsize=(10, 7))
        nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold', node_size=700)
        plt.title('Graph with Node Coloring Based on ILP Solution')
        plt.axis('off')  # Turn off the axis
        plt.show()
    
    @staticmethod
    def ilp_AND_frustration(G, showPlot = False):
        """
        Helper function to compute the macroscale index by the AND model
        """
        def count_signed_edges(graph, node):
            positive_count = 0
            negative_count = 0

            # Check for edges where the node is the source (u)
            for _, v, data in graph.out_edges(node, data=True):
                if data['sign'] == 1:
                    positive_count += 1
                elif data['sign'] == -1:
                    negative_count += 1

            # Check for edges where the node is the target (v)
            for u, _, data in graph.in_edges(node, data=True):
                if data['sign'] == 1:
                    positive_count += 1
                elif data['sign'] == -1:
                    negative_count += 1

            return positive_count, negative_count

        # Define the Solver
        solver = pywraplp.Solver.CreateSolver('SCIP')

        # Define the variables
        x = {node: solver.IntVar(0, 1, f'x[{node}]') for node in G.nodes()}
        xij = {(i, j): solver.IntVar(0, 1, f'xij[{i},{j}]') for i, j in G.edges()}

        num_neg = 0

        # Define Constraints
        for (u, v, data) in G.edges(data=True):
            if data['sign'] > 0:  # Positive edge
                constraint = solver.RowConstraint(0, solver.infinity(), '')
                constraint.SetCoefficient(xij[(u,v)], -1)
                constraint.SetCoefficient(x[u], 1)
                constraint = solver.RowConstraint(0, solver.infinity(), '')
                constraint.SetCoefficient(xij[(u,v)], -1)
                constraint.SetCoefficient(x[v], 1)
            else:  # Negative edge
                num_neg += 1
                constraint = solver.RowConstraint(-1, solver.infinity(), '')
                constraint.SetCoefficient(xij[(u,v)], 1)
                constraint.SetCoefficient(x[u], -1)
                constraint.SetCoefficient(x[v], -1)

        # Set Objective
        objective = solver.Objective()
        for (u, v, data) in G.edges(data=True):
            if data['sign'] > 0:  # Positive edge
                objective.SetCoefficient(xij[(u, v)], -2)
            else:  # Negative edge
                objective.SetCoefficient(xij[(u, v)], 2)

        for u in G.nodes():
            positive_count, negative_count = count_signed_edges(G, u)
            objective.SetCoefficient(x[u], positive_count - negative_count)
        objective.SetMinimization()

        #Call the solver
        status = solver.Solve()

        # Solution
        if status == pywraplp.Solver.OPTIMAL:
            # Frustration Index
            min_edges = solver.Objective().Value() + num_neg
            N_edges = G.number_of_edges()
            macro = 1 - 2 * min_edges / N_edges
            C, D = FrustrationDynamiX.compute_cohesiveness_divisiveness(G, x)  # Assumes adaptation for NetworkX
            if showPlot:
                FrustrationDynamiX.plot_colored_graph(G, x)  # Assumes adaptation for NetworkX
            return min_edges, macro, C, D
        else:
            print('The problem does not have an optimal solution.')
            return None, None, None, None
        
    @staticmethod
    def ilp_XOR_frustration(G, showPlot = False):
        """
        Helper function to compute the macroscale index by the XOR model
        """ 
            # Define the Solver
        solver = pywraplp.Solver.CreateSolver('SCIP')

        # Define the variables
        x = {}  # Variable for each Node
        for node in G.nodes():
            x[node] = solver.IntVar(0, 1, f'x[{node}]')

        f = {}  # Variable for each Edge
        for i, edge in enumerate(G.edges()):
            f[i] = solver.IntVar(0, 1, f'f[{i}]')

        # Define Constraints
        for i, (u, v, data) in enumerate(G.edges(data=True)):
            if data['sign'] > 0:  # Positive edge
                constraint1 = solver.RowConstraint(0, solver.infinity(), '')
                constraint1.SetCoefficient(f[i], 1)
                constraint1.SetCoefficient(x[u], -1)
                constraint1.SetCoefficient(x[v], 1)

                constraint2 = solver.RowConstraint(0, solver.infinity(), '')
                constraint2.SetCoefficient(f[i], 1)
                constraint2.SetCoefficient(x[u], 1)
                constraint2.SetCoefficient(x[v], -1)
            else:  # Negative edge
                constraint1 = solver.RowConstraint(-1, solver.infinity(), '')
                constraint1.SetCoefficient(f[i], 1)
                constraint1.SetCoefficient(x[u], -1)
                constraint1.SetCoefficient(x[v], -1)

                constraint2 = solver.RowConstraint(1, solver.infinity(), '')
                constraint2.SetCoefficient(f[i], 1)
                constraint2.SetCoefficient(x[u], 1)
                constraint2.SetCoefficient(x[v], 1)

        # Set Objective
        objective = solver.Objective()
        for i in f.keys():
            objective.SetCoefficient(f[i], 1)
        objective.SetMinimization()

        # Call the solver
        status = solver.Solve()

        # Solution
        if status == pywraplp.Solver.OPTIMAL:
            # Frustration Index
            min_edges = solver.Objective().Value()
            N_edges = len(G.edges())
            macro = 1 - 2 * min_edges / N_edges
            C, D = FrustrationDynamiX.compute_cohesiveness_divisiveness(G, x)  # Assuming this function is adapted for NetworkX
            if showPlot:
                FrustrationDynamiX.plot_colored_graph(G, x)  # Assuming this function exists and is adapted for NetworkX
            return min_edges, macro, C, D
        else:
            print('The problem does not have an optimal solution.')
            return None, None, None, None
        
    @staticmethod
    def ilp_ABS_frustration(G, showPlot = False):
        """
        Helper function to compute the macroscale index by the ABS model
        """
        # Define the Solver
        solver = pywraplp.Solver.CreateSolver('SCIP')

        # Define the variables
        infinity = solver.infinity()
        x = {}  # Variable for each Node
        for i in G.nodes():
            x[i] = solver.IntVar(0, 1, 'x%i' % i)

        e = {}  # 2 Variables for each Edge
        h = {}
        for i, edge in enumerate(G.edges()):
            e[i] = solver.IntVar(0, 1, 'e%i' % i)
            h[i] = solver.IntVar(0, 1, 'h%i' % i)

        # Define Constraints
        # Loop over edges and add constraints based on the sign of the edge
        for i, (u, v, data) in enumerate(G.edges(data=True)):
            if data['sign'] > 0:  # Positive edge
                constraint = solver.RowConstraint(0, 0, '')
                constraint.SetCoefficient(e[i], -1)
                constraint.SetCoefficient(h[i], 1)
                constraint.SetCoefficient(x[u], 1)
                constraint.SetCoefficient(x[v], -1)
            else:  # Negative edge
                constraint = solver.RowConstraint(1, 1, '')
                constraint.SetCoefficient(e[i], -1)
                constraint.SetCoefficient(h[i], 1)
                constraint.SetCoefficient(x[u], 1)
                constraint.SetCoefficient(x[v], 1)

        # Set Objective
        objective = solver.Objective()
        for i in range(len(G.edges())):
            objective.SetCoefficient(e[i], 1)
            objective.SetCoefficient(h[i], 1)
        objective.SetMinimization()

        # Call the solver
        status = solver.Solve()

        # Solution
        if status == pywraplp.Solver.OPTIMAL:
            # Frustration Index
            min_edges = solver.Objective().Value()
            N_edges = len(G.edges())
            macro = 1 - 2 * min_edges / N_edges
            C,D = FrustrationDynamiX.compute_cohesiveness_divisiveness(G, x)
            if showPlot:
              FrustrationDynamiX.plot_colored_graph(G, x)
            return min_edges, macro, C, D
        else:
            return None, None, None, None
    
    def compute_triadic_evolution(self, window_size = None, showPlots = True):
        """
        Helper function to compute the triadic balance for all frames
        """
        model = FrustrationDynamiX(self.time_series)
        jacobian_matrix, time_vector = model.jacobian_smap(window_size = window_size, showPlot = showPlots)
        FrustrationDynamiX.temp_coo(jacobian_matrix)
        number_iterations = len(time_vector)
        triadic_balance = np.zeros(number_iterations)
        balanced_triangles = np.zeros(number_iterations)
        unbalanced_triangles = np.zeros(number_iterations)
        for i in tqdm(range(1,number_iterations)):
            path = "./temp/J_" + str(i) + ".csv"
            G = FrustrationDynamiX.read_graph(path)
            triadic_balance[i], balanced_triangles[i], unbalanced_triangles[i] = FrustrationDynamiX.compute_triad_balance(G)
        
        self.time_vector = time_vector
        self.triadic_balance = triadic_balance
        self.balanced_triangles = balanced_triangles
        self.unbalanced_triangles = unbalanced_triangles
        shutil.rmtree("./temp")
        
        return time_vector, triadic_balance, balanced_triangles, unbalanced_triangles
    
    def compute_frustration_evolution(self, method, window_size = None, showPlots = True):
        """
        Helper function to compute the frustration ILP for either AND, ABS or XOR, based on specified method
        """
        assert method in ["AND", "XOR", "ABS"], "Invalid Method: Method should be AND or XOR or ABS"
        model = FrustrationDynamiX(self.time_series)
        jacobian_matrix, time_vector = model.jacobian_smap(window_size = window_size, showPlot = showPlots)
        FrustrationDynamiX.temp_coo(jacobian_matrix)
        number_iterations = len(time_vector)
        F, Z, C, D = np.zeros(number_iterations), np.zeros(number_iterations), np.zeros(number_iterations), np.zeros(number_iterations)
        for i in tqdm(range(1,number_iterations)):
            path = "./temp/J_" + str(i) + ".csv"
            G = FrustrationDynamiX.read_graph(path)
            if method == "AND":
                Z[i], F[i], C[i], D[i] = FrustrationDynamiX.ilp_AND_frustration(G, showPlot = showPlots)
            elif method == "XOR":
                Z[i], F[i], C[i], D[i] = FrustrationDynamiX.ilp_XOR_frustration(G, showPlot = showPlots)
            elif method == "ABS":
                Z[i], F[i], C[i], D[i] = FrustrationDynamiX.ilp_ABS_frustration(G, showPlot = showPlots)
        
        self.time_vector = time_vector
        self.edge_deletion = Z
        self.frustration = F
        self.cohesiveness = C
        self.divisiveness = D
        shutil.rmtree("./temp")
        
        return time_vector, F, Z, C, D

    def plot_frustration_series(self, method, xlabel = "Time", ylabel = "Variables and Frustration", title = "Frustration vs. Time", save_plot = None):
        assert method in ["MIC", "MAC", "MES"], "Invalid Method: Method should be MIC or MAC or MES"
        
        if not self.is_normalized:
            warnings.warn("If data points are not normalized between -1 and 1, plot might be out of scale")
        
        for col in self.dynamic_var:
            plt.plot(self.time, self.time_series[col], label=col)
            
        if method == "MIC":
            #assert self.triadic_balance != None, "Missing call: compute_triadic_evolution method should be called first"
            plt.plot(self.time_vector, self.triadic_balance, marker = "x")
        
        elif method == "MAC":
            #assert self.frustration != None, "Missing call: compute_frustration_evolution method should be called first"
            plt.plot(self.time_vector, self.frustration, marker = "x")
        
        elif method == "MES":
            #assert self.frustration != None, "Missing call: compute_frustration_evolution method should be called first"
            plt.plot(self.time_vector, self.cohesiveness, marker = "x")
            plt.plot(self.time_vector, self.divisiveness, marker = "x")
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        if save_plot != None:
            assert type(save_plot) == str, "save_plot variable should have type string, type " + str(type(save_plot)) + " was given instead"
            plt.savefig(save_plot)
        plt.show()