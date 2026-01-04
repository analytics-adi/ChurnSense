import streamlit as st
import pandas as pd
import pickle

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="centered"
)

st.title("📉 Customer Churn Prediction")
st.write("Predict whether a customer is likely to churn based on service and account details.")

# --------------------------------------------------
# Load model and encoders
# --------------------------------------------------
@st.cache_resource
def load_artifacts():
    with open("customer_churn_model.pkl", "rb") as f:
        model_data = pickle.load(f)

    with open("encoders.pkl", "rb") as f:
        encoders = pickle.load(f)

    return model_data["model"], model_data["features_names"], encoders


model, feature_names, encoders = load_artifacts()

# --------------------------------------------------
# Input Form
# --------------------------------------------------
with st.form("churn_form"):
    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", encoders["gender"].classes_)
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", encoders["Partner"].classes_)
        dependents = st.selectbox("Dependents", encoders["Dependents"].classes_)
        phone_service = st.selectbox("Phone Service", encoders["PhoneService"].classes_)
        multiple_lines = st.selectbox("Multiple Lines", encoders["MultipleLines"].classes_)
        internet_service = st.selectbox("Internet Service", encoders["InternetService"].classes_)

    with col2:
        online_security = st.selectbox("Online Security", encoders["OnlineSecurity"].classes_)
        online_backup = st.selectbox("Online Backup", encoders["OnlineBackup"].classes_)
        device_protection = st.selectbox("Device Protection", encoders["DeviceProtection"].classes_)
        tech_support = st.selectbox("Tech Support", encoders["TechSupport"].classes_)
        streaming_tv = st.selectbox("Streaming TV", encoders["StreamingTV"].classes_)
        streaming_movies = st.selectbox("Streaming Movies", encoders["StreamingMovies"].classes_)
        contract = st.selectbox("Contract", encoders["Contract"].classes_)

    col3, col4 = st.columns(2)

    with col3:
        paperless_billing = st.selectbox("Paperless Billing", encoders["PaperlessBilling"].classes_)
        payment_method = st.selectbox("Payment Method", encoders["PaymentMethod"].classes_)

    with col4:
        tenure = st.number_input("Tenure (months)", 0, 100, 12)
        monthly_charges = st.number_input("Monthly Charges", 0.0, value=70.0)
        total_charges = st.number_input("Total Charges", 0.0, value=800.0)

    submit = st.form_submit_button("Predict Churn")


# --------------------------------------------------
# Prediction
# --------------------------------------------------
if submit:
    input_data = {
    "gender": encoders["gender"].transform([gender])[0],
    "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
    "Partner": encoders["Partner"].transform([partner])[0],
    "Dependents": encoders["Dependents"].transform([dependents])[0],
    "PhoneService": encoders["PhoneService"].transform([phone_service])[0],
    "MultipleLines": encoders["MultipleLines"].transform([multiple_lines])[0],
    "InternetService": encoders["InternetService"].transform([internet_service])[0],
    "OnlineSecurity": encoders["OnlineSecurity"].transform([online_security])[0],
    "OnlineBackup": encoders["OnlineBackup"].transform([online_backup])[0],
    "DeviceProtection": encoders["DeviceProtection"].transform([device_protection])[0],
    "TechSupport": encoders["TechSupport"].transform([tech_support])[0],
    "StreamingTV": encoders["StreamingTV"].transform([streaming_tv])[0],
    "StreamingMovies": encoders["StreamingMovies"].transform([streaming_movies])[0],
    "Contract": encoders["Contract"].transform([contract])[0],
    "PaperlessBilling": encoders["PaperlessBilling"].transform([paperless_billing])[0],
    "PaymentMethod": encoders["PaymentMethod"].transform([payment_method])[0],
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges
}

    df_input = pd.DataFrame([input_data])[feature_names]

    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ Customer is likely to churn (Risk: {probability:.2%})")
    else:
        st.success(f"✅ Customer is unlikely to churn (Risk: {probability:.2%})")
