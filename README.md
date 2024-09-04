# Product Feature: Narrative Generation

The 'narrative' is an important deliverable for medical doctors. Despite the structured nature of our workflow they want to have full control over the 'letter' that comes out of the system.
For them it's primary way of interacting with colleagues in the hospital, general practitioners and other healthcare professionals.

## Goals of having a narrative
- communication with colleagues: the narrative is the primary way of communicating with other healthcare professionals
  - important information on the patient must be exchanged
  - doctors want to keep a good relationship with their colleagues, and especially with referring GP's
- interoperability with other systems: plain-text / html / pdf is easy to share
- future reference: the narrative is a way to document the patient's history and the doctor's thoughts


## Requirements (sorted by priority)

### Functional Requirements
- interpolation of structured data points into the narrative
 - combine multiple answers into a single sentence
 - configure join characters for answers or groups
- maximal control over the phrasing of the narrative
- automatic generation: manual editiing per patient should be minimal
- human-readable & grammatically correct: the narrative should be easy to read and understand and not give the impression that it was generated by a machine
- easy to use for the easy cases, but also flexible enough for the hard cases


### Non-Functional Requirements
- performance: the narrative generation should be fast, < 500ms
- maintainability and extensibility:
  - the DSL that is used to store the narrative templates should be easy to understand and extend with new functionality
  - keeping the template consistent with the data-model is hard, so we should try to limit the potential for such errors
  - migrating legacy template DSL's to newer DSL's is really hard since we have a JSON data model. We should try to get the DSL/data-model right from the start.
- FHIR compliance: any structured data that is used in the narrative should be derived from the FHIR QuestionnaireResponse.

## Budget & Timeline
- We need a POC version of this in the next weeks. MD's are ok with a feature complete version that lacks good UX.
- We should have a plan on how to improve the UX in the future, but it's not a hard requirement for the POC.

## Technologies that we could use

### Liquid
- Liquid is a templating language that is used in Jekyll and Shopify
- Choosing Liquid = trading flexibility over simplicity.
- Good support for both Python & Javascript
- ❓is it possible to have a good UX on top of Jinja templates
Considered: Jinja2, Handlebars, custom JSON DSL

### FHIRPath for intermediate variables
- FHIRPath = JSONPath for FHIR, it's a way to extract data from a FHIR resource
- There is a high chance that we will need to support it in someway the future for advanced features
  - pre-population of questions
  - configurable data mappings (QR -> clinical data warehouse)
  - calculated expressions (e.g. BMI, GFR)
  - advanced conditional logic on queestions and answer options
- We can use variables defined as FHIRPath expressions to extract the answers from the FHIR QuestionnaireResponse.



### LLM's to make the narrative more human-readable
[Example with GPT](https://chatgpt.com/share/e1f55e16-d113-4616-8f75-5951552884c2)
- LLM's are good at generating human-readable text
- But they are hard to control and might generate text that is not correct
- Concern of MD's: how do we make sure that the generated text is correct? Can we ensure that it only makes grammatical changes and not changes the meaning of the text?
- We could provide a UI that enables to users to request a more human-readable version of the narrative and then use the LLM to generate it. Integrating this in th UI enables us to show a diff between the generated and the original narrative.
And make sure the user can easily accept or reject the changes.

**Example:**

Variables:
```yaml
collega: "Dr. Klaasen"
naam: "Gregoir Antonissen"
geslacht: "man"
temperatuur:  null,
symptomen: ["droge hoest"]
```
Original template:
```liquid
Beste {{collega}},

{% fix grammar  %}
We zagen uw patient, {{naam}}, op de raadpleging cardiologie. Bij het klinisch onderzoek werd
{% if symptomen contains 'koorts' -%} een verhoogde temperatuur van {{ temperatuur }}°C wijzend op koorts, {% endif %}
en {{ symtomen | join: ", " | remove "koorts, " }}.
{% endfix %}
```

Output:
```diff
Beste Dr. Klaasen,

- We zagen uw patient, Gregoir Antonissen, op de raadpleging cardiologie. Bij het klinisch onderzoek werd
- en droge hoest.
+ We zagen uw patiënt, Gregoir Antonissen, op de raadpleging cardiologie. Bij het klinisch onderzoek werd droge hoest vastgesteld.
```

## Ideas

### 1. Implement the "variables" feature of FHIR Questionnaires and provide sensible defaults:

Let's say we automatically provide the following variables on each question/group:

| Variable | FHIRPath | Description |
|----------|----------|-------------|
| `gender` | `Patient.gender` | The gender of the patient |
| `question` | `%qitem.text` | The text of the question |
| `answer` | `%context.answer.value` | The answer of the question |

**Note:**
- `%qitem` is a special variable that refers to the current question item. This is common in FHIRPath implementations of Questionnaires.
- `%context` is a special variable that refers to the current context of the FHIRPath expression. Typically this is the corresponding `QuestionnaireResponse` item.

These variables can be used to create simple narratives. For example

```liquid
{{question}}: {{answer}}
```

Or even consider special cases:

```liquid
{% if "No complaints" in answer %}
The patient has no complaints.
{% else %}
The patient reports the following complaints: {{answer | join: ", "}}
{% endif %}
```
Advanced users or "implementers" can use other variables to create more advanced narratives. If we allow configuration of narrative templates on "group" level, we could even combine multiple nested answers.
For example, they could use the following variables:

| Variable | FHIRPath | Description |
|----------|----------|-------------|
| `diagnosis` | `%qitem.where(linkId = 'diagnosis-213QDDJDH').answer.value` | The diagnosis of the patient |
| `severity` | `%qitem.where(linkId = 'severity-QSDJFHQDK').answer.value` | The severity of the diagnosis |

```liquid
The patient was diagnosed with {{severity} {{diagnosis}}.
```
**Note:**
- This sentence will probably feel computer-generated because of the bad adjective usage, but it's a good starting point for the user to start editing the narrative.
- ⚠️ there is no guarantee that these variables will resolve to a value. The linkId's are hardcoded and might not be present in the QuestionnaireResponse. Is this a problem?
