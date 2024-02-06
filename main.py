import os
import streamlit as st
import base64

# Directory where uploaded files will be stored
UPLOAD_DIRECTORY = "uploaded_files"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to the directory."""
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def list_files(directory):
    """Lists files in a directory."""
    return os.listdir(directory)

def delete_file(file_path):
    """Deletes a file from the directory."""
    if os.path.exists(file_path):
        os.remove(file_path)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generates an HTML download link."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Streamlit widgets
st.title("PDF Document Opener")

# Upload file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.success(f"Uploaded {uploaded_file.name}")

# List uploaded files
st.header("Uploaded Documents")
all_files = list_files(UPLOAD_DIRECTORY)

for filename in all_files:
    st.text(filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    # Check if the file exists before displaying or offering download
    if os.path.exists(file_path):
        # Display PDF
        if st.button(f"Open {filename}"):
            with open(file_path, "rb") as pdf_file:
                base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_display = f'''<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'''
            st.markdown(pdf_display, unsafe_allow_html=True)

        # Download button using Streamlit's built-in functionality
        with open(file_path, "rb") as pdf_file:
            st.download_button(label=f"Download {filename}", 
                               data=pdf_file, 
                               file_name=filename, 
                               mime="application/pdf")

    # Delete button
    if st.button(f"Delete {filename}"):
        delete_file(file_path)
        st.experimental_rerun()