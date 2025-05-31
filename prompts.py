# prompts.py
def sentence_extraction_prompt(title, text):
   return f"""
You are analyzing a clinical document for an AML cancer patient. Extract all sentences that contain potential evidence for the following categories:
1. AML Diagnosis Date  
2. Precedent Disease (with the date of mention)  
3. Performance Status at Baseline:
   - ECOG score (0-4)
   - Karnofsky score (KPS)
   - With associated dates  
4. Mutational Status (with gene name + value + date if available):
   - NPM1, RUNX1, TP53, FLT3, ASXL1
Return a JSON with relevant sentences grouped under each category. Include the document title.
Document Title: {title}
Document Text:
{text}
Return JSON in this format:
{{
 "document_title": "title of the document",
 "aml_diagnosis_sentences": [],
 "precedent_disease_sentences": [],
 "performance_status_sentences": [],
 "mutational_status_sentences": []
}}
"""
def field_extraction_prompt(text):
   return f"""
Extract the following information from the clinical note provided below. Return output in JSON format only.
Clinical Note:
\"\"\"{text}\"\"\"
Extract and return this information:
1. AML Diagnosis Date — mm/dd/yyyy format
2. Precedent Disease — a list of objects, each with:
  - disease name
  - associated date (mm/dd/yyyy)
3. Performance Status at Baseline:
  - KPS score (number or "Not mentioned")
  - KPS date
  - ECOG score (0–4 or "Not mentioned")
  - ECOG date
4. Mutational Status — dictionary for:
  - NPM1, RUNX1, TP53, FLT3, ASXL1
  - For each: status, date of record, evidence
Return JSON with this structure:
{{
 "document_title": "",
 "aml_diagnosis_date": {{
   "value": "",
   "evidence": ""
 }},
 "precedent_disease": [],
 "performance_status": {{
   "kps_score": {{
     "value": "",
     "date": "",
     "evidence": ""
   }},
   "ecog_score": {{
     "value": "",
     "date": "",
     "evidence": ""
   }}
 }},
 "mutational_status": {{
   "NPM1": {{}},
   "RUNX1": {{}},
   "TP53": {{}},
   "FLT3": {{}},
   "ASXL1": {{}}
 }}
}}
"""