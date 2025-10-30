import streamlit as st
import requests
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Resume Converter", layout="centered")

# This is the URL of your deployed API
API_URL = "https://resumetemplateconverter.onrender.com/convert-resume/"

# --- UI ---
st.title("📄 Resume Template Converter")
st.write("Upload your resume and select a template to format it.")

template_id = st.selectbox(
    "Select a Template",
    ("template1", "template2")
)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF or DOCX)", 
    type=["pdf", "docx"]
)

if st.button("Convert Resume"):
    if uploaded_file is not None:
        files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
        params = {'template_id': template_id}

        try:
            with st.spinner(f"Converting using {template_id}..."):

                # === THIS IS THE "INTEGRATION" ===
                # Your Streamlit frontend calls your FastAPI backend.
                response = requests.post(API_URL, files=files, params=params)
                # ===================================

                if response.status_code == 200:
                    st.success("Conversion successful! 🎉")

                    st.download_button(
                        label="Download Formatted Resume",
                        data=BytesIO(response.content),
                        file_name=f"{template_id}_Formatted_{uploaded_file.name}",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                else:
                    st.error(f"API Error: {response.json().get('detail')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: Could not connect to API. {e}")
    else:
        st.warning("Please upload a file first.")