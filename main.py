import streamlit as st
import requests
import re
import json
from PIL import Image

def send_to_api(data):
    url = "https://bd63ab6e-971e-4fb8-9357-8001d6cc7294.mock.pstmn.io"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={"codes": data}, headers=headers)
    
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = "Could not decode JSON from response"
        
    return response.status_code, response_data

def main():
    # Display logo
    logo = Image.open("Logo_FiHogar (1).png")
    st.image(logo, use_column_width=True)
    
    st.title("Streamlit Web App to Send Codes to API")

    uploaded_file = st.file_uploader("Upload a TXT file", type=["txt"])
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        # Reading the file content and separating numbers
        content = uploaded_file.read().decode("utf-8")
        lines = content.split('\n')
        codes = [re.sub(r'\D', '', line) for line in lines if line.strip() != '']
        
        # Displaying separated numbers
        st.write("Separated Codes:")
        st.write(codes)
        
        # Preparing payload
        payload = {"codes": codes}
        
        # Displaying payload
        payload_str = json.dumps(payload, indent=4)
        st.write("Payload to be sent to API:")
        st.code(payload_str, language='json')
        
        # Sending data to API
        if st.button("Send to API"):
            status_code, response_data = send_to_api(codes)
            st.write(f"API Status Code: {status_code}")
            st.write("API Response:")
            st.write(response_data)

if __name__ == "__main__":
    main()
