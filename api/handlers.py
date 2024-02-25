"""Module providing backend handlers functionality"""
from flask import render_template, request, jsonify, current_app, Blueprint
from llm import llm_inference

handlers_bp = Blueprint('handlers', __name__, template_folder='../templates')

@handlers_bp.route("/")
def home():
    """
    Render homepage template
    TODO: upgrade index.html
    """
    return render_template('index.html')

@handlers_bp.route("/about")
def about():
    """
    Render about template
    TODO: setup about.html
    """
    return render_template('about.html')

@handlers_bp.route("/version")
def version():
    """
    Render biobyte service version JSON
    """
    version = {
        "name": "biobyte-service",
        "version": "0.1.0-alpha",
        "status": "OK"
    }

    return jsonify(version)

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
