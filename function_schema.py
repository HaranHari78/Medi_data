function_schema = [
    {
        "name": "extract_patient_fields",
        "description": "Extract structured AML cancer data from the provided clinical text.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_title": {"type": "string"},
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
                            "disease_name": {"type": "string"},
                            "associated_date": {"type": "string"},
                            "evidence": {"type": "string"}
                        },
                        "required": ["disease_name", "associated_date", "evidence"]
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
                        "NPM1": {"type": "object"},
                        "RUNX1": {"type": "object"},
                        "TP53": {"type": "object"},
                        "FLT3": {"type": "object"},
                        "ASXL1": {"type": "object"}
                    },
                    "required": ["NPM1", "RUNX1", "TP53", "FLT3", "ASXL1"]
                }
            },
            "required": [
                "document_title",
                "aml_diagnosis_date",
                "precedent_disease",
                "performance_status",
                "mutational_status"
            ]
        }
    }
]
