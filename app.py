import json
from pathlib import Path
import streamlit as st
import yaml

from narrative_generation import generate

EXAMPLE_PATH = Path("examples")
examples = [
    dir for dir in EXAMPLE_PATH.iterdir() if dir.is_dir()
]

selected_example = st.selectbox("Select an example", examples, format_func=lambda x: x.name)
if selected_example is None:
    st.stop()

questionnaire_path = selected_example / "Questionnaire.json"

template_path = selected_example / "template.yaml"
template = yaml.safe_load(template_path.read_text())

with st.expander("Questionnaire"):
    st.code(questionnaire_path.read_text())

st.markdown("### Narrative Template")
st.markdown("__variables__")
st.table(template["variable"])
st.markdown("__template__")
st.code(template["textNarrative"])

questionnaire_response_paths = selected_example.glob("*-QuestionnaireResponse.json")

selected_response_path = st.selectbox("Select a response", questionnaire_response_paths, format_func=lambda x: x.name.replace("-QuestionnaireResponse.json", ""))

if selected_response_path is None:
    st.stop()

template_path = selected_example / "template.yaml"
template = yaml.safe_load(template_path.read_text())
questionnaire = json.loads(questionnaire_path.read_text())
questionnaire_response = json.loads(selected_response_path.read_text())
question_item = questionnaire["item"][0]
response_item = questionnaire_response["item"][0] if questionnaire_response["item"] else {}
generated_text = generate(template, question_item=question_item, response_item=response_item)
with st.expander("Questionnaire Response"):
    st.code(selected_response_path.read_text())
st.markdown("### Generated Narrative")
st.html(f"""
        <pre>
            {generated_text}
        </pre>
        """)
