import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from .models import AnalyzeRequest, AnalyzeResponse
from .rag import retrieve_context, format_context
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .openai_client import chat_json
from .parsers import extract_text_from_pdf_bytes
from .safety import safety_notes

app = FastAPI(title="Skill Gap Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for class demo; tighten for real deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract_resume")
async def extract_resume(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf_bytes(pdf_bytes)
    return {"resume_text": text}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    # Retrieval query can be JD + optional role hint
    retrieval_query = req.job_description
    if req.target_role:
        retrieval_query += f"\nTarget role hint: {req.target_role}"

    docs = retrieve_context(retrieval_query)
    context = format_context(docs)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        resume=req.resume_text,
        jd=req.job_description,
        context=context
    )

    raw = chat_json(SYSTEM_PROMPT, user_prompt)
    data = json.loads(raw)

    # Attach transparency fields
    data["retrieved_docs"] = docs
    data["safety_notes"] = safety_notes()

    return data
