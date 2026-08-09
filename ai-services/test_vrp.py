from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    
    # Locations: 0 is Base Station, 1-4 are Emergency SOS Locations
    data['locations'] = [
        'Rescue Base (HQ)', 
        'Location A (Minor Cut)', 
        'Location B (Severe Bleeding)', 
        'Location C (Heart Attack)', 
        'Location D (Fractured Leg)'
    ]
    
    # Urgency Scores from Phase 1 (1 to 10). 0 is for Base.
    data['urgency_scores'] = [0, 2, 8, 10, 5] 
    
    # Distance matrix in kilometers between all locations
    data['distance_matrix'] = [
        [0, 10, 15, 20, 25],  # Distances from Base
        [10, 0, 35, 25, 30],  # Distances from Loc A
        [15, 35, 0, 30, 20],  # Distances from Loc B
        [20, 25, 30, 0, 10],  # Distances from Loc C
        [25, 30, 20, 10, 0],  # Distances from Loc D
    ]
    
    data['num_vehicles'] = 1  # 1 Rescue Ambulance/Team
    data['depot'] = 0         # Starting and ending at Base (Index 0)
    return data

def main():
    # 1. Load Data
    data = create_data_model()
    
    # 2. CREATE PRIORITY-WEIGHTED COST MATRIX (The Magic Algorithm)
    # Reduce effective distance cost for high-urgency locations so the solver goes there first.
    weighted_matrix = []
    for i in range(len(data['distance_matrix'])):
        row = []
        for j in range(len(data['distance_matrix'][i])):
            actual_distance = data['distance_matrix'][i][j]
            urgency = data['urgency_scores'][j]
            
            if j == 0 or i == j:
                # Returning to base or same location has no urgency modifier
                cost = actual_distance
            else:
                # Logic: Cost = Distance * (11 - Urgency)
                # If urgency is 10, multiplier is 1 (Visits immediately)
                # If urgency is 2, multiplier is 9 (Visits later)
                cost = actual_distance * (11 - urgency)
            
            row.append(int(cost))
        weighted_matrix.append(row)

    # 3. Setup OR-Tools Routing Manager & Model
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # 4. Create the Distance Callback using our WEIGHTED matrix
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return weighted_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 5. Set Optimization Strategy
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # 6. Solve the VRP
    solution = routing.SolveWithParameters(search_parameters)

    # 7. Print the Results
    if solution:
        print("\n🚨 LifeGrid VRP Route Engine (Priority + Distance) 🚨")
        print("-" * 55)
        
        index = routing.Start(0)
        plan_output = 'Optimal Rescue Path:\n\n'
        route_distance = 0
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            loc_name = data['locations'][node_index]
            urgency = data['urgency_scores'][node_index]
            
            if node_index == 0:
                plan_output += f" 🟢 {loc_name}\n"
            else:
                plan_output += f"   ⬇️\n 🚑 {loc_name} (Urgency: {urgency}/10)\n"
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            # Calculate ACTUAL distance traveled, not the weighted one
            route_distance += data['distance_matrix'][manager.IndexToNode(previous_index)][manager.IndexToNode(index)]
            
        node_index = manager.IndexToNode(index)
        plan_output += f"   ⬇️\n 🏁 {data['locations'][node_index]} (Return)\n"
        
        print(plan_output)
        print("-" * 55)
        print(f"📍 Total Physical Distance Traveled: {route_distance} km\n")
    else:
        print("❌ No solution found by the routing engine.")

if __name__ == '__main__':
    main()