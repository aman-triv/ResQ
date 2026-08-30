from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ai_services.route_manager import set_active_route

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
    weighted_matrix = []
    for i in range(len(data['distance_matrix'])):
        row = []
        for j in range(len(data['distance_matrix'][i])):
            actual_distance = data['distance_matrix'][i][j]
            urgency = data['urgency_scores'][j]
            
            if j == 0 or i == j:
                cost = actual_distance
            else:
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

    # 7. Print the Results & Register Active Route
    if solution:
        print("\n🚨 LifeGrid VRP Route Engine (Priority + Distance) 🚨")
        print("-" * 55)
        
        index = routing.Start(0)
        plan_output = 'Optimal Rescue Path:\n\n'
        route_distance = 0
        
        # GPS coordinates mapping for locations in mock data
        location_coords = [
            (28.6139, 77.2090),  # 0: Rescue Base (HQ)
            (28.6200, 77.2100),  # 1: Location A
            (28.6250, 77.2150),  # 2: Location B
            (28.6300, 77.2200),  # 3: Location C
            (28.6350, 77.2250)   # 4: Location D
        ]
        optimized_path_coords = []
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            loc_name = data['locations'][node_index]
            urgency = data['urgency_scores'][node_index]
            
            # Extract coordinates for routing manager
            optimized_path_coords.append(location_coords[node_index])
            
            if node_index == 0:
                plan_output += f" 🟢 {loc_name}\n"
            else:
                plan_output += f"   ⬇️\n 🚑 {loc_name} (Urgency: {urgency}/10)\n"
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += data['distance_matrix'][manager.IndexToNode(previous_index)][manager.IndexToNode(index)]
            
        node_index = manager.IndexToNode(index)
        optimized_path_coords.append(location_coords[node_index])
        plan_output += f"   ⬇️\n 🏁 {data['locations'][node_index]} (Return)\n"
        
        # Save route to active memory for en-route matching
        set_active_route("TEAM_ALPHA", optimized_path_coords)
        
        print(plan_output)
        print("-" * 55)
        print(f"📍 Total Physical Distance Traveled: {route_distance} km\n")
    else:
        print("❌ No solution found by the routing engine.")

if __name__ == '__main__':
    main()