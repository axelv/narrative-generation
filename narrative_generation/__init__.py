
from fhirpathpy import evaluate
from fhirpathpy.engine.nodes import ResourceNode
from fhirpathpy.models import models
from liquid import Template

def generate(template, question_item: dict, response_item:dict):
    context = {}
    for variable in template["variable"]:
        result = evaluate(
            response_item,
            {
                "expression": variable["expression"],
                "base": "QuestionnaireResponse.item"
            },
            {"qitem":ResourceNode.create_node(question_item, "Questionnaire.item")},
            model=models["r5"]
        )
        context[variable["name"]] = result[0] if result else None # type: ignore
    return Template(template["textNarrative"]).render(context)
