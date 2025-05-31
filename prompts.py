from typing import List, Dict, Any

def get_extraction_functions() -> List[Dict[str, Any]]:
    """Returns function definitions for two-stage medical data extraction"""
    return [
        # Stage 1: Sentence Extraction
        {
            "name": "extract_relevant_sentences",
            "description": "Identify and extract relevant sentences about AML diagnosis and related medical factors",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_title": {
                        "type": "string",
                        "description": "Title or identifier of the medical document"
                    },
                    "aml_diagnosis_sentences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sentences confirming AML diagnosis including subtype if available"
                    },
                    "precedent_disease_sentences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sentences describing prior hematologic disorders or relevant cancer history"
                    },
                    "performance_status_sentences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sentences indicating ECOG/Karnofsky performance status scores"
                    },
                    "mutational_status_sentences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sentences about genetic mutations (NPM1, FLT3, etc.) with testing dates if available"
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

        # Stage 2: Structured Data Extraction
        {
            "name": "extract_structured_fields",
            "description": "Convert extracted medical information into standardized structured format",
            "parameters": {
                "type": "object",
                "properties": {
                    "aml_diagnosis_date": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "string",
                                "description": "Date of AML diagnosis in YYYY-MM-DD format when available"
                            },
                            "evidence": {
                                "type": "string",
                                "description": "Supporting text from the document"
                            }
                        },
                        "required": ["evidence"]
                    },
                    "precedent_disease": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "disease_name": {
                                    "type": "string",
                                    "description": "Name of prior hematologic disorder or cancer"
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Date of diagnosis if available (YYYY-MM-DD)"
                                },
                                "evidence": {
                                    "type": "string",
                                    "description": "Supporting text from the document"
                                }
                            },
                            "required": ["disease_name", "evidence"]
                        }
                    },
                    "performance_status": {
                        "type": "object",
                        "properties": {
                            "kps_score": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Karnofsky Performance Status score (0-100)"
                                    },
                                    "date": {
                                        "type": "string",
                                        "description": "Assessment date in YYYY-MM-DD format"
                                    },
                                    "evidence": {
                                        "type": "string",
                                        "description": "Supporting text from the document"
                                    }
                                },
                                "required": ["value", "evidence"]
                            },
                            "ecog_score": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "ECOG Performance Status score (0-5)"
                                    },
                                    "date": {
                                        "type": "string",
                                        "description": "Assessment date in YYYY-MM-DD format"
                                    },
                                    "evidence": {
                                        "type": "string",
                                        "description": "Supporting text from the document"
                                    }
                                },
                                "required": ["value", "evidence"]
                            }
                        }
                    },
                    "mutational_status": {
                        "type": "object",
                        "properties": {
                            "NPM1": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "enum": ["Positive", "Negative", "Not Tested", "Unknown"],
                                        "description": "Mutation status"
                                    },
                                    "date": {
                                        "type": "string",
                                        "description": "Test date in YYYY-MM-DD format"
                                    },
                                    "evidence": {
                                        "type": "string",
                                        "description": "Supporting text from the document"
                                    }
                                },
                                "required": ["status", "evidence"]
                            },
                            "FLT3": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "enum": ["ITD Positive", "TKD Positive", "Negative", "Not Tested", "Unknown"],
                                        "description": "FLT3 mutation subtype when available"
                                    },
                                    "date": {
                                        "type": "string",
                                        "description": "Test date in YYYY-MM-DD format"
                                    },
                                    "evidence": {
                                        "type": "string",
                                        "description": "Supporting text from the document"
                                    }
                                },
                                "required": ["status", "evidence"]
                            },
                            # Additional genetic markers...
                            "RUNX1": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "enum": ["Positive", "Negative", "Not Tested", "Unknown"]
                                    },
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                },
                                "required": ["status", "evidence"]
                            },
                            "TP53": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "enum": ["Positive", "Negative", "Not Tested", "Unknown"]
                                    },
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                },
                                "required": ["status", "evidence"]
                            },
                            "ASXL1": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "enum": ["Positive", "Negative", "Not Tested", "Unknown"]
                                    },
                                    "date": {"type": "string"},
                                    "evidence": {"type": "string"}
                                },
                                "required": ["status", "evidence"]
                            }
                        },
                        "required": ["NPM1", "FLT3", "RUNX1", "TP53", "ASXL1"]
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
