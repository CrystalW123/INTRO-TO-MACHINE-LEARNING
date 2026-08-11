import streamlit as st

import streamlit as st

home = st.Page("pages/home.py", title="Home")
prediction = st.Page("pages/prediction.py", title="Prediction")
batch_prediction = st.Page("pages/batch_prediction.py", title="Batch Prediction")

pg = st.navigation([home, prediction, batch_prediction])
pg.run()
