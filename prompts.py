# prompts.py
def get_extraction_functions():
    """Returns both extraction functions matching the original two-prompt approach"""
    return [
        {
            "name": "extract_relevant_sentences",
            "description": "Extract relevant sentences matching the original first prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_title": {"type": "string"},
                    "aml_diagnosis_sentences": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "precedent_disease_sentences": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "performance_status_sentences": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "mutational_status_sentences": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": [
                    "document_title",
                    "aml_diagnosis_sentences",
                    "precedent_disease_sentences",
                    "performance_status_sentences",
                    "mutational_status_sentences"
                ]
            }
        },
        {
            "name": "extract_structured_fields",
            "description": "Extract structured fields matching the original second prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "aml_diagnosis_date": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "evidence": {"type": "string"}
                        }
                    },
                    "precedent_disease": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "disease_name": {"type": "string"},
                                "date": {"type": "string"},
                                "evidence": {"type": "string"}
                            }
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
                                }
                            },
                            "ecog_score": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            }
                        }
                    },
                    "mutational_status": {
                        "type": "object",
                        "properties": {
                            "NPM1": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            },
                            "RUNX1": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            },
                            "TP53": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            },
                            "FLT3": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            },
                            "ASXL1": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "required": [
                    "aml_diagnosis_date",
                    "precedent_disease",
                    "performance_status",
                    "mutational_status"
                ]
            }
        }
    ]
