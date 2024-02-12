import os

def load_config() -> dict:
    config = {}
    # Load model_path where model is located in server
    # Default to seallm-7b-chat.q4_k_m.gguf
    if os.environ.get('MODEL_PATH') is None:
        config['MODEL_PATH'] = 'seallm-7b-chat.q4_k_m.gguf'
    else:
        config['MODEL_PATH'] = os.environ.get('MODEL_PATH')

    # Load model location type 
    # Available option are local, gcs, and huggingface
    # Default to local
    match os.environ.get('MODEL_LOCATION'):
        case "gcs":
            config['MODEL_LOCATION'] = "gcs"
        case "huggingface":
            config['MODEL_LOCATION'] = "huggingface"
        case _:
            config['MODEL_LOCATION'] = "local"

    # Determine environment type
    # Availabel options are dev and prod
    # Default to dev
    match os.environ.get('ENVIRONMENT_TYPE'):
        case "prod":
            config['ENVIRONMENT_TYPE'] = "prod"
        case _:
            config['ENVIRONMENT_TYPE'] = "dev"

    return config
