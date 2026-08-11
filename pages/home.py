import streamlit as st
from styles import apply_company_styles

apply_company_styles()

st.set_page_config(
    page_title="IncomeProt LTD",
    layout="wide"
)



st.html(
    """
    <div class="company-hero">
        <div style="font-size:0.85rem; font-weight:700;
                    letter-spacing:0.1rem;">
            INCOMEPROT LTD
        </div>

        <h1 style="margin-bottom:0.4rem;">
            AI-Powered Income Classification
        </h1>

        <p style="font-size:1.1rem; max-width:760px;">
            Transforming census and employment information into
            clear, consistent machine-learning insights.
        </p>
    </div>
    """
)

st.markdown(
    """
    <div class="hero-description">
        IncomeProt LTD uses machine learning to estimate whether an
        individual's annual income is likely to be above or below $50,000
        based on census, education, employment and demographic information.
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "This application is an educational demonstration built using "
    "the UCI Adult Census Income dataset."
    "Images are from Pinterest all rights to the owner"
)


# Image section

image_col1, image_col2, image_col3 = st.columns(3)

with image_col1:
    st.image(
        "images/421016265180379473.jpeg",
        use_container_width=True
    )

with image_col2:
    st.image(
        "images/1032802127089533571.jpeg",
        use_container_width=True
    )

with image_col3:
    st.image(
        "images/1050464681826835136.jpeg",
        use_container_width=True
    )



st.divider()

# Company values

st.markdown("## Why IncomeProt?")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.html(
        """
        <div class="company-card">
            <h3>⚡ Fast</h3>
            <p>
                Generate income classifications in seconds using
                a trained machine-learning pipeline.
            </p>
        </div>
        """
    )

with feature_col2:
    st.html(
        """
        <div class="company-card">
            <h3>✓ Reliable</h3>
            <p>
                Every record follows the same preprocessing and
                prediction process.
            </p>
        </div>
        """
    )

with feature_col3:
    st.html(
        """
        <div class="company-card">
            <h3>🔍 Transparent</h3>
            <p>
                Review the predicted class, model probabilities
                and submitted information.
            </p>
        </div>
        """
    )


st.divider()


# How it works

st.markdown("## How It Works")

step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown("### 1. Enter Details")
    st.write(
        "Provide personal, employment, education and financial information."
    )

with step_col2:
    st.markdown("### 2. Run the Model")
    st.write(
        "The information is processed using the same pipeline used "
        "during model training."
    )

with step_col3:
    st.markdown("### 3. Review Results")
    st.write(
        "View the predicted income category and probability assigned "
        "to each class."
    )


st.divider()

# Call to action

st.markdown("## Explore the Income Prediction Tool")

st.write(
    "Enter an individual's profile information and receive a predicted "
    "income category together with the model's estimated probabilities."
)

if st.button(
    "Start a Prediction",
    type="primary",
    use_container_width=True
):
    st.switch_page("pages/prediction.py")

st.divider()

st.markdown("## Explore Batch Prediction Tool")

st.write(
    "Enter a csv with multiple records to get prediction of all records"
)

if st.button(
    "Start Batch Prediction",
    type="primary",
    use_container_width=True
):
    st.switch_page("pages/batch_prediction.py")

st.divider()


# Contact form

with st.form("contact_form"):
    st.subheader("Contact Us")

    name = st.text_input(
        "Your Name",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "Your Email",
        placeholder="name@example.com"
    )

    message = st.text_area(
        "Your Message",
        placeholder="How can we help?"
    )

    contact_submitted = st.form_submit_button(
        "Send Message",
        use_container_width=True
    )

    if contact_submitted:
        if not name.strip():
            st.error("Please enter your name.")

        elif not email.strip():
            st.error("Please enter your email address.")

        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")

        elif not message.strip():
            st.error("Please enter a message.")

        else:
            st.success(
                f"Thanks, {name}. Your message has been received."
            )


# Disclaimer

st.divider()

st.markdown(
    """
    <div class="disclaimer">
        <strong>Educational disclaimer:</strong> This application is designed
        for teaching and demonstration purposes. Predictions are based on
        historical census patterns and should not be used for employment,
        lending, insurance or eligibility decisions.
    </div>
    """,
    unsafe_allow_html=True
)

