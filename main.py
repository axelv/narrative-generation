from liquid import DictLoader, Environment
from fhirpathpy import evaluate
from fhirpathpy.models import models
from grammar_fix import FixGrammar

example_patient = {
    "resourceType": "Patient",
    "id": "example",
    "gender": "male",
    "birthDate": "1974-12-25",
    "name": [
        {
            "use": "official",
            "text": "Jan Jansen",
        }
    ]
}


single_answer_snippet = """
{%- assign question = qitem | fhirpath: "%qitem.text" -%}
{%- assign answer = item | fhirpath: "%context.answer.value" -%}
{{question}}: {{answer}}
"""

multi_answer_snippet = """
{%- assign question = qitem | fhirpath: "%qitem.text" -%}
{%- assign answers = item | fhirpath: "%context.answer.value" -%}
{{question}}: {{answers | join: ", "}}
"""

sympton_snippet = """
{%- assign symptoms = item | fhirpath: "%context.answer.value" -%}
{%- fix grammar -%}
We stelden volgende symtomen bij hem/haar vast: {{symptoms | join: ", "}}.
{% endfix -%}
"""

single_decimal_answer_snippet = """
{%- assign question = qitem | fhirpath: "%qitem.text" -%}
{%- assign answer = item | fhirpath: "%context.answer.value" -%}
{%- assign unit = qitem | fhirpath: "%qitem.unit.display" -%}
{{question}}: {{answer}} {{unit}}
"""

diagnosis_snippet = """
{%- assign diagnosis = item | fhirpath: "%context.answer.value" -%}
{%- assign severity = item | fhirpath: "%context.answer.item.where(linkId='3.1').answer.value" -%}
{%- assign date = item | fhirpath: "%context.answer.item.where(linkId='3.2').answer.value" -%}
{%- fix grammar -%}
Deze symptomen zijn een sterke indicatie voor {{severity}} {{diagnosis}} vastgesteld op {{date}}.
{% endfix -%}
"""

def execute_fhirpath(resource, expression, **kwargs):
    return evaluate(resource, {"expression": expression, "base": "QuestionnaireResponse.item"}, kwargs, model=models["r5"])

example_q = {
    "item": [
        {
            "type": "string",
            "linkId": "1",
            "text": "Symptomen",
            "repeats": True,
        },
        {
            "type": "decimal",
            "linkId": "2",
            "text": "Temperatuur",
            "unit": {
                "system": "http://unitsofmeasure.org",
                "code": "Cel",
                "display": "°C"
            }
        },
        {
            "type": "string",
            "linkId": "3",
            "text": "Diagnose",
            "item": [
                {
                    "type": "string",
                    "linkId": "3.1",
                    "text": "Ernst",
                },
                {
                    "type": "date",
                    "linkId": "3.2",
                    "text": "Datum",
                }
            ]
        },
        {
            "type": "string",
            "linkId": "4",
            "text": "Voorgestelde behandeling",
            "repeats": True,
        }
    ]
}

def iterate_items(items):
    for item in items:
        yield item
        if "item" in item:
            yield from iterate_items(item["item"])

def get_item(link_id:str):
    return next((item for item in iterate_items(example_q["item"]) if item["linkId"] == link_id), None)


example_qr = {
    "item": [
        {
            "linkId": "1",
            "text": "Symptomen",
            "answer": [
                {
                    "valueString": "koorts"
                },
                {
                    "valueString": "hoofdpijn"
                },
                {
                    "valueString": "vermoeidheid"
                }
            ]
        },
        {
            "linkId": "2",
            "text": "Temperatuur",
            "answer": [
                {
                    "valueDecimal": 38.5
                }
            ]
        },
        {
            "linkId": "3",
            "text": "Diagnose",
            "answer": [
                {
                    "valueString": "COVID-19",
                    "item": [
                        {
                            "linkId": "3.1",
                            "text": "Ernst",
                            "answer": [
                                {
                                    "valueString": "Mild"
                                }
                            ]
                        },
                        {
                            "linkId": "3.2",
                            "text": "Datum",
                            "answer": [
                                {
                                    "valueDate": "2021-09-01"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "linkId": "4",
            "text": "Voorgestelde behandeling",
            "answer": [
                {
                    "valueString": "Paracetamol"
                },
                {
                    "valueString": "Ibuprofen"
                },
                {
                    "valueString": "Hydroxychloroquine"
                }
            ]
        }
    ]
}

liquid_template = """
{%- assign qitem = "1" | load_qitem %}
{%- render "1" item: resource.item[0], qitem: qitem %}
{%- assign qitem = "2" | load_qitem %}
{%- render "2" item: resource.item[1], qitem: qitem %}
{%- assign qitem = "3" | load_qitem %}
{%- render "3" item: resource.item[2], qitem: qitem %}
{%- assign qitem = "4" | load_qitem %}
{%- render "4" item: resource.item[3], qitem: qitem %}
"""

def main():
    env = Environment(loader=DictLoader({"1": sympton_snippet, "2": single_decimal_answer_snippet, "3":diagnosis_snippet, "4": multi_answer_snippet}))
    env.add_filter("fhirpath", execute_fhirpath)
    env.add_filter("load_qitem", get_item)
    env.add_tag(FixGrammar)
    template = env.from_string(liquid_template)
    print(template.render(resource=example_qr))

if __name__ == "__main__":
    main()
