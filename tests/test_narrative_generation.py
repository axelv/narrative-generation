import pytest
import json
import yaml
from pathlib import Path
from narrative_generation import generate


EXAMPLE_DIR = Path("examples")

examples = [
    dir for dir in EXAMPLE_DIR.iterdir() if dir.is_dir()
]

def get_expected(qr_path:Path):
    expected = qr_path.with_name(qr_path.name.replace("QuestionnaireResponse.json", "output.txt"))
    assert expected.exists(), f"Expected output file not found: {expected}"
    return expected

test_cases = [(example/"Questionnaire.json", example/"template.yaml", qr, get_expected(qr))
    for example in examples for qr in example.glob("*-QuestionnaireResponse.json")
]

@pytest.mark.parametrize("q_path, template, qr_path, expected", test_cases, ids=lambda p: p.name)
def test_example_dir(q_path:Path, template:Path, qr_path:Path, expected:Path):
    questionnaire = json.loads(q_path.read_text())
    template = yaml.safe_load(template.read_text())
    questionnaire_response = json.loads(qr_path.read_text())
    question_item = questionnaire["item"][0]
    response_item = questionnaire_response["item"][0] if questionnaire_response["item"] else {}
    result = generate(template, question_item=question_item, response_item=response_item)
    assert result == expected.read_text()
