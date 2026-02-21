import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- APP SETUP ---
st.set_page_config(page_title="Poké-Scanner", layout="centered")
st.title("🔍 Poké-Scanner")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # This part automatically finds the best "Flash" model in your sidebar list
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        primary_model = "models/gemini-2.5-flash" if "models/gemini-2.5-flash" in available_models else available_models[0]
        
        model = genai.GenerativeModel(primary_model)
        st.sidebar.success(f"Connected: {primary_model.split('/')[-1]}")

        img_file = st.file_uploader("Upload Card Photo", type=["jpg", "png", "jpeg"])

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            if st.button("🔍 Scan Card"):
                with st.spinner("Professor is analyzing..."):
                    try:
                        # 2-second delay to respect the free tier speed limits
                        time.sleep(2) 
                        prompt = "Identify this Pokemon card. Tell me the Name, Set, Number, and Estimated Value."
                        response = model.generate_content([prompt, img])
                        
                        st.markdown("### 📊 Results")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Scan failed: {e}")
                        st.info("If it says 'Quota Exceeded', just wait 30 seconds and try one more time!")
    except Exception as e:
        st.error(f"Connection Error: {e}")
else:
    st.info("👈 Please paste your NEW API key in the sidebar.")
