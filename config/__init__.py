"""Module providing configuration management functionality"""

import os, logging

class Config(object):
    MODEL_PATH = os.environ.get('MODEL_PATH')
    MODEL_LOCATION = os.environ.get('MODEL_LOCATION')
    ENVIRONMENT_TYPE = os.environ.get('ENVIRONMENT_TYPE')
    DEBUG = os.environ.get('DEBUG')

    # Load model_path where model is located in server
    # Default to seallm-7b-chat.q4_k_m.gguf
    if os.environ.get('MODEL_PATH') is None:
        logging.warning("""
        Environment Variable MODEL_PATH is not set. Default to SEALLM.
        """)
        MODEL_PATH = 'seallm-7b-chat.q4_k_m.gguf'
    else:
        MODEL_PATH = os.environ.get('MODEL_PATH')

    # Load model location type
    # Available option are local, gcs, and huggingface
    # Default to local
    match os.environ.get('MODEL_LOCATION'):
        case "gcs":
            MODEL_LOCATION = "gcs"
        case "huggingface":
            MODEL_LOCATION = "huggingface"
        case "local":
            MODEL_LOCATION = "local"
        case _:
            logging.warning("""
            Environment Variable MODEL_LOCATION is not set. Default to local.
            """)
            MODEL_LOCATION = "local"

    # Determine environment type
    # Available options are dev and prod
    # Default to dev
    match os.environ.get('ENVIRONMENT_TYPE'):
        case "prod":
            ENVIRONMENT_TYPE = "prod"
        case "dev":
            ENVIRONMENT_TYPE = "dev"
        case _:
            logging.warning("""
            Environment Variable ENVIRONMENT_TYPE is not set. Default to dev.
            """)
            ENVIRONMENT_TYPE = "dev"

    # Determine to activate debug mode
    # Available options are true and false
    # Default to false
    match os.environ.get('DEBUG'):
        case "true":
            DEBUG = True
        case "false":
            DEBUG = False
        case _:
            DEBUG = False
