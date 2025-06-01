# main.py

import json
import os
import pandas as pd
from prompts import sentence_extraction_prompt, field_extraction_prompt, function_definitions
from utils import load_config, call_openai_with_function
from schemas import StructuredOutput

# Load config and model name
openai_config = load_config()
model = openai_config['gpt_models']['model_gpt4o']

input_file = 'medicaldata.csv'
sentence_output_file = 'output/extracted_sentences.json'
structured_output_file = 'output/structured_data.json'

sentence_results = []
structured_results = []

def process_row(index, row):
    title = row.get('title', '')
    text = row.get('text', '')
    if not text:
        return

    # Step 1: Extract sentences
    prompt1 = sentence_extraction_prompt(title, text)
    sentence_response = call_openai_with_function(model, prompt1, function_definitions, 'extract_sentences')
    if not sentence_response:
        return

    sentence_response["document_title"] = title
    sentence_results.append(sentence_response)

    # Step 2: Combine text and extract structured data
    combined_text = ". ".join(
        sentence_response.get('aml_diagnosis_sentences', []) +
        sentence_response.get('precedent_disease_sentences', []) +
        sentence_response.get('performance_status_sentences', []) +
        sentence_response.get('mutational_status_sentences', [])
    )

    prompt2 = field_extraction_prompt(combined_text)
    structured_response = call_openai_with_function(model, prompt2, function_definitions, 'extract_structured_data')
    if not structured_response:
        return

    structured_response["document_title"] = title
    try:
        validated = StructuredOutput(**structured_response)
        structured_results.append(validated.model_dump())
    except Exception as e:
        print(f"⚠️ Validation error on row {index}:", e)

def main():
    os.makedirs("output", exist_ok=True)
    df = pd.read_csv(input_file)

    for i, row in df.iterrows():
        process_row(i, row)

    # Save results
    with open(sentence_output_file, 'w', encoding='utf-8') as f:
        json.dump(sentence_results, f, indent=4)

    with open(structured_output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_results, f, indent=4)

    print("✅ Data extraction complete and saved.")

if __name__ == "__main__":
    main()
