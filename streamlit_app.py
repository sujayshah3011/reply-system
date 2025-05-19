import streamlit as st
import requests
import json

st.title("Social Media Reply Generator")

# Form
with st.form("post_form"):
    platform = st.selectbox("Platform", ["Twitter", "LinkedIn", "Instagram"])
    post_text = st.text_area("Post Text", placeholder="Enter the social media post here...")
    submit = st.form_submit_button("Generate Reply")

if submit:
    if not post_text:
        st.error("Please enter a post text.")
    else:
        # Call FastAPI endpoint
        try:
            response = requests.post(
                "http://localhost:8000/reply",
                json={"platform": platform, "post_text": post_text}
            )
            response.raise_for_status()
            result = response.json()
            
            # Display results
            st.success("Reply generated successfully!")
            st.write("**Platform**: " + result["platform"])
            st.write("**Post**: " + result["post_text"])
            st.write("**Generated Reply**: " + result["generated_reply"])
            st.write("**Timestamp**: " + result["timestamp"])
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")