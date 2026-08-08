import json

DEMO_SCENARIOS = {
    "scenario_human_trauma": {
        "title": "Scenario A: Building Collapse & Medical Emergency",
        "input_type": "Image + Text",
        "description": "Building wall collapsed near Market, 2 people severely injured.",
        "expected_category": "human",
        "expected_urgency": 9,
        "action": "Routes to Nearest Trauma & ICU Hospital"
    },
    "scenario_animal_rescue": {
        "title": "Scenario B: Animal Distress in Waterlogging",
        "input_type": "Image",
        "description": "Dog hit by car and trapped near flooded drainage.",
        "expected_category": "animal",
        "expected_urgency": 7,
        "action": "Routes to Nearest Veterinary Rescue Center"
    },
    "scenario_duplicate_surge": {
        "title": "Scenario C: Panic Surge Deduplication",
        "input_type": "Multi-SOS Stream",
        "description": "15 duplicate SOS reports received within 50 meters radius.",
        "expected_action": "DBSCAN clusters 15 alerts into 1 Master Ticket"
    }
}

def export_demo_scenarios():
    with open("demo_scenarios.json", "w") as f:
        json.dump(DEMO_SCENARIOS, f, indent=4)
    print("✅ Created 'demo_scenarios.json' for Pitch Presentation!")

if __name__ == "__main__":
    export_demo_scenarios()
