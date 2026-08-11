# IncomeProt LTD

IncomeProt LTD is a Streamlit-based machine learning application that demonstrates how a classification model can be presented as a simple company-style product.

The application uses the UCI Adult Census Income dataset to predict whether an individual's annual income is likely to be:

* **$50,000 or below**
* **Above $50,000**

This project was created as an educational machine learning demonstration for students, showing the journey from exploratory data analysis and model development to deployment through an interactive application.

---

## Project Overview

The project demonstrates an end-to-end machine learning workflow including:

* Exploratory data analysis
* Numerical and categorical feature analysis
* Data preprocessing
* Handling class imbalance
* Binary classification
* Model evaluation
* Model persistence
* Single-record predictions
* Batch predictions
* Streamlit deployment

The final application is designed to resemble a lightweight internal company prediction platform.

---

## Machine Learning Model

The prediction model is built using an `imblearn` pipeline containing:

1. A preprocessing pipeline
2. SMOTE for handling class imbalance during training
3. An XGBoost classifier

The model structure is:

```python
xg2 = ImPipeline([
    ("preprocessor", preprocessor),
    ("smote", SMOTE(random_state=42)),
    (
        "classifier",
        XGBClassifier(
            learning_rate=0.2,
            max_depth=6,
            min_child_weight=1,
            n_estimators=100,
            subsample=0.7
        )
    )
])
```

The complete fitted pipeline is saved as:

```text
adult_income_pipeline.joblib
```

Saving the full pipeline ensures that the same preprocessing used during training is automatically applied when generating predictions.

---

## Prediction Target

The application performs binary classification.

The target represents annual income:

```text
0 = Income <= $50K
1 = Income > $50K
```

Although the target is encoded numerically, it represents two categorical classes.

---

## Input Features

The model uses the following features:

* Age
* Work class
* Final weight (`fnlwgt`)
* Education number
* Marital status
* Occupation
* Relationship
* Race
* Sex
* Capital gain
* Capital loss
* Hours worked per week
* Native country

The Streamlit interface collects these values from users before sending them to the saved machine learning pipeline.

---

## Application Features

### Home Page

The homepage introduces IncomeProt LTD and provides an overview of the prediction service.

It includes:

* Company-style branding
* Information about the application
* Navigation to prediction services
* Product features
* Educational disclaimer

### Single Prediction

The Single Prediction page allows a user to enter information for one individual.

The application then:

1. Collects the submitted information
2. Creates a one-row pandas DataFrame
3. Sends the record through the saved machine learning pipeline
4. Generates an income prediction
5. Calculates class probabilities
6. Displays the prediction and probability scores

Example output:

```text
Predicted Income Category: Above $50,000

Probability of income <= $50K: 22%
Probability of income > $50K: 78%
```

### Batch Prediction

The Batch Prediction page allows users to upload a CSV containing multiple records.

The application:

1. Reads the uploaded CSV
2. Validates the required model columns
3. Retains additional identifier columns
4. Runs predictions for all records
5. Adds predicted classes and probabilities
6. Displays a summary of the results
7. Allows users to download the completed prediction file

Additional columns such as `customer_id` may be included in the uploaded file and will remain in the output.

---

## Project Structure

```text
IncomeProt/
│
├── app.py
├── adult_income_pipeline.joblib
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── images/
│   ├── image1.jpeg
│   ├── image2.jpeg
│   └── image3.jpeg
│
└── pages/
    ├── home.py
    ├── prediction.py
    └── batch_prediction.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project directory:

```bash
cd YOUR_REPOSITORY
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the application can be opened in a browser.

---

## Dependencies

The project uses:

* Streamlit
* pandas
* NumPy
* scikit-learn
* imbalanced-learn
* XGBoost
* joblib

Exact package versions are provided in `requirements.txt`.

---

## Dataset

The project uses the UCI Adult Census Income dataset.

The dataset contains demographic, employment, education and financial characteristics collected from US census information.

The machine learning task is to classify whether an individual's annual income exceeds $50,000.

---

## Educational Purpose

This project is intended to demonstrate how a machine learning model can move beyond a notebook and become an interactive application.

Students can use the project to understand:

* How raw user information becomes model input
* Why preprocessing must remain consistent between training and prediction
* How machine learning pipelines simplify deployment
* How prediction probabilities differ from guaranteed outcomes
* How batch scoring can be implemented in real-world systems
* How machine learning applications can be presented to non-technical users

---

## Responsible Use

The Adult Census dataset contains demographic attributes such as sex and race and reflects historical socioeconomic patterns.

Associations found by the model should not be interpreted as causal relationships.

This application is for educational and demonstration purposes only.

It should **not** be used to make real decisions related to:

* Employment
* Credit
* Lending
* Insurance
* Eligibility
* Admissions
* Access to services

Model predictions reflect patterns learned from historical data and should not be treated as guaranteed future outcomes.

---

## Author

Created as part of an introductory machine learning learning experience focused on taking students from data exploration through model deployment.
