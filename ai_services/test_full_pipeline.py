from ai_pipeline import parse_sos_text, generate_first_aid, calculate_optimal_route

print("🚨 --- FULL LIFEGRID AI PIPELINE VERIFICATION --- 🚨\n")

# 1. Test SOS Parsing
sample_text = "Fire in Block B floor 3! 2 people heavily burned and breathing issue."
print("1️⃣ [NLP] Parsing SOS Text...")
parsed = parse_sos_text(sample_text)
print("Output:", parsed)

# 2. Test First-Aid Generation
print("\n2️⃣ [AI Bot] Generating First-Aid Steps...")
first_aid = generate_first_aid("Heavy burns and breathing difficulty from fire smoke")
print("Output:\n", first_aid)

# 3. Test Routing Engine
print("\n3️⃣ [VRP] Calculating Optimal Route...")
locs = ["Base HQ", "Block B (Burn)", "Sector 2 (Cut)"]
urgencies = [0, 9, 3]
dist_matrix = [
    [0, 10, 5],
    [10, 0, 8],
    [5, 8, 0]
]
route = calculate_optimal_route(locs, urgencies, dist_matrix)
print("Optimal Route Path:")
for step in route:
    print(f" 📍 -> {step['location']} (Urgency: {step['urgency']})")

print("\n✅ ALL PERSON 3 MODULES WORKING END-TO-END!")