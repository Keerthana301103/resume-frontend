import streamlit as st
import requests
from io import BytesIO
import os
import base64 

# --- CONFIG ---
st.set_page_config(page_title="Resume Converter", layout="centered")
API_URL = "https://resumetemplateconverter.onrender.com/convert-resume/"

# --- UI ---
st.title("Resume Template Converter")
st.write("Upload your resume and select a template to format it.")

TEMPLATE_OPTIONS = {
    "Old Template": "template1",
    "New Template": "template2"
}

selected_template_name = st.selectbox(
    "Select a Template",
    TEMPLATE_OPTIONS.keys()
)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF or DOCX)", 
    type=["pdf", "docx"]
)

if st.button("Convert Resume"):
    if uploaded_file is not None:
        
        template_id_to_send = TEMPLATE_OPTIONS[selected_template_name]
        
        files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
        params = {'template_id': template_id_to_send}

        try:
            with st.spinner(f"Converting using {selected_template_name}..."):
                
                response = requests.post(API_URL, files=files, params=params)

                if response.status_code == 200:
                    st.success("Conversion successful!")
                    
                    # --- 2. START: New Download & Display Logic ---
                    
                    # Get the JSON data from the response
                    data = response.json()
                    
                    # Get the text and display it
                    gemini_text = data.get("gemini_text", "No text returned.")
                    st.subheader("Extracted Text:")
                    st.text_area("", value=gemini_text, height=300)
                    
                    # Get the Base64 file data and decode it
                    file_data_b64 = data.get("file_data_b64")
                    file_bytes = base64.b64decode(file_data_b64)
                    
                    # Get the filename from the API
                    new_download_filename = data.get("file_name", "formatted_resume.docx")

                    st.download_button(
                        label="Download Formatted Resume",
                        data=file_bytes, # <-- Use the decoded bytes
                        file_name=new_download_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    # --- END: New Download & Display Logic ---
                    
                else:
                    st.error(f"API Error: {response.json().get('detail')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: Could not connect to API. {e}")
    else:
        st.warning("Please upload a file first.")

