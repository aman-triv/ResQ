# 1. Python ka lightweight base environment set karo
FROM python:3.10-slim

# 2. Container ke andar humara main working folder '/app' banao
WORKDIR /app

# 3. Computer Vision (YOLOv8/OpenCV) chalane ke liye zaroori system files install karo
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Apni requirements file ko container me copy karo
COPY requirements.txt .

# 5. Saari Python libraries install karo
RUN pip install --no-cache-dir -r requirements.txt

# 6. Apne bache hue saare code files ko container ke andar copy karo
COPY . .

# 7. Project ko run karne ki default command
# Abhi test ke liye hum isko test_full_pipeline.py par point kar rahe hain
CMD ["python", "test_full_pipeline.py"]