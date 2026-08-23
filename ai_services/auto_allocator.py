import numpy as np
from scipy.optimize import linear_sum_assignment
from ai_services.hospital_router import calculate_haversine_distance

def auto_allocate_rescue_teams(tickets: list, rescue_teams: list) -> list:
    """
    Bipartite Matching Engine:
    High Priority Tickets ko Nearest + Compatible Rescue Teams ke sath match karta hai.
    """
    if not tickets or not rescue_teams:
        return []

    num_tickets = len(tickets)
    num_teams = len(rescue_teams)

    # Cost Matrix: Rows = Tickets, Cols = Teams
    cost_matrix = np.zeros((num_tickets, num_teams))

    for i, ticket in enumerate(tickets):
        t_lat, t_lng = ticket["latitude"], ticket["longitude"]
        req_vehicle = ticket.get("required_vehicle", "").lower()
        urgency = ticket.get("urgency_score", 5)

        for j, team in enumerate(rescue_teams):
            r_lat, r_lng = team["latitude"], team["longitude"]
            team_vehicle = team.get("vehicle_type", "").lower()

            # 1. Haversine Distance Score
            dist_km = calculate_haversine_distance(t_lat, t_lng, r_lat, r_lng)

            # 2. Vehicle Mismatch Penalty
            vehicle_penalty = 0.0
            if req_vehicle and team_vehicle and req_vehicle != team_vehicle:
                vehicle_penalty = 100.0  # High penalty if vehicle type doesn't match

            # Total Cost (Kam cost = Better Priority)
            # Higher Urgency Score reduces cost so critical cases get matched first
            total_cost = (dist_km * 2.0) + vehicle_penalty - (urgency * 3.0)
            cost_matrix[i, j] = max(0.0, total_cost)

    # SciPy Hungarian Algorithm to find minimum total cost matching
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assignments = []
    for r, c in zip(row_ind, col_ind):
        ticket = tickets[r]
        team = rescue_teams[c]
        dist = calculate_haversine_distance(
            ticket["latitude"], ticket["longitude"],
            team["latitude"], team["longitude"]
        )
        
        assignments.append({
            "ticket_id": ticket["id"],
            "assigned_team_id": team["id"],
            "team_name": team.get("name", "Rescue Team"),
            "distance_km": dist,
            "urgency_score": ticket.get("urgency_score", 5),
            "vehicle_matched": ticket.get("required_vehicle", "").lower() == team.get("vehicle_type", "").lower()
        })

    return assignments


# --- Quick Test ---
if __name__ == "__main__":
    test_tickets = [
        {"id": "TICKET-1", "latitude": 28.6139, "longitude": 77.2090, "urgency_score": 9, "required_vehicle": "fire_truck"},
        {"id": "TICKET-2", "latitude": 28.6200, "longitude": 77.2150, "urgency_score": 6, "required_vehicle": "ambulance"}
    ]
    test_teams = [
        {"id": "TEAM-A", "name": "Fire Squad 1", "latitude": 28.6150, "longitude": 77.2100, "vehicle_type": "fire_truck", "is_available": True},
        {"id": "TEAM-B", "name": "Medical Unit 2", "latitude": 28.6210, "longitude": 77.2160, "vehicle_type": "ambulance", "is_available": True}
    ]
    
    print("Matched Assignments:", auto_allocate_rescue_teams(test_tickets, test_teams))