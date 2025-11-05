from gpt4all import GPT4All
import os

# ✅ Always use raw string (r"...") for Windows paths to avoid \U errors
MODEL_PATH = r"C:\Users\Veneel\rag-ai-platform\models\mistral-7b-openorca.Q3_K_M.gguf"

def get_generator(model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    # Initialize GPT4All model from local path
    model = GPT4All(model_path)
    return model

def generate_answer(model, prompt, max_tokens=256):
    """
    Generates a response using the local GPT4All model.
    """
    response = model.generate(prompt, max_tokens=max_tokens)
    return response
