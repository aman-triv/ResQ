# Phase 1: Local LLM Setup & SOS Text Parsing
import ollama
import json

def analyze_sos_text(user_text):
    system_prompt = """
    You are an emergency triage AI for disaster rescue.
    Analyze the user emergency message and output ONLY a valid JSON object.
    Do NOT include any markdown block (like ```json), no intro text, no explanation.

    Required JSON Structure:
    {
        "urgency_score": <integer from 1 to 10>,
        "category": "'human' or 'animal' (Strictly choose 'animal' if the victim is a dog, cat, cow, pet, or any animal. Choose 'human' only for people).",
        "is_medical_emergency": <true or false>,
        "summary": "<max 6 words summary of the crisis>"
    }
    """

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_text}
        ],
        format='json'
    )

    try:
        result_json = json.loads(response['message']['content'])
        return result_json
    except Exception as e:
        return {"error": "Failed to parse JSON", "raw": response['message']['content']}

if __name__ == "__main__":
    sample_emergency = "Bhai 3 log building me aag me fase hain, leg me severe fracture hai kisi ko jaldi ambulance bhejo!"
    
    print("AI Emergency Text Process kar raha hai...\n")
    output = analyze_sos_text(sample_emergency)
    print("--- AI OUTPUT (JSON) ---")
    print(json.dumps(output, indent=2))
def get_first_aid_instruction(category, is_medical, summary):
    """
    Victim ko immediate offline First-Aid aur survival tips dene ke liye
    """
    system_prompt = """
    You are an emergency First-Aid Assistant in India. 
    Give 3 short, practical bullet points on what the person should do RIGHT NOW to stay safe before rescue arrives.
    CRITICAL RULE: Strictly use Indian emergency numbers (like 112) and NEVER mention 911.
    Keep instructions simple and under 30 words total.
    """
    
    user_context = f"Category: {category}, Medical Emergency: {is_medical}, Situation: {summary}"
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_context}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return "1. Stay calm. 2. Stop severe bleeding if any. 3. Stay in a safe spot."
def get_destination_facility(category, lat, lng):
    """
    Dual Routing Logic: Category (human vs animal) ke basis par 
    nearest facility (Hospital vs Vet Clinic) return karta hai.
    """
    if category and category.lower() == "animal":
        return {
            "facility_type": "Veterinary Hospital / Animal Rescue",
            "name": "City Animal Shelter & Emergency Vet Care",
            "estimated_distance_km": 2.5,
            "helpline": "+91-9876543210"
        }
    else:
        return {
            "facility_type": "Trauma Center / General Hospital",
            "name": "City General Hospital & Emergency Care",
            "estimated_distance_km": 1.5,
            "helpline": "+91-102 / +91-112"
        }