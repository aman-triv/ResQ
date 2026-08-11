import time
import json
import ollama
import whisper
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Preload fast models into RAM
whisper_model = whisper.load_model("tiny")
FAST_LLM = "llama3.2"

def parse_sos_text(sos_text: str):
    """Processes incoming raw text and returns structured JSON."""
    prompt = f"""Extract details from this emergency text and return ONLY JSON:
Text: "{sos_text}"
JSON format:
{{"urgency_score": <1-10>, "category": "<Human/Animal>", "is_medical": <true/false>, "summary": "<short description>"}}"""

    response = ollama.chat(
        model=FAST_LLM,
        messages=[{'role': 'user', 'content': prompt}],
        options={'num_predict': 60, 'temperature': 0.1},
        keep_alive='10m'
    )
    return response['message']['content']

def transcribe_audio(audio_path: str):
    """Converts audio voice note into text using Whisper Tiny."""
    result = whisper_model.transcribe(audio_path)
    return result.get('text', '')

def generate_first_aid(emergency_desc: str):
    """Generates sub-2s fast first-aid steps."""
    prompt = f"Provide 3 critical emergency first-aid steps for: {emergency_desc}"
    response = ollama.chat(
        model=FAST_LLM,
        messages=[{'role': 'user', 'content': prompt}],
        options={'num_predict': 50, 'temperature': 0.1},
        keep_alive='10m'
    )
    return response['message']['content']

def calculate_optimal_route(locations: list, urgency_scores: list, distance_matrix: list):
    """Priority + Distance VRP solver via Google OR-Tools."""
    weighted_matrix = []
    for i in range(len(distance_matrix)):
        row = []
        for j in range(len(distance_matrix[i])):
            dist = distance_matrix[i][j]
            urgency = urgency_scores[j]
            cost = dist if (j == 0 or i == j) else dist * (11 - urgency)
            row.append(int(cost))
        weighted_matrix.append(row)

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_idx, to_idx):
        return weighted_matrix[manager.IndexToNode(from_idx)][manager.IndexToNode(to_idx)]

    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)
    
    route = []
    if solution:
        idx = routing.Start(0)
        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            route.append({"location": locations[node], "urgency": urgency_scores[node]})
            idx = solution.Value(routing.NextVar(idx))
        route.append({"location": locations[manager.IndexToNode(idx)], "urgency": 0})
    return route

def process_sos_pipeline(text: str = "", image_path: str = None, location: tuple = None):
    """Orchestrates text parsing and returns consolidated AI results."""
    parsed_result = {}
    if text:
        try:
            raw_res = parse_sos_text(text)
            parsed_result = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        except Exception:
            parsed_result = {"urgency_score": 5, "category": "Human", "is_medical": False}

    return {
        "urgency_score": parsed_result.get("urgency_score", 5),
        "is_animal": True if parsed_result.get("category") == "Animal" else False,
        "is_duplicate": False
    }

# 👉 Test script sabse niche rahegi
if __name__ == "__main__":
    print("🚀 Testing Consolidated AI Pipeline Module...")
    # ... test code ...