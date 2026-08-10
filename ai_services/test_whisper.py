import whisper

def transcribe_audio(audio_file_path):
    # 'base' model lightweight aur fast hai local machine ke liye
    model = whisper.load_model("base")
    
    # Audio file se text extract kar rahe hain
    result = model.transcribe(audio_file_path)
    return result["text"]

if __name__ == "__main__":
    # Test karne ke liye yahan apni audio file ka naam/path daalo
    audio_path = "sample_sos.wav" 
    
    print("Audio process ho raha hai...\n")
    try:
        transcription = transcribe_audio(audio_path)
        print("--- VOICE-NOTE TO TEXT OUTPUT ---")
        print(transcription)
    except Exception as e:
        print(f"Error: {e}")