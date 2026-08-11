import io
import joblib
import pandas as pd
import streamlit as st

from styles import apply_company_styles

apply_company_styles()


st.set_page_config(
    page_title="Batch Income Prediction",
    layout="wide"
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("adult_income_pipeline.joblib")


model = load_model()


# Required model columns

required_columns = [
    "age",
    "workclass",
    "fnlwgt",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country"
]


# Page heading

st.title("Batch Income Prediction")

st.caption(
    "Upload a CSV containing multiple records to generate "
    "income predictions for all rows."
)

st.info(
    "The uploaded file must contain all required model columns. "
    "Additional columns, such as customer_id or record_id, may be included "
    "and will remain in the downloaded results."
)


# Expected file format

with st.expander("View required CSV columns"):
    required_columns_df = pd.DataFrame({
        "Required column": required_columns
    })

    st.dataframe(
        required_columns_df,
        use_container_width=True,
        hide_index=True
    )


# Example template

example_data = pd.DataFrame({
    "age": [35, 48],
    "workclass": ["Private", "Self-emp-not-inc"],
    "fnlwgt": [100000, 150000],
    "education-num": [13, 9],
    "marital-status": [
        "Never-married",
        "Married-civ-spouse"
    ],
    "occupation": [
        "Prof-specialty",
        "Craft-repair"
    ],
    "relationship": [
        "Not-in-family",
        "Husband"
    ],
    "race": ["White", "Black"],
    "sex": ["Female", "Male"],
    "capital-gain": [0, 0],
    "capital-loss": [0, 0],
    "hours-per-week": [40, 50],
    "native-country": [
        "United-States",
        "United-States"
    ]
})

example_csv = example_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Template",
    data=example_csv,
    file_name="income_prediction_template.csv",
    mime="text/csv",
    use_container_width=True
)


st.divider()


# Upload CSV

uploaded_file = st.file_uploader(
    "Upload customer CSV",
    type=["csv"],
    help="Upload a comma-separated CSV file containing the required columns."
)


if uploaded_file is not None:

    try:
        uploaded_df = pd.read_csv(uploaded_file)

    except Exception as error:
        st.error("The uploaded CSV could not be read.")
        st.exception(error)
        st.stop()

    if uploaded_df.empty:
        st.warning("The uploaded file contains no records.")
        st.stop()

    st.success(
        f"File uploaded successfully: "
        f"{len(uploaded_df):,} records detected."
    )


    # Show uploaded data

    st.subheader("Uploaded Data Preview")

    st.dataframe(
        uploaded_df.head(20),
        use_container_width=True
    )

    # Validate columns

    missing_columns = [
        column
        for column in required_columns
        if column not in uploaded_df.columns
    ]

    extra_columns = [
        column
        for column in uploaded_df.columns
        if column not in required_columns
    ]


    if missing_columns:
        st.error(
            "The uploaded file is missing required columns."
        )

        st.write("Missing columns:")

        for column in missing_columns:
            st.write(f"- `{column}`")

        st.stop()


    st.success("All required model columns are present.")


    if extra_columns:
        st.info(
            "The following additional columns will not be passed to the "
            "model, but they will remain in the output file:"
        )

        st.write(", ".join(extra_columns))


    # Prepare model input

    model_input = uploaded_df[required_columns].copy()


    # Basic missing-value check

    missing_value_counts = (
        model_input
        .isna()
        .sum()
        .sort_values(ascending=False)
    )

    columns_with_missing_values = (
        missing_value_counts[
            missing_value_counts > 0
        ]
    )


    if not columns_with_missing_values.empty:
        st.warning(
            "Some required fields contain missing values. "
            "This needs to be filled as preprocessing does not cover for it"
        )

        missing_summary = (
            columns_with_missing_values
            .rename("Missing values")
            .reset_index()
            .rename(columns={"index": "Column"})
        )

        st.dataframe(
            missing_summary,
            use_container_width=True,
            hide_index=True
        )

    # Run prediction

    if st.button(
        "Generate Batch Predictions",
        type="primary",
        use_container_width=True
    ):

        try:
            with st.spinner("Generating predictions..."):

                predictions = model.predict(model_input)

                probability_matrix = model.predict_proba(
                    model_input
                )

                class_labels = list(model.classes_)

                probability_df = pd.DataFrame(
                    probability_matrix,
                    columns=class_labels,
                    index=uploaded_df.index
                )


                # Confirm expected target classes
                if 0 not in class_labels or 1 not in class_labels:
                    st.error(
                        "The model does not use the expected class labels "
                        "0 and 1."
                    )

                    st.write(
                        "Classes found in the model:",
                        class_labels
                    )

                    st.stop()


                results_df = uploaded_df.copy()

                results_df["predicted_class"] = predictions

                results_df["predicted_income"] = (
                    pd.Series(
                        predictions,
                        index=results_df.index
                    )
                    .map({
                        0: "$50K or below",
                        1: "Above $50K"
                    })
                )

                results_df["probability_below_50k"] = (
                    probability_df[0]
                )

                results_df["probability_above_50k"] = (
                    probability_df[1]
                )


            # Prediction summary

            st.divider()
            st.subheader("Batch Prediction Summary")

            total_records = len(results_df)

            below_count = (
                results_df["predicted_class"] == 0
            ).sum()

            above_count = (
                results_df["predicted_class"] == 1
            ).sum()

            above_rate = above_count / total_records


            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                st.metric(
                    "Total Records",
                    f"{total_records:,}"
                )

            with summary_col2:
                st.metric(
                    "Predicted Above $50K",
                    f"{above_count:,}",
                    f"{above_rate:.1%} of records"
                )

            with summary_col3:
                st.metric(
                    "Predicted $50K or Below",
                    f"{below_count:,}",
                    f"{1 - above_rate:.1%} of records"
                )

            # Prediction distribution

            st.subheader("Prediction Distribution")

            prediction_summary = (
                results_df["predicted_income"]
                .value_counts()
                .rename_axis("Income category")
                .reset_index(name="Number of records")
            )

            st.bar_chart(
                prediction_summary,
                x="Income category",
                y="Number of records"
            )


            # Results preview

            st.subheader("Prediction Results")

            default_result_columns = (
                extra_columns
                + [
                    "predicted_income",
                    "probability_below_50k",
                    "probability_above_50k"
                ]
            )

            # Prevent duplicate column names
            default_result_columns = list(
                dict.fromkeys(default_result_columns)
            )

            st.dataframe(
                results_df[default_result_columns].head(100),
                use_container_width=True,
                column_config={
                    "probability_below_50k": st.column_config.ProgressColumn(
                        "Probability: ≤ $50K",
                        min_value=0.0,
                        max_value=1.0,
                        format="percent"
                    ),
                    "probability_above_50k": st.column_config.ProgressColumn(
                        "Probability: > $50K",
                        min_value=0.0,
                        max_value=1.0,
                        format="percent"
                    )
                }
            )


            if len(results_df) > 100:
                st.caption(
                    "The preview shows the first 100 records. "
                    "The downloaded CSV contains all records."
                )


            # Download predictions

            results_csv = results_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download Prediction Results",
                data=results_csv,
                file_name="batch_income_predictions.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )


            st.caption(
                "Predictions are model estimates based on historical "
            )


        except Exception as error:
            st.error(
                "Batch predictions could not be generated."
            )

            st.exception(error)