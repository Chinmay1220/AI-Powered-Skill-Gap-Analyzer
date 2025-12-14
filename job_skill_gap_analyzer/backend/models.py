from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., description="Extracted resume text")
    job_description: str = Field(..., description="Job description text")
    target_role: Optional[str] = Field(None, description="Optional target role hint")

class Evidence(BaseModel):
    source: str
    snippet: str

class SkillGapItem(BaseModel):
    skill: str
    status: Literal["missing", "weak", "strong"]
    rationale: str
    evidence: List[Evidence] = []

class ResumeRewriteItem(BaseModel):
    original: str
    improved: str
    why: str

class LearningPlanItem(BaseModel):
    skill: str
    plan: List[str]

class AnalyzeResponse(BaseModel):
    summary: str
    inferred_role: str
    inferred_level: str
    skill_gaps: List[SkillGapItem]
    resume_rewrites: List[ResumeRewriteItem]
    learning_plan: List[LearningPlanItem]
    retrieved_docs: List[Dict[str, Any]]  # for transparency/debug
    safety_notes: List[str]
