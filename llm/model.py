import io
import os
from requests import get
from google.cloud import storage

def download_model(model_location: str, model_path: str) -> str:
    """
    Download LLM Model from gcs or huggingface.
    Take model_location and model_path.
    For model stored in gcs, use google cloud storage lib to download model.
    For model stored in huggingface, use requests lib to stream download model.
    Return str of model name.
    Example:
    >>> download_model(model_location="gcs", model_path="gs://genai/model/seallm.gguf")
    "seallm.gguf"
    """
    model_name = model_path.split("/")[-1]

    match model_location:
        case "gcs":
            gcs_bucket = model_path.split("/")[2]
            gcs_blob = model_path.split(gcs_bucket)[1][1:]

            gcs_client = storage.Client()

            file_obj = io.BytesIO()

            bucket = gcs_client.bucket(gcs_bucket)
            blob = bucket.blob(gcs_blob)
            blob.download_to_filename(file_obj)
                
            # Before reading from file_obj, remember to rewind with file_obj.seek(0).
            # Reference: https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_download_to_stream.py#L48
            file_obj.seek(0)
            return model_name
        case "huggingface":
            url = model_path + "?download=true"
            with get(url, stream=True) as response:
                response.raise_for_status()
                with open(model_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=10*1024*1024):
                        file.write(chunk)
            return model_name
        case _:
            raise Exception("""
            External model location supported are gcs and huggingface.
            For gcs, make sure your model_path follow this format:
            gs://<bucket_name>/<bucket_path>/<model_file_name>
            For huggingface, make sure your model_path follow this format:
            https://huggingface.co/<author>/<model_name>/blob/main/<model_file_name>.gguf
            """)

def check_model(model_path: str) -> bool:
    """
    Check model availability in local directory
    Take model_path from model_location hugginface or gcs.
    Check the last path of huggingface or gcs endpoint to set the model_name.
    Then check if the same model_name is available in current directory.
    Return boolean. True if file exist and False if not.
    """
    model_name = model_path.split("/")[-1]
    if os.path.isfile(os.getcwd() + "/" + model_name):
        return True
    return False
