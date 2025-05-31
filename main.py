import json
from typing import Dict
from utils import call_openai_api_with_functions
from prompts import get_extraction_functions

def process_medical_document(document_text: str) -> Dict:
    """
    End-to-end medical document processor:
    1. Extracts relevant sentences
    2. Converts them to structured data
    """
    # --- Stage 1: Extract Sentences ---
    stage1_result = call_openai_api_with_functions(
        model="gpt-4",
        messages=[{"role": "user", "content": document_text}],
        functions=get_extraction_functions(),
        function_call={"name": "extract_relevant_sentences"}
    )
    
    if not stage1_result:
        raise ValueError("❌ Stage 1 failed: No sentences extracted")

    # --- Stage 2: Structure Data ---
    stage2_result = call_openai_api_with_functions(
        model="gpt-4",
        messages=[
            {"role": "user", "content": document_text},
            {"role": "assistant", "content": json.dumps(stage1_result)}
        ],
        functions=get_extraction_functions(),
        function_call={"name": "extract_structured_fields"}
    )

    return stage2_result or {}

if __name__ == "__main__":
    # Example Usage
    sample_report = """
    PATIENT: John Doe
    DATE: 2023-10-15
    DIAGNOSIS: AML with FLT3-ITD mutation (2023-09-01).
    PRIOR HISTORY: MDS (2022-05-10), ECOG 1.
    GENETICS: NPM1 negative, TP53 positive.
    """
    
    try:
        result = process_medical_document(sample_report)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
