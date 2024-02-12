from llama_cpp import Llama
import time
from llm.model import download_model, check_model


def llm_inference(query: str, model_location: str, model_path: str):
    """
    Inference qury to LLM model
    Take query and model path then compose query to prompt template
    Return tupple of latency and prompt output
    """

    if model_location != "local" and check_model is False:
        download_model(model_location=model_location, model_path=model_path)

    LLM = Llama(model_path=model_path, n_gpu_layers=32, n_threads=6, n_ctx=3584, n_batch=521, verbose=True, temperature=0, cuda_device=0)

    prompt_template = f"""
    Kamu adalah seorang asisten AI yang akan membantu dokter dalam mengidentifikasi permasalahan pasien. \n
    Kamu akan mendengarkan percakapan antara dokter dengan pasiennya, lalu kamu harus melakukan Name Entity Recognition untuk gejala penyakit pasien. \n
    Contohnya: "Batuk", "Mual", "Bersin", dll. \n
    Setelah melakukan Name Entity Recognition, kamu harus memberikan kemungkinan diagnosa penyakit pasien beserta kemungkinan (dalam persentase) dan alasan akan diagnosa tersebut. \n
    Kamu dapat memberikan lebih dari 1 diagnosa, namun kamu harus menyertakan kemungkinan (dalam persentase) dan alasan untuk masing-masing diagnosa tersebut
    Masukkan kata-kata yang merupakan gejala penyakit tersebut ke dalam format berikut (gantikan huruf xxx): \n\n

    Gejala: xxx \n
    Diagnosa: xxx \n
    Kemungkinan: xxx \n
    Alasan: xxx \n \n

    Sekarang analisalah potongan percakapan berikut! \n

    ```
    {query}
    ```
    """

    before = time.time()
    # Process LLM Inference
    output = LLM(prompt_template, max_tokens=0)
    after = time.time()
    latency = after - before

    return latency, output
