import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Hack4Good", layout="wide")

st.title("GIZ Policy II")
st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)

feature = st.sidebar.selectbox("Feature", ["Exploration", "Q&A"])

if feature == "Q&A":
    query = st.text_input("Enter a query:")
    k = st.slider("Number of Results:", 1, 10, value=5)
    if query:
        results = [
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."
        ]
        summary = {}
        for i in range(k):
            summary["Result " + str(i + 1)] = results
        st.json(json.dumps(summary))
