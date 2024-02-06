import time
from llama_cpp import Llama
from retriever import doc_retriever

#https://huggingface.co/TheBloke/Llama-2-7B-GGUF

def llm_inference(knowledge_source, query):
    model_path = "./seallm-7b-chat.q4_k_m.gguf"
    LLM = Llama(model_path=model_path, n_gpu_layers=0, n_threads=6, n_ctx=3584, n_batch=521, verbose=True, temperature=0, cuda_device=0)
    prompt_template = f"""Kamu adalah seorang asisten penjawab dokumen.\n
    Kamu harus menjawab pertanyaan dari user secara ringkas dan jelas.\n
    Jika memungkinkan, sertakan juga nomor halaman dari dokumen sumber untuk meningkatkan kredibilitas jawabanmu.\n
    Untuk menjawab pertanyaan dari user mengenai isi dari dokumen tersebut, kamu dapat mengacu pada potongan halaman pada dokumen berikut:\n
    {knowledge_source}\n\n
    ```
    Sekarang jawablah pertanyaan user berikut: "{query}"\n
    Jawaban: 
    ```
    """
    a=time.time()
    output = LLM(prompt_template, max_tokens=0)
    b=time.time()
    c=b-a
    return c, output
