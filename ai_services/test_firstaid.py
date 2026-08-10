import ollama

def get_first_aid_guidance(emergency_type):
    prompt = f"""
    You are an emergency medical and safety guide.
    Provide 3 to 4 short, actionable, and critical offline first-aid or safety tips for this situation: "{emergency_type}".
    Keep points very brief, clear, and easy to read during panic.
    """
    
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']

if __name__ == "__main__":
    # Test Emergency Situation
    sample_crisis = "Leg severe fracture and heavy bleeding"
    
    print("Offline First-Aid Tips generate ho rahe hain...\n")
    tips = get_first_aid_guidance(sample_crisis)
    
    print("--- FIRST-AID & SAFETY GUIDANCE ---")
    print(tips)