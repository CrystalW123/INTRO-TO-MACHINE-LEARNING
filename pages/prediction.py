import streamlit as st
import joblib
import pandas as pd
from styles import apply_company_styles

apply_company_styles()

st.set_page_config(
    page_title="Income Prediction",
    layout="wide"
)


# Load model

@st.cache_resource
def load_model():
    return joblib.load("adult_income_pipeline.joblib")


model = load_model()

# Input options

marital_status_options = [
    "Married-civ-spouse",
    "Never-married",
    "Divorced",
    "Separated",
    "Widowed",
    "Married-spouse-absent",
    "Married-AF-spouse"
]

race_options = [
    "White",
    "Black",
    "Asian-Pac-Islander",
    "Amer-Indian-Eskimo",
    "Other"
]

relationship_options = [
    "Husband",
    "Not-in-family",
    "Own-child",
    "Unmarried",
    "Wife",
    "Other-relative"
]

country_options = [
    "United-States",
    "Mexico",
    "Philippines",
    "Germany",
    "Canada",
    "Puerto-Rico",
    "El-Salvador",
    "India",
    "Cuba",
    "England",
    "Jamaica",
    "South",
    "China",
    "Italy",
    "Dominican-Republic",
    "Vietnam",
    "Guatemala",
    "Japan",
    "Poland",
    "Columbia",
    "Taiwan",
    "Haiti",
    "Iran",
    "Portugal",
    "Nicaragua",
    "Peru",
    "France",
    "Greece",
    "Ecuador",
    "Ireland",
    "Hong",
    "Cambodia",
    "Trinadad&Tobago",
    "Thailand",
    "Laos",
    "Yugoslavia",
    "Outlying-US(Guam-USVI-etc)",
    "Honduras",
    "Hungary",
    "Scotland",
    "Holand-Netherlands"
]

workclass_options = [
    "Private",
    "Self-emp-not-inc",
    "Local-gov",
    "State-gov",
    "Self-emp-inc",
    "Federal-gov",
    "Without-pay",
    "Never-worked"
]

occupation_options = [
    "Prof-specialty",
    "Craft-repair",
    "Exec-managerial",
    "Adm-clerical",
    "Sales",
    "Other-service",
    "Machine-op-inspct",
    "Transport-moving",
    "Handlers-cleaners",
    "Farming-fishing",
    "Tech-support",
    "Protective-serv",
    "Priv-house-serv",
    "Armed-Forces"
]

education_mapping = {
    "Preschool": 1,
    "1st-4th": 2,
    "5th-6th": 3,
    "7th-8th": 4,
    "9th": 5,
    "10th": 6,
    "11th": 7,
    "12th": 8,
    "HS-grad": 9,
    "Some-college": 10,
    "Assoc-voc": 11,
    "Assoc-acdm": 12,
    "Bachelors": 13,
    "Masters": 14,
    "Prof-school": 15,
    "Doctorate": 16
}


# Page heading

st.title("Income Prediction Portal")

st.caption(
    "Enter an individual's census and employment information "
    "to estimate their annual income category."
)

# Prediction form

with st.form("prediction_form"):

    st.subheader("Personal Profile")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=17,
            max_value=100,
            value=35,
            step=1
        )

        sex = st.selectbox(
            "Sex",
            ["Female", "Male"]
        )

        marital_status = st.selectbox(
            "Marital status",
            marital_status_options
        )

    with col2:
        race = st.selectbox(
            "Race",
            race_options
        )

        relationship = st.selectbox(
            "Relationship",
            relationship_options
        )

        native_country = st.selectbox(
            "Native country",
            country_options
        )

    st.divider()

    st.subheader("Employment and Education")

    col3, col4 = st.columns(2)

    with col3:
        workclass = st.selectbox(
            "Work class",
            workclass_options
        )

        occupation = st.selectbox(
            "Occupation",
            occupation_options
        )

        hours_per_week = st.slider(
            "Hours worked per week",
            min_value=1,
            max_value=100,
            value=40
        )

    with col4:
        education = st.selectbox(
            "Education",
            list(education_mapping.keys())
        )

        education_num = education_mapping[education]

        st.text_input(
            "Education level number",
            value=str(education_num),
            disabled=True
        )

        capital_gain = st.number_input(
            "Capital gain",
            min_value=0,
            value=0,
            step=100
        )

        capital_loss = st.number_input(
            "Capital loss",
            min_value=0,
            value=0,
            step=100
        )

    with st.expander("Advanced fields"):
        fnlwgt = st.number_input(
            "Census population weight",
            min_value=1,
            value=100000,
            step=1000,
            help=(
                "This is the census sampling weight. "
                "It is not the person's salary or net worth."
            )
        )

    submitted = st.form_submit_button(
        "Generate Prediction",
        type="primary",
        use_container_width=True
    )


# Prediction

if submitted:

    input_data = pd.DataFrame({
        "age": [age],
        "workclass": [workclass],
        "fnlwgt": [fnlwgt],
        "education": [education],
        "education-num": [education_num],
        "marital-status": [marital_status],
        "occupation": [occupation],
        "relationship": [relationship],
        "race": [race],
        "sex": [sex],
        "capital-gain": [capital_gain],
        "capital-loss": [capital_loss],
        "hours-per-week": [hours_per_week],
        "native-country": [native_country]
    })

    try:
        prediction = model.predict(input_data)[0]

        class_probabilities = model.predict_proba(
            input_data
        )[0]

        probability_by_class = dict(
            zip(
                model.classes_,
                class_probabilities
            )
        )

        st.divider()
        st.subheader("Prediction Result")

        if prediction == 1:
            st.success(
                "Predicted income category: Above $50,000"
            )
        else:
            st.info(
                "Predicted income category: $50,000 or below"
            )

        probability_above = probability_by_class[1]
        probability_below = probability_by_class[0]

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                "Probability of income ≤ $50K",
                f"{probability_below:.1%}"
            )

        with result_col2:
            st.metric(
                "Probability of income > $50K",
                f"{probability_above:.1%}"
            )

        st.progress(float(probability_above))

        st.caption(
            "The displayed probability is the model's estimate, "
            "not a guaranteed income outcome."
        )

        with st.expander("View submitted information"):
            submitted_data = input_data.T.rename(
                columns={0: "Submitted value"}
            )

            st.dataframe(
                submitted_data,
                use_container_width=True
            )

    except Exception as error:
        st.error(
            "Prediction could not be generated."
        )

        st.exception(error)
