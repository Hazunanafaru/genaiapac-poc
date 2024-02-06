import os
import base64
import streamlit as st
from file_management import save_uploaded_file, list_files, delete_file, UPLOAD_DIRECTORY
from retriever import doc_indexer, doc_retriever
from model import llm_inference

st.title("SMART DOCUMENT ASSISTANT")

if 'chat_visible' not in st.session_state:
    st.session_state.chat_visible = False
if 'active_document' not in st.session_state:
    st.session_state.active_document = ''
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None

def toggle_chat_visibility(filename):
    st.session_state.chat_visible = not st.session_state.chat_visible
    st.session_state.active_document = filename
    if st.session_state.chat_visible:
        st.session_state.vector_db = doc_indexer(filename)

with st.container():
    st.subheader("Upload Dokumen PDF")
    uploaded_file = st.file_uploader("", type="pdf")
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"Dokumen {uploaded_file.name} sudah terupload")

with st.container():
    st.subheader("Dokumen Terupload")
    all_files = list_files(UPLOAD_DIRECTORY)

    for filename in all_files:
        with st.expander(f"{filename}", expanded=False):
            file_path = os.path.join(UPLOAD_DIRECTORY, filename)
            cols = st.columns([1, 1, 1, 1])

            with cols[0]:
                if st.button(f"Buka File", key=f"open_{filename}"):
                    with open(file_path, "rb") as pdf_file:
                        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
                    pdf_display = f'''<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'''
                    st.markdown(pdf_display, unsafe_allow_html=True)

            with cols[1]:
                with open(file_path, "rb") as pdf_file:
                    st.download_button(label="Download File", data=pdf_file, file_name=filename, mime="application/pdf", key=f"download_{filename}")

            with cols[2]:
                if st.button("Hapus File", key=f"delete_{filename}"):
                    delete_file(file_path)
                    st.experimental_rerun()

            with cols[3]:
                if st.button("QnA dengan Dokumen", key=f"chat_{filename}"):
                    toggle_chat_visibility(filename)

if st.session_state.chat_visible and st.session_state.active_document and st.session_state.vector_db:
    with st.container():
        st.header(f"QnA dengan Dokumen {st.session_state.active_document}")
        user_input = st.text_input("Tanyakan sesuatu mengenai dokumen ini:", key="user_input")
        if user_input:
            knowledge_source = doc_retriever(st.session_state.vector_db, user_input)
            bot_latency, output = llm_inference(knowledge_source, user_input)
            bot_answer = output['choices'][0]['text'].strip()
            st.write(f"{bot_answer}\n\nJawaban ini digenerate dalam waktu {bot_latency} detik.")