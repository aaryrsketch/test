import streamlit as st
from gemini_scan import analyze_waste_image
from db import already_scanned_today,save_scan


def scan_page():
    st.title("Daily Waste Scan")
    if st.button("Leaderboard"):
        st.switch_page("pages/leader.py")
    uploaded_file = st.file_uploader("Upload your timestamped waste photo", type=["jpg", "jpeg", "png"])
    logout=st.button("logout")
    if logout:
        st.session_state.user = None
        st.session_state.session = None
        st.switch_page("main.py")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded image", use_container_width=True)
        
        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                result = analyze_waste_image(uploaded_file)
            
            if result["valid"]:
                user_id = st.session_state.user.id
                if already_scanned_today(user_id):
                    st.warning("Already scanned today. Come back tomorrow!")
                else:
                    save_scan(user_id, result["categories"], 100)
                    st.badge("Scan verified! +100 XP")
                    st.write("Waste categories detected:", ", ".join(result["categories"]))
                    
            else:
                st.error(f"Scan rejected: {result['reason']}")
scan_page()