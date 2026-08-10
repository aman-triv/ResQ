import time
import ollama
import whisper

print("⚡ Running Ultra-Optimized Latency Test...\n")

# Whisper model loaded
whisper_model = whisper.load_model("tiny")

# Benchmark Ollama with VRAM pin & trimmed token length
start_time = time.time()
response = ollama.chat(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': 'Urgent: Patient has severe chest pain. Give 3 quick first-aid steps.'}],
    options={
        'num_predict': 30,  # Concise fast response
        'temperature': 0.1
    },
    keep_alive='10m'  # Keeps model active in RAM/VRAM
)
ollama_time = time.time() - start_time

print(f"⏱️ Ollama (1B Model) Response Time: {ollama_time:.2f} seconds")
print("-" * 45)

if ollama_time < 2.0:
    print("✅ SUCCESS: Latency is under 2 seconds Target!")
else:
    print("⚠️ Still over 2s. Needs minor tweak.")