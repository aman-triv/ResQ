import json
import random
from faker import Faker

fake = Faker('en_IN') # Indian Names and Context

# Base coordinates around a central location (e.g., Delhi/NCR area)
BASE_LAT = 28.6139
BASE_LNG = 77.2090

EMERGENCY_TEXTS = [
    "Severe flooding near main road, water entering houses. Need boat rescue.",
    "Fire broke out in 3rd floor apartment. People trapped inside.",
    "Injured dog hit by vehicle, needs urgent veterinary care.",
    "Building wall collapsed. 2 people injured and stuck.",
    "Cattle trapped in water near farm field.",
    "Old person with breathing issue, water rising around house.",
    "Electricity pole fallen, sparking near waterlogged street."
]

def generate_mock_incidents(count=20):
    incidents = []
    
    for i in range(1, count + 1):
        is_animal = random.choice([True, False, False]) # 33% chance animal rescue
        category = "animal" if is_animal else "human"
        
        # Random location within ~5-10 km radius
        lat = BASE_LAT + random.uniform(-0.05, 0.05)
        lng = BASE_LNG + random.uniform(-0.05, 0.05)
        
        urgency = random.randint(1, 10)
        
        incident = {
            "id": f"SOS-{1000 + i}",
            "reporter_name": fake.name(),
            "phone_number": fake.phone_number(),
            "description": random.choice(EMERGENCY_TEXTS),
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "urgency_score": urgency,
            "category": category,
            "is_medical_emergency": urgency >= 7,
            "status": "pending",
            "timestamp": fake.date_time_this_month().isoformat()
        }
        incidents.append(incident)
        
    return incidents

if __name__ == "__main__":
    data = generate_mock_incidents(20)
    
    # JSON file me save karo
    with open("mock_sos_data.json", "w") as f:
        json.dump(data, f, indent=4)
        
    print("✅ Successfully generated 'mock_sos_data.json' with 20 dummy cases!")
