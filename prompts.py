def sentence_extraction_prompt(title, text):
    return f"""
    You are a clinical information extractor analyzing documents for AML cancer patients.
    Your task is to identify and extract sentences providing evidence for:
    - AML Diagnosis Date
    - Precedent Disease (with date of mention)
    - Performance Status (ECOG or KPS with date)
    - Mutational Status (genes like NPM1, RUNX1, etc.)

    Avoid vague phrases like "may suggest". Use full, exact sentences from the text.

    Document Title: {title}
    Document Text: {text}

    Return JSON like:
    {{
        "document_title": "{title}",
        "aml_diagnosis_sentences": [],
        "precedent_disease_sentences": [],
        "performance_status_sentences": [],
        "mutational_status_sentences": []
    }}
    """

def field_extraction_prompt(text):
    return f"""
    Extract structured AML data from the following clinical note.

    Note:
    \"\"\"{text}\"\"\"

    Return JSON:
    {{
        "aml_diagnosis_date": {{"value": "", "evidence": ""}},
        "precedent_disease": [{{"disease": "", "date": "", "evidence": ""}}],
        "performance_status": {{
            "kps_score": {{"value": "", "date": "", "evidence": ""}},
            "ecog_score": {{"value": "", "date": "", "evidence": ""}}
        }},
        "mutational_status": {{
            "NPM1": {{"status": "", "date": "", "evidence": ""}},
            "RUNX1": {{"status": "", "date": "", "evidence": ""}},
            "TP53": {{"status": "", "date": "", "evidence": ""}},
            "FLT3": {{"status": "", "date": "", "evidence": ""}},
            "ASXL1": {{"status": "", "date": "", "evidence": ""}}
        }}
    }}
    """

function_definitions = [
    {
        "name": "extract_sentences",
        "description": "Extract evidence sentences grouped by clinical category",
        "parameters": {
            "type": "object",
            "properties": {
                "aml_diagnosis_sentences": {"type": "array", "items": {"type": "string"}},
                "precedent_disease_sentences": {"type": "array", "items": {"type": "string"}},
                "performance_status_sentences": {"type": "array", "items": {"type": "string"}},
                "mutational_status_sentences": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["aml_diagnosis_sentences", "precedent_disease_sentences", "performance_status_sentences", "mutational_status_sentences"]
        }
    },
    {
        "name": "extract_structured_data",
        "description": "Extract structured AML clinical data from sentences",
        "parameters": {
            "type": "object",
            "properties": {
                "aml_diagnosis_date": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "string"},
                        "evidence": {"type": "string"}
                    },
                    "required": ["value", "evidence"]
                },
                "precedent_disease": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "disease": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        },
                        "required": ["disease", "date", "evidence"]
                    }
                },
                "performance_status": {
                    "type": "object",
                    "properties": {
                        "kps_score": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "date": {"type": "string"},
                                "evidence": {"type": "string"}
                            },
                            "required": ["value", "date", "evidence"]
                        },
                        "ecog_score": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "date": {"type": "string"},
                                "evidence": {"type": "string"}
                            },
                            "required": ["value", "date", "evidence"]
                        }
                    },
                    "required": ["kps_score", "ecog_score"]
                },
                "mutational_status": {
                    "type": "object",
                    "properties": {
                        "NPM1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["status", "date", "evidence"]},
                        "RUNX1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["status", "date", "evidence"]},
                        "TP53": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["status", "date", "evidence"]},
                        "FLT3": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["status", "date", "evidence"]},
                        "ASXL1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["status", "date", "evidence"]}
                    },
                    "required": ["NPM1", "RUNX1", "TP53", "FLT3", "ASXL1"]
                }
            },
            "required": ["aml_diagnosis_date", "precedent_disease", "performance_status", "mutational_status"]
        }
    }
]
