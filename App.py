import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="Poké-Scanner", layout="centered")
st.title("🔍 Poké-Value Scanner")

# Securely get your API Key from Streamlit Secrets
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # --- THE CAMERA WIDGET ---
    img_file = st.camera_input("Scan a Pokémon Card")

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Scanning...", use_container_width=True)
        
        # This is the "Special Instructions" for the AI
        prompt = """
        Analyze this Pokémon card. I am a collector and I need:
        1. CARD IDENTITY: Name, Set Name, and Set Number (e.g., 142/190).
        2. RARITY: Identify the icon at the bottom (Star, Diamond, Circle, etc.).
        3. PRICE: Give an estimated market value based on recent 'Sold' listings online.
        4. AUTHENTICITY: Look for 'Fake' red flags:
           - Does the 'é' in Pokémon have the accent?
           - Is the font standard or does it look 'thin' or 'off'?
           - Is the HP value realistic (e.g., no 9000 HP cards)?
           - Is the holographic pattern vertical (often fake) or textured/diagonal?
        """

        with st.spinner("Consulting the Professor..."):
            response = model.generate_content([prompt, img])
            st.markdown("### 📊 Scan Results")
            st.write(response.text)
else:
    st.info("Please enter your Gemini API Key in the sidebar to start.")
