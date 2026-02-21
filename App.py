import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from google.api_core.exceptions import ResourceExhausted

# --- APP CONFIG ---
st.set_page_config(page_title="Poké-Scanner", layout="centered")
st.title("🔍 Poké-Value Scanner")

# Sidebar for the API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # UPDATED: The correct 2026 model name string
        model = genai.GenerativeModel('gemini-3-flash')

        st.write("### Choose how to scan:")
        option = st.radio("", ["🖼️ Upload from Gallery", "📱 Use Camera"])

        img_file = None
        if option == "📱 Use Camera":
            img_file = st.camera_input("Take a picture")
        else:
            img_file = st.file_uploader("Choose a photo", type=["jpg", "png", "jpeg"])

        if img_file:
            img = Image.open(img_file)
            st.image(img, caption="Ready to analyze!", use_container_width=True)
            
            prompt = """
            Analyze this Pokémon card for a collector. Provide:
            1. CARD IDENTITY: Name, Set, and Number.
            2. RARITY: Describe the symbol (Star, Circle, etc.).
            3. VALUE: Estimated market price for an ungraded card.
            4. AUTHENTICITY: Check font, HP, and holo style for red flags.
            """

            if st.button("🔍 Scan Card Now"):
                with st.spinner("Consulting the Professor..."):
                    try:
                        # Small delay for free tier stability
                        time.sleep(1) 
                        response = model.generate_content([prompt, img])
                        st.markdown("### 📊 Scan Results")
                        st.write(response.text)
                    except ResourceExhausted:
                        st.error("😅 AI is busy! Wait 60 seconds and try again.")
                    except Exception as e:
                        st.error(f"Professor is confused: {e}")
    except Exception as setup_error:
        st.error(f"Setup error: {setup_error}")
else:
    st.info("👈 Please enter your Gemini API Key in the sidebar to wake up the AI.")
