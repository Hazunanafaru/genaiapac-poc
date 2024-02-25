"""Module providing backend handlers functionality"""
from flask import render_template, request, jsonify, current_app, Blueprint
from llm import llm_inference
# from api import init_app
#
# app = init_app()
handlers_bp = Blueprint('handlers', __name__, template_folder='../templates')

@handlers_bp.route("/")
def home():
    """
    Home Endpoint that render index.html
    """
    return render_template('index.html')

@handlers_bp.route('/api/v1/inference_query', methods=['POST'])
def post_inference_query_llm():
    """
    Inference query to LLM and return dict of answer and latency
    """
    data = request.get_json()
    current_app.logger.debug(f"Request JSON: {data}")

    text = data['text']
    current_app.logger.debug(f"Text data: {text}")

    latency, answer = llm_inference(
        query=text,
        model_path=current_app.config['MODEL_PATH'],
        model_location=current_app.config['MODEL_LOCATION']
    )
    response = {
        "answer": answer,
        "latency": latency
    }
    current_app.logger.debug(f"Response: {response}")
    return jsonify(response)
