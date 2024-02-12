"""Module providing API functionality"""

from flask import Flask, render_template, request, jsonify
from llm import llm_inference
from config import load_config

app = Flask(__name__, template_folder="../templates")
config = load_config()

@app.route("/")
def home():
    """
    Home Endpoint that render index.html
    """
    return render_template('index.html')

@app.route('/api/v1/inference_query', methods=['POST'])
def post_inference_query_llm():
    """
    Inference query to LLM and return dict of answer and latency
    """
    data = request.get_json()
    text = data['text']
    bot_latency, output = llm_inference(query=text, model_path=config['MODEL_PATH'])
    bot_answer = output['choices'][0]['text'].strip()
    response = {
        "answer": bot_answer,
        "latency": bot_latency
    }
    print(response)
    return jsonify(response)

def init_api():
    """
    Init Flask API based on environment type
    """
    if config['ENVIRONMENT_TYPE'] == "prod":
        app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)
