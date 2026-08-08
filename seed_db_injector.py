import sqlite3
import random
from faker import Faker

fake = Faker('en_IN')
DB_NAME = "resqgrid.db"

def initialize_and_seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Create SOS Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sos_requests (
        id TEXT PRIMARY KEY,
        reporter_name TEXT,
        phone TEXT,
        description TEXT,
        latitude REAL,
        longitude REAL,
        urgency_score INTEGER,
        category TEXT,
        is_medical INTEGER,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Insert Dummy SOS Requests
    base_lat, base_lng = 28.6139, 77.2090
    categories = ["human", "animal", "human"]

    for i in range(1, 26):
        sos_id = f"SOS-100{i}"
        cat = random.choice(categories)
        urgency = random.randint(3, 10)
        lat = base_lat + random.uniform(-0.04, 0.04)
        lng = base_lng + random.uniform(-0.04, 0.04)

        cursor.execute('''
        INSERT OR REPLACE INTO sos_requests 
        (id, reporter_name, phone, description, latitude, longitude, urgency_score, category, is_medical, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sos_id,
            fake.name(),
            fake.phone_number(),
            f"Emergency SOS Alert near area {i}: need urgent help.",
            lat,
            lng,
            urgency,
            cat,
            1 if urgency >= 7 else 0,
            "pending"
        ))

    conn.commit()
    conn.close()
    print(f"✅ Successfully created '{DB_NAME}' and injected 25 Seed SOS records!")

if __name__ == "__main__":
    initialize_and_seed_database()
