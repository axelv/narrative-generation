

# Example 1.

TODO: https://github.com/Tiro-health/Cicero/blob/91aa6a4f304a797dffb5787ac2ccf304111c64b7/blocks/cardio-tavi-procedure-report-BE-nl.yaml#L607

**Questionnaire**
```yaml
- item:
    - linkdId: ""
      text: "Materiaal vebruik"
      type:

      item:
        - linkId: ""
          narrativeTemplate: ""
            Plaatsen van een {{ sheats-type }} {{sheats-maat}}
          ""
          text: "1ste"
          item:
            - linkId: "sheaths-maat"
              text: "Sheaths maat"

            - linkId: "sheats-type"
              text: "Sheaths type"

```

**QuestionnaireResponse **
```yaml
- item:
    linkId: ""
    answer: ""

```


**Variables**
```yaml


```


**Narrative Template**
```liquid


```


**Narrative Output**
```text

```


# Example 2.

TODO: https://github.com/Tiro-health/Cicero/blob/91aa6a4f304a797dffb5787ac2ccf304111c64b7/blocks/cardio-tavi-procedure-report-BE-nl.yaml#L4104

**Questionnaire**
```yaml
- item:
    - linkdId: ""
      text: "Postdilattatie"
      narrativeTemplate: "
        {% if uitgevoerd == 'Ja' %}
          {% if reden is defined %}
            Wegens {{ reden }} beslissing tot postdilatatie. Opvoeren van de {{ maat-ballon }} {{soort-ballon}} tot in de klepprothese.
          {% else %}
            De postdilatatie werd uitgevoerd.
          {% endif %}
        {% else %}
          De postdilatatie werd niet uitgevoerd.
        {% endif %}
      "
      type:
      item:
        - linkId: "uitgevoerd"
          text: "Uitgevoerd"

        - linkId: "waarom-uitgevoerd"
          text: "Waarom"

        - linkId: "soort-ballon"
          text: "Soort ballon"

        - linkId: "maat-ballon"
          text: "Maat ballon"

```

**QuestionnaireResponse **
```yaml
- item:
    linkId: ""
    answer: ""

```


**Variables**
```yaml


```


**Narrative Template**
```liquid


```


**Narrative Output**
```text

```



# Example 3


**Questionnaire**
```yaml
- item:
    - linkdId: ""
      text: "Pre dilatatie"
      narrativeTemplate: "
        {% if pre-dilatatie %}
          Opvoeren van een ({maat-ballon}) mm ({soort-ballon}) over de voerdraad tot in de aortaklepring. Onder snelle ventriculaire pacing {{rapid-pacing-freq}} /min werd de aortaklep {{aantal insuf}} maal succesvol gepredilateerd.
        {% else %}
          De pre-dilatatie werd niet uitgevoerd.
        {% endif %}
      "
      type: group
      item:
        - linkId: ""

        - linkId: "waarom-uitgevoerd"
          text: "Waarom"

        - linkId: "soort-ballon"
          text: "Soort ballon"

        - linkId: "maat-ballon"
          text: "Maat ballon"

```

**QuestionnaireResponse **
```yaml
- item:
    linkId: ""
    answer: ""

```


**Variables**
```yaml


```


**Narrative Template**
```liquid


```


**Narrative Output**
```text

```


## Example 4

https://github.com/Tiro-health/Cicero/blob/91aa6a4f304a797dffb5787ac2ccf304111c64b7/blocks/cardio-tavi-procedure-report-BE-nl.yaml#L6280

````liquid
{%- case recuperatie -%}
  {%- when 'ja' -%}
  Ontstaan van persistente {{post_procedurele_geleidingstoornis}} na {{timing}}.
  {%- when 'nee' -%}
  Onstaan van persistenet {{post_procedurele_geleidingstoornis}} na {{timing}}.
{%- endcase -%}
````



## Example 5


**QuestionnaireResponse **
```yaml

- item:
  - linkId: "lijn"
    answer:
      valueString: "1L"
  - linkId: "period-start"
    answer:
      valueDate: "2024-08-29"
  - linkId: "period-end"
    answer:
      valueDate: "2024-09-03"
  - linkId: "procedure"
    answer:
      valueString: "Radiotherapie"
- item:
  - linkId: "lijn"
    answer:
      valueString: "2L"
  - linkId: "procedure"
    answer:
      valueString: "Systeemtherapie"
- item:
  - linkId: "lijn"
    answer:
      valueString: "3L"
  - linkId: "date"
    answer:
      valueDate: "2024-09-04"
  - linkId: "procedure"
    answer:
      valueString: "Chirurgie"
  - linkId: "omschrijving"
    answer:
      valueString: "Test"
  - linkId: "specificatie"
    item:
      - linkId: "pT"
        answer:
          valueString: "1b"
      - linkId: "pN"
        answer:
          valueString: "2"
      - linkId: "pM"
        answer:
          valueString: "1b"
      - linkId: "R"
        answer:
          valueString: "2"

```text
1L - 29/08/2024-03/09/2024 - Radiotherapie -  -
2L -  - Systeemtherapie -  -
3L - 04/09/2024 - Chirurgie - Test - pT1b, pN2, pM1b, R2
```
!! Advanced case

name: row-template
```liquid
{% case procedure %}
{% when 'Radiotherapie' %}
  {{render "lijn"}} - {{render "period-start"}}{{render "period-date"}}-{{render "period-end"}} - {{render "procedure"}} - {{render "omschrijving"}} - {{render "specificatie"}}
{% when 'Systeemtherapie' %}
  {{render "lijn"}} -  - {{render "procedure"}} - {{render "omschrijving"}} - {{render "specificatie"}}
```


name: table-template
```liquid
{% item in context.item %}
  {{render "row-template"}}
{% endfor %}
```
