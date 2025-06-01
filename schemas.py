# schemas.py

from pydantic import BaseModel
from typing import List

class AMLDiagnosis(BaseModel):
    value: str
    evidence: str

class PrecedentDisease(BaseModel):
    disease: str
    date: str
    evidence: str

class Score(BaseModel):
    value: str
    date: str
    evidence: str

class PerformanceStatus(BaseModel):
    kps_score: Score
    ecog_score: Score

class MutationStatusEntry(BaseModel):
    status: str
    date: str
    evidence: str

class MutationStatus(BaseModel):
    NPM1: MutationStatusEntry
    RUNX1: MutationStatusEntry
    TP53: MutationStatusEntry
    FLT3: MutationStatusEntry
    ASXL1: MutationStatusEntry

class StructuredOutput(BaseModel):
    document_title: str
    aml_diagnosis_date: AMLDiagnosis
    precedent_disease: List[PrecedentDisease]
    performance_status: PerformanceStatus
    mutational_status: MutationStatus
