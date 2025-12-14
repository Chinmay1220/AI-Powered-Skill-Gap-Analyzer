SYSTEM_PROMPT = """You are a career assistant that performs evidence-based skill gap analysis.
Rules:
- Do NOT make hiring decisions or rank candidates.
- Provide advisory feedback only.
- Ground claims in the provided Resume, Job Description, and Retrieved Context.
- If evidence is insufficient, say so.
- Return VALID JSON only."""

USER_PROMPT_TEMPLATE = """Analyze the fit between the Resume and Job Description.

Resume:
\"\"\"{resume}\"\"\"

Job Description:
\"\"\"{jd}\"\"\"

Retrieved Context (benchmarks/expectations/resources):
{context}

Return JSON with keys:
- inferred_role (string)
- inferred_level (string: Entry/Mid/Senior)
- summary (string)
- skill_gaps (array of objects):
  - skill (string)
  - status (missing|weak|strong)
  - rationale (string)
  - evidence (array of {{source, snippet}})
- resume_rewrites (array of objects):
  - original (string)  # a resume bullet from the resume
  - improved (string)  # rewritten bullet with metrics/keywords where appropriate
  - why (string)
- learning_plan (array of objects):
  - skill (string)
  - plan (array of strings)
Be concise but specific.
"""
