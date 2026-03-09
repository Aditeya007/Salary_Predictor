import streamlit as st
import pickle
import numpy as np
st.set_page_config(
    page_title="Dev Salary Predictor",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="expanded"
)
@st.cache_resource
def load_model():
    with open('saved_steps2.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

try:
    data = load_model()
    regressor = data["model"]
    scaler = data["scaler"]
    le_country = data["le_country"]
    le_dev = data["le_dev"]
except FileNotFoundError:
    st.error("❌ Model file not found. Please ensure 'saved_steps.pkl' exists in the same folder.")
    st.stop()


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055687.png", width=80)
    st.title("About")
    st.info(
        "This app predicts the **annual salary** of a software developer "
        "based on country, education level, role, and years of experience.\n\n"
        "📊 Data sourced from the **Stack Overflow Developer Survey**."
    )
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit & Scikit-learn")


st.markdown("<h1 style='text-align:center;'>💻 Software Developer Salary Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Predict your expected salary based on your profile</p>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("📋 Enter Your Details")
education_levels = (
    "Less than a Bachelors",
    "Bachelor’s degree",
    "Master’s degree",
    "Post grad",
)

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox(
        "🌍 Country",
        options=le_country.classes_,
        help="Select the country where you work or plan to work."
    )

    education = st.selectbox(
        "🎓 Education Level",
        options=education_levels,
        help="Select your highest education level."
    )

with col2:
    dev_type = st.selectbox(
        "💻 Developer Type",
        options=le_dev.classes_,
        help="Select your primary developer role."
    )

    experience = st.slider(
        "🧑‍💼 Years of Experience",
        min_value=0,
        max_value=50,
        value=3,
        step=1,
        help="Drag to select your years of professional experience."
    )
    st.markdown("")
    st.metric(label="Experience Selected", value=f"{experience} years")

st.markdown("---")


def predict_salary(country, education, experience, dev_type):
    
    ed_mapping = {
        "Less than a Bachelors": 0,
        "Bachelor’s degree": 1,
        "Master’s degree": 2,
        "Post grad": 3
    }
    ed_num = ed_mapping[education]
    country_num = le_country.transform([country])[0]
    dev_num = le_dev.transform([dev_type])[0]
    X = np.array([[country_num, ed_num, experience, dev_num]])
    X_scaled = scaler.transform(X)
    salary = regressor.predict(X_scaled)
    return salary[0]
if st.button("🔮 Predict My Salary", use_container_width=True, type="primary"):
    with st.spinner("Consulting the Random Forest algorithm..."):
        try:
            result = predict_salary(country, education, experience, dev_type)

            st.success("✅ Prediction Complete!")
            
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("🌍 Country", country)
            with col_b:
                st.metric("💻 Role", dev_type[:15] + "..." if len(dev_type) > 15 else dev_type)
            with col_c:
                st.metric("🧑‍💼 Experience", f"{experience} yrs")

            
            st.markdown("")
            st.markdown(
                f"<div style='text-align:center; padding:25px; background-color:#1e3a5f;"
                f"border-radius:14px; margin-top:10px; border: 1px solid #4fc3f7;'>"
                f"<h2 style='color:#4fc3f7; margin-bottom: 5px;'>💰 Estimated Annual Salary</h2>"
                f"<h1 style='color:white; font-size:3.5em; margin-top: 0px;'>${result:,.2f}</h1>"
                f"<p style='color:#90caf9; font-size: 0.9em;'>Based on Stack Overflow Developer Survey data</p>"
                f"</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")


st.markdown("---")
st.caption("⚠️ This is an estimate based on survey data and may not reflect actual salaries. Predictions are subject to market conditions and individual negotiation skills.")