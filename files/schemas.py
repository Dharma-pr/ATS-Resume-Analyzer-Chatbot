from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ResumeData(BaseModel):
    skills: List[str] = []
    experience: List[str] = []
    education: List[str] = []
    certifications: List[str] = []
    projects: List[str] = []
    raw_text: str

class JobDescriptionInput(BaseModel):
    title: str
    content: str

class AnalysisResult(BaseModel):
    match_score: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    semantic_gaps: Dict
    recommendations: List[str]

class ChatMessageInput(BaseModel):
    analysis_id: int
    message: str

class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime