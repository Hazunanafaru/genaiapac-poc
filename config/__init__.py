"""Module providing configuration management functionality"""

import os

def load_config() -> dict:
    """
    Load config from environment variable.
    On dev environment type will load after load_dotenv() executed.
    On prod environment type will get environment variables that injected
    either by Docker or Kubernetes.
    Return dict.
    """
    config = {}
    # Load model_path where model is located in server
    # Default to seallm-7b-chat.q4_k_m.gguf
    if os.environ.get('MODEL_PATH') is None:
        config['MODEL_PATH'] = 'seallm-7b-chat.q4_k_m.gguf'
    else:
        config['MODEL_PATH'] = os.environ.get('MODEL_PATH')

    # Load model location type
    # Available option are local and gcs (TODO)
    # Default to local
    match os.environ.get('MODEL_LOCATION'):
        case None:
            config['MODEL_LOCATION'] = 'local'
        case _:
            config['MODEL_LOCATION'] = os.environ.get('MODEL_LOCATION')

    # Determine environment type
    # Availabel options are dev and prod
    # Default to dev
    match os.environ.get('ENVIRONMENT_TYPE'):
        case "dev":
            config['ENVIRONMENT_TYPE'] = "prod"
        case "prod":
            config['ENVIRONMENT_TYPE'] = "prod"
        case _:
            config['ENVIRONMENT_TYPE'] = "dev"

    return config
