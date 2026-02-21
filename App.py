import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Poké-Scanner", layout="centered")
st.title("🔍 Poké-Scanner Diagnostic")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- DIAGNOSTIC: List available models ---
        st.sidebar.write("### Available Models:")
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m_name in available_models:
            st.sidebar.code(m_name)

        # We'll try the most stable standard model for 2026
        # If this fails, look at the list in the sidebar and swap the name!
        model_name = 'gemini-2.0-flash' 
        model = genai.GenerativeModel(model_name)

        img_file = st.file_uploader("Upload Card Photo", type=["jpg", "png", "jpeg"])

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            if st.button("🔍 Scan Now"):
                with st.spinner("Analyzing..."):
                    # Use a very simple prompt to test connection
                    response = model.generate_content(["Identify this Pokemon card", img])
                    st.write(response.text)

    except Exception as e:
        st.error(f"Professor is still confused: {e}")
        st.info("Check the sidebar! If you don't see a list of 'models/gemini...', your API key might not be fully activated yet.")
else:
    st.info("👈 Paste your key in the sidebar. Make sure you clicked 'Continue' on the Google AI Studio setup screen first!")
