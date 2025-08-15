import os
import time
import pandas as pd
import networkx as nx
from pyscipopt import Model, quicksum

# Step 1: Load data
def load_data(drivers_file, riders_file, graph_file):
    drivers_df = pd.read_csv(drivers_file)
    riders_df = pd.read_csv(riders_file)
    graph_df = pd.read_csv(graph_file)
    return drivers_df, riders_df, graph_df

# Step 2: Prepare drivers and riders data
def prepare_data(drivers_df, riders_df):
    drivers = []
    for _, row in drivers_df.iterrows():
        drivers.append({
            'id': row['id'],
            'source': row['source'],
            'destination': row['destination'],
            'seats': row['seats'],
            'threshold': row['threshold']
        })

    riders = [{'id': row['id'], 'source': row['source'], 'destination': row['destination']} for _, row in riders_df.iterrows()]
    return drivers, riders

# Step 3: Build graph from graph_df
def build_graph(graph_df):
    G = nx.DiGraph()
    for _, row in graph_df.iterrows():
        G.add_edge(row['source'], row['destination'], weight=row['weight'])
    return G

# Step 4: Define optimization model
def define_model(G, drivers, riders):
    num_drivers = len(drivers)
    num_riders = len(riders)
    model = Model("rideshare_optimization")

    # Define decision variables
    I = {}
    for i in range(num_drivers):
        for j in range(num_riders):
            I[i, j] = model.addVar(vtype="B", name=f"I_{i}_{j}")  # Binary variable

    # Objective - Maximize the number of riders assigned to drivers
    model.setObjective(
        quicksum(I[i, j] for i in range(num_drivers) for j in range(num_riders)), "maximize"
    )

    # Constraint for each driver to ensure the deviated path length does not exceed the maximum allowed distance
    for i, driver in enumerate(drivers):
        max_distance = nx.shortest_path_length(G, source=driver['source'], target=driver['destination'], weight='weight') * (1 + driver['threshold'] / 100)
        for j, rider in enumerate(riders):
            if nx.has_path(G, driver['source'], rider['source']) and nx.has_path(G, rider['source'], rider['destination']) and nx.has_path(G, rider['destination'], driver['destination']):
                deviated_path_length = (nx.shortest_path_length(G, source=driver['source'], target=rider['source'], weight='weight') +
                                        nx.shortest_path_length(G, source=rider['source'], target=rider['destination'], weight='weight') +
                                        nx.shortest_path_length(G, source=rider['destination'], target=driver['destination'], weight='weight'))
                model.addCons(I[i, j] * deviated_path_length <= max_distance, f"deviated_path_driver_{i}_rider_{j}")

    # Unique Assignment Constraint for each rider
    for j in range(num_riders):
        model.addCons(
            quicksum(I[i, j] for i in range(num_drivers)) <= 1, f"unique_assignment_rider_{j}"
        )

    # Car Capacity Constraint for each driver
    for i, driver in enumerate(drivers):
        model.addCons(
            quicksum(I[i, j] for j in range(num_riders)) <= driver['seats'], f"car_capacity_driver_{i}"
        )

    return model, I

# Step 5: Solve model and display results
def solve_model(model, I, drivers, riders):
    model.optimize()
    if model.getStatus() == "optimal":
        print("Objective value (max riders accommodated):", model.getObjVal())
        accommodated_riders = 0
        for i in range(len(drivers)):
            for j in range(len(riders)):
                if model.getVal(I[i, j]) > 0.5:  # Variable is binary
                    print(f"Rider {riders[j]['id']} assigned to Driver {drivers[i]['id']}")
                    accommodated_riders += 1
        print(f"Number of accommodated riders: {accommodated_riders}")
    else:
        print("No feasible solution found.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    # Start the timer
    start_time = time.time()
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'Input2')

    # Set paths for input files
    drivers_file = os.path.join(input_dir, 'drivers.csv')
    riders_file = os.path.join(input_dir, 'riders.csv')
    
    map_dir = os.path.join(script_dir, 'map')
    graph_file = os.path.join(map_dir, 'graph.csv')
    
    # Load data
    drivers_df, riders_df, graph_df = load_data(drivers_file, riders_file, graph_file)
    
    # Prepare drivers and riders data
    drivers, riders = prepare_data(drivers_df, riders_df)
    
    # Build the graph
    G = build_graph(graph_df)
    
    # Define the optimization model
    model, I = define_model(G, drivers, riders)
    
    # Solve the model and display results
    solve_model(model, I, drivers, riders)
    
    # End the timer and print execution time
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
