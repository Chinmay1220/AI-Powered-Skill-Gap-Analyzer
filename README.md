# 🚀 Career AI: Job Description → Skill Gap Analyzer  
**Beyond the Match Score: How AI Delivers the Career Feedback You Actually Need**

---

## 📌 Introduction: The Black Box of Job Rejection

For students and early-career professionals, the modern job search often feels like shouting into the void. You spend hours tailoring your resume, writing thoughtful cover letters, and submitting applications—only to receive a generic rejection email days or weeks later, if you hear back at all.

This lack of meaningful feedback creates a frustrating **“black box”** where candidates are left guessing *why* they were rejected and *what* they should improve.

**Career AI: Job Description → Skill Gap Analyzer** is built to crack open that black box **before you even apply**.

Instead of offering a vague “match score,” this AI-powered system explains **why** a candidate may be rejected, **which skills are weak or missing**, and **exactly what to do next**, grounded in real-world, industry-aligned expectations.
<img width="2752" height="1536" alt="unnamed (1)" src="https://github.com/user-attachments/assets/66425a6e-47ca-4d5f-a438-15381a526d79" />

---

## 🎯 Problem

Applicants are routinely rejected without feedback.  
Most resume tools rely on shallow keyword matching, ATS-style scoring, or opaque “fit percentages” that are neither explainable nor actionable.

As a result, candidates:
- Don’t know which skills actually matter
- Don’t know how far they are from expectations
- Don’t know how to improve strategically

---

## 💡 Solution

This project implements a **Retrieval-Augmented Generation (RAG)** system that:

- Takes a **resume + job description**
- Retrieves **role expectations, skill benchmarks, and learning resources** from a vector database
- Uses an LLM to generate **evidence-grounded**:
  - Skill gap analysis
  - Resume rewrite suggestions
  - Personalized learning plans

The goal is not automation — it is **explainable career guidance**.

---

## 🧠 Beyond a “Match Score”: Explaining the *Why*

Before comparing skills, the system:
- Analyzes the job description to infer the **target role**
- Estimates the expected **seniority level**
- Selects **role-appropriate benchmarks** from its knowledge base

Each skill is classified as:
- ✅ **Strong**
- ⚠️ **Weak**
- ❌ **Missing**

Every classification includes **clear rationale**, shifting the resume improvement process from guesswork to **data-driven strategy**.

---

## 🧪 Fighting AI Hallucinations with RAG

To ensure accuracy and trust, the system uses **Retrieval-Augmented Generation (RAG)**.

Instead of relying solely on an LLM’s general knowledge, the backend:
1. Retrieves relevant role expectations, skill benchmarks, and learning resources from a **Pinecone vector database**
2. Uses those documents as **grounding evidence**
3. Generates recommendations strictly based on retrieved knowledge

This prevents hallucinations and ensures guidance is:
- Grounded in real-world hiring standards
- Transparent and auditable
- Far more reliable than generic AI advice

> *Generative AI is used not just to generate text, but to provide explainable, evidence-based career guidance.*

---

## 🛠️ Turning Analysis into Action

The system doesn’t stop at diagnosis. It provides **actionable next steps**:

### ✍️ Resume Rewrite Suggestions
Targeted bullet-point rewrites help users better highlight existing experience in ways that align with hiring expectations.

### 📚 Personalized Learning Plan
For weak or missing skills, the system generates a structured learning roadmap with:
- Skill-specific guidance
- Project ideas
- Practical next steps

This transforms feedback into a **career improvement plan**, not just a report.

---

## 🔍 Transparency by Design

Most hiring algorithms are opaque. This system is intentionally the opposite.

For every recommendation, users can view:
- Retrieved benchmark documents
- Evidence snippets supporting each conclusion

This aligns with responsible AI principles such as **computational skepticism**, **traceability**, and **explainability**.

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI Backend
 ├── Resume PDF Extraction
 ├── RAG Retrieval (Pinecone)
 ├── Prompt Orchestration + Safety
 │
 ▼
OpenAI Embeddings → Pinecone Vector DB
 │
 ▼
OpenAI GPT (Grounded Generation)
 │
 ▼
Structured JSON Response
 │
 ▼
Streamlit UI + PDF Report Download
---
```

hi
