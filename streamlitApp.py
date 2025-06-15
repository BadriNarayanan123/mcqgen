import os
import json
import traceback
import pandas as pd
import streamlit as st
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

Response = {
    "1": {
        "Question": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "Answer": "correct answer",
    },
    "2": {
        "Question": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "Answer": "correct answer",
    },
    "3": {
        "Question": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "Answer": "correct answer",
    },
}

st.set_page_config(page_title="MCQ Generator", layout="wide")
st.title("📘 MCQ Quiz Generator and Evaluator")

uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
number = st.number_input("Number of MCQs", min_value=1, max_value=50, value=5)
subject = st.text_input("Subject", value="Data Structures and Algorithms")
tone = st.selectbox("Tone", ["Simple","Medium","Hard"], index=0)

    
if uploaded_file and st.button("Generate Quiz"):
    try:
        text = read_file(uploaded_file)
        with st.spinner("Generating quiz and evaluation..."):
            result = generate_evaluate_chain({
                "text": text,
                "number": number,
                "subject": subject,
                "tone": tone,
                "response_json": json.dumps(Response)
            })
        print(result["review"])
        st.subheader("📝 Generated Quiz")
        try:
            quiz_data = get_table_data(json.loads(result["quiz"]))
            df = pd.DataFrame(quiz_data)
            print(df)
            st.table(df)
        except Exception as e:
            st.error("Failed to parse quiz JSON. Raw output below:")
            st.text(result["quiz"])

        st.subheader("🔍 Quiz Review")
        st.write(result["review"])

    except Exception as e:
        st.error("Something went wrong: " + str(e))
        st.text(traceback.format_exc())
