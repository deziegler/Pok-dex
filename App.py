import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from google.api_core.exceptions import ResourceExhausted

# --- CONFIGURATION ---
st.set_page_config(page_title="Poké-Scanner", layout="centered")
st.title("🔍 Poké-Value Scanner")

# Securely get your API Key from Streamlit Secrets
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using a slightly faster, more stable model for free tier
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.write("### Choose how to scan:")
    # Give the user a choice between camera and file upload
    option = st.radio("", ["📱 Use Camera", "🖼️ Upload from Gallery"])

    img_file = None
    if option == "📱 Use Camera":
        img_file = st.camera_input("Take a picture")
    else:
        img_file = st.file_uploader("Choose a photo", type=["jpg", "png", "jpeg"])

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Ready to analyze!", use_container_width=True)
        
        # The "Special Instructions" for the AI
        prompt = """
        Analyze this Pokémon card. I am a collector.
        Please provide the following details clearly:
        1.  **CARD IDENTITY:** Exact Name, Set Name, and Set Number (e.g., Charizard VMAX, Shining Fates, SV107/SV122).
        2.  **RARITY SYMBOL:** Describe the specific rarity icon found on the card (e.g., "White Star", "Silvery-White Star with gold outline").
        3.  **ESTIMATED MARKET VALUE:** Provide a price range based on recent sold listings for an ungraded card in near-mint condition.
        4.  **AUTHENTICITY CHECKLIST:** Review the image for common signs of a fake card. Mention the font quality, HP number realism, and holographic pattern style.
        """

        if st.button("🔍 Scan Card Now"):
            with st.spinner("Consulting the Professor... (This may take a few seconds)"):
                try:
                    # Add a small delay to be gentle on the free-tier API
                    time.sleep(1)
                    response = model.generate_content([prompt, img])
                    st.markdown("### 📊 Scan Results")
                    st.write(response.text)
                except ResourceExhausted:
                    st.error("😅 Phew! The AI is a bit overwhelmed right now.")
                    st.warning("Please wait about a minute and try clicking 'Scan Card Now' again. The free plan has a speed limit!")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
else:
    st.info("👈 Please open the sidebar and enter your Gemini API Key to start.")
