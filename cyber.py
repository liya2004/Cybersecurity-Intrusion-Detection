import streamlit as st
import pandas as pd
import pickle
import base64
import os
import sklearn
from sklearn.ensemble import RandomForestClassifier
def add_bg_from_local(image_file):
    script_dir = os.path.dirname(__file__)
    img_path = os.path.join(script_dir, image_file)
    with open(img_path, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("cyber_img.jpg")
model=pickle.load(open('cybersecurity_model.pkl','rb'))
scaler=pickle.load(open('cybersecurity_scaler.pkl','rb'))
st.sidebar.title("🔐 Cybersecurity Intrusion Detection")
page=st.sidebar.radio("Go to", ["🏠 Introduction", "🧩 Input Data", "📊 Output"])
if page=="🏠 Introduction":
    st.title("Cybersecurity Intrusion Detection System")
    st.markdown("""
    ### 🔍 Project Overview  
    This ML system identifies whether a network activity indicates:  
    - **Normal behavior**, or  
    - **Suspicious Attack**  
    #### 📘 Objective:
    - Analyze network parameters  
    - Predict intrusion using a Random Forest model  
    - Provide a user-friendly Streamlit interface  
    """)
elif page=="🧩 Input Data":
    st.title("Enter Network Parameters")
    col1,col2,col3=st.columns(3)
    with col1:
        network_packet_size=st.text_input("Network Packet Size (0-100000)")
        protocol_type=st.selectbox("Protocol Type", ["","TCP", "UDP", "ICMP"])
        login_attempts = st.text_input("Login Attempts (0 - 50)")
    with col2:
        session_duration=st.text_input("Session Duration (sec)")
        encryption_used=st.selectbox("Encryption Used", ["", "AES", "DES", "None"])
        ip_reputation_score=st.text_input("IP Reputation Score (0 - 10)")
    with col3:
        failed_logins=st.text_input("Failed Logins (0 - 50)")
        browser_type=st.selectbox("Browser Type",["", "Chrome", "Firefox", "Edge", "Safari", "Other"])
        unusual_time_access=st.selectbox("Unusual Time Access", ["", "Yes", "No"])
    if st.button("🔎 Predict Intrusion"):
        if (not network_packet_size or not login_attempts or not session_duration or
            not ip_reputation_score or not failed_logins or
            protocol_type == "" or encryption_used == "" or
            browser_type == "" or unusual_time_access == ""):
            st.warning("⚠️ Please fill all fields before predicting.")
            st.stop()
        try:
            network_packet_size = float(network_packet_size)
            login_attempts = int(login_attempts)
            session_duration = float(session_duration)
            ip_reputation_score = float(ip_reputation_score)
            failed_logins = int(failed_logins)
        except:
            st.error("❌ Invalid input! Please enter correct numeric values.")
            st.stop()
        input_data=pd.DataFrame({
            'network_packet_size':[network_packet_size],
            'protocol_type':[protocol_type],
            'login_attempts':[login_attempts],
            'session_duration':[session_duration],
            'encryption_used':[encryption_used],
            'ip_reputation_score':[ip_reputation_score],
            'failed_logins':[failed_logins],
            'browser_type':[browser_type],
            'unusual_time_access':[unusual_time_access]
        })
        st.write("### Entered Data")
        st.write(input_data)
        input_encoded=pd.get_dummies(input_data)
        input_encoded=input_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
        input_scaled=scaler.transform(input_encoded)
        prediction=model.predict(input_scaled)[0]
        st.session_state["prediction_result"]=prediction
        st.success("Prediction completed! Go to the Output page to view result.")
elif page=="📊 Output":
    st.title("Prediction Result")

    if "prediction_result" in st.session_state:
        result=st.session_state["prediction_result"]
        if result==1 or str(result).lower() in ["attack", "yes"]:
            st.error("🚨 Intrusion Detected! Suspicious activity found.")
            st.markdown("""
                <style>
                .blink {
                    animation: blinker 1s linear infinite;
                    color: red;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                }
                @keyframes blinker {
                    50% { opacity: 0; }
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<p class="blink">⚠️ WARNING: HIGH RISK INTRUSION DETECTED</p>', unsafe_allow_html=True)

        else:
            st.success("✅ Normal Behavior Detected. No intrusion found.")

    else:
        st.warning("Please run a prediction first from the Input Data page.")




