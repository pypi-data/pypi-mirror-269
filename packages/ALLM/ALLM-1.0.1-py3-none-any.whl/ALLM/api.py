from flask import Flask, request, jsonify
from .instruct import load_model
from llama_index.llms.llama_cpp import LlamaCPP
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="127.0.0.1", help="Host on which you wish to run the API server")
parser.add_argument("--port", type=str, default='5000', help="Host on which you wish to run the API server")

app = Flask(__name__)
app.config['DEBUG'] = False

model_files = [f for f in os.listdir('model') if f.endswith('.gguf')]
model_path = load_model(model_files[0]) if model_files else None

def generate(model):
    llm = LlamaCPP(
            model_path=model,
            temperature=0.5,
            max_new_tokens=512,
            context_window=3900,
            verbose=False,
        )
    return llm

def infer(llm, prompt):
    if prompt.lower() == "exit":
        return "Exiting chat."
    response_iter = llm.stream_complete(prompt)
    response_text = ''.join(response.delta for response in response_iter)
    return response_text

@app.route('/')
def index():
    return "Welcome to the All Advance AI API!"

@app.route('/v1/chat/completions', methods=['POST'])
def infer_text():
    user_input = request.data.decode('utf-8')
    print("Received input:", user_input)  # Debug statement

    if model_path is None:
        return "Model is not loaded or initialized. Kindly run 'allm-run --name model_name_or_path' to initialize the model"

    llm = generate(model_path)
    response = infer(llm, user_input)
    print("Generated response:", response)  # Debug statement
    return response

def main():
    args = parser.parse_args()
    host = args.host
    port = args.port
    print(f"Inference is working on http://{host}:{port}/v1/chat/completions")
    app.run(host=host, port=port)
    
if __name__ == '__main__':
    main()
