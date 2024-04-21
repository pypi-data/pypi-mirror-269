from flask import Flask, request, jsonify
from llama_index.llms.llama_cpp import LlamaCPP
from .instruct import load_model
import os

app = Flask(__name__)

# Check if apiconfig.txt exists in the model folder
config_file_path = os.path.join('model', 'apiconfig.txt')
if not os.path.exists(config_file_path):
    # Create apiconfig.txt with default values
    with open(config_file_path, 'w') as file:
       file.write('Host=127.0.0.1\n')
       file.write('Port=5000\n')
       file.write('CertFile=""\n')
       file.write('CertKey=""\n')

# Read host and port from apiconfig.txt
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == 'Host':
                host = value
            elif key == 'Port':
                port = int(value)
            elif key == 'CertFile':
                cert_file = value.strip('"')
            elif key == 'CertKey':
                cert_key = value.strip('"')
else:
    print("File doesn't exist.")
    host = '127.0.0.1'
    port = 5000
    cert_file = ""
    cert_key = ""

print("Host:", host)
print("Port:", port)
print("CertFile:", cert_file)
print("CertKey:", cert_key)

model_files = [f for f in os.listdir('model') if f.endswith('.gguf')]
model_path = load_model(model_files[0]) if model_files else None

llm = LlamaCPP(
    model_path=model_path,
    temperature=0.1,
    max_new_tokens=512,
    context_window=3900,
    model_kwargs={"n_gpu_layers": 0},
    verbose=False,
)

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    user_input = request.json.get("input")

    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting chat."})

    prompt_template = "<s>[INST] {prompt} [/INST]"
    prompt = prompt_template.format(prompt=user_input)

    response_iter = llm.stream_complete(prompt)
    response_text = ''.join(response.delta for response in response_iter)

    return jsonify({"response": response_text})

def main():
        print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
        if cert_file is not "" and cert_key is not "":
            app.run(host=host, port=port, debug=False, ssl_context=[cert_file,cert_key])
        else:
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
