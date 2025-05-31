import json
import os
import re
import pandas as pd
from typing import Dict, List
from utils import load_config, call_openai_api_with_functions, extract_with_timeout
from prompts import get_extraction_functions

def clean_text(text: str) -> str:
    """Clean text by removing special characters and extra whitespace"""
    return re.sub(r'\s+', ' ', text).strip()

def process_document(text: str, title: str, model: str) -> Dict:
    """Process a single document using two-step function calling"""
    functions = get_extraction_functions()
    
    # Initialize results
    sentence_results = {}
    structured_results = {}
    
    try:
        # STEP 1: Sentence extraction (matches first prompt)
        sentence_response = extract_with_timeout(
            lambda: call_openai_api_with_functions(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"""
                    You are analyzing a clinical document for an AML cancer patient. 
                    Extract all sentences that contain potential evidence for:
                    1. AML Diagnosis Date  
                    2. Precedent Disease (with date)  
                    3. Performance Status (ECOG/KPS with dates)  
                    4. Mutational Status (NPM1, RUNX1, TP53, FLT3, ASXL1)
                    
                    Document Title: {title}
                    Document Text: {clean_text(text)}
                    """
                }],
                functions=functions,
                function_call={"name": "extract_relevant_sentences"}
            ),
            timeout=30
        )
        
        if not sentence_response:
            return {}
            
        sentence_results = {
            "document_title": title,
            "aml_diagnosis_sentences": sentence_response.get("aml_diagnosis_sentences", []),
            "precedent_disease_sentences": sentence_response.get("precedent_disease_sentences", []),
            "performance_status_sentences": sentence_response.get("performance_status_sentences", []),
            "mutational_status_sentences": sentence_response.get("mutational_status_sentences", [])
        }
        
        # STEP 2: Structured extraction (matches second prompt)
        combined_text = " ".join(
            sentence_results['aml_diagnosis_sentences'] +
            sentence_results['precedent_disease_sentences'] +
            sentence_results['performance_status_sentences'] +
            sentence_results['mutational_status_sentences']
        )
        
        structured_response = extract_with_timeout(
            lambda: call_openai_api_with_functions(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Extract structured information from:
                    {clean_text(combined_text)}
                    
                    Required fields:
                    1. AML Diagnosis Date (mm/dd/yyyy)
                    2. Precedent Diseases (name + date)
                    3. Performance Status (KPS + ECOG with dates)
                    4. Mutational Status (NPM1, RUNX1, TP53, FLT3, ASXL1)
                    """
                }],
                functions=functions,
                function_call={"name": "extract_structured_fields"}
            ),
            timeout=30
        )
        
        if structured_response:
            structured_results = structured_response
            structured_results["document_title"] = title
            
    except Exception as e:
        print(f"Error processing document {title[:50]}...: {e}")
    
    return {
        "sentence_results": sentence_results,
        "structured_results": structured_results
    }

def main():
    # Load configuration
    config = load_config()
    model = config['gpt_models']['model_gpt4o']
    input_file = "medicaldata.csv"
    
    # Initialize results
    all_sentence_results = []
    all_structured_results = []
    
    # Load and process data
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
        
        for index, row in df.iterrows():
            title = row.get('title', "")
            text = row.get('text', "")
            
            if not text:
                continue
                
            print(f"Processing document {index+1}/{len(df)}: {title[:50]}...")
            
            results = process_document(text, title, model)
            
            if results.get("sentence_results"):
                all_sentence_results.append(results["sentence_results"])
            if results.get("structured_results"):
                all_structured_results.append(results["structured_results"])
                
    except Exception as e:
        print(f"Error processing CSV file: {e}")
    
    # Save outputs (matching original format)
    os.makedirs("output", exist_ok=True)
    
    try:
        with open("output/extracted_sentences.json", 'w', encoding='utf-8') as f:
            json.dump(all_sentence_results, f, indent=4)
        
        with open("output/structured_data.json", 'w', encoding='utf-8') as f:
            json.dump(all_structured_results, f, indent=4)
            
        print(f"""
        Processing complete!
        - Extracted sentences saved to: output/extracted_sentences.json
        - Structured data saved to: output/structured_data.json
        """)
        
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
