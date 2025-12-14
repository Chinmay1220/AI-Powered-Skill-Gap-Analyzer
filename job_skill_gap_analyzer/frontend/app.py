import io
import json
import streamlit as st
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Skill Gap Analyzer", layout="wide", page_icon="🎯")

# ---------------------------
# CSS (modern dark, readable)
# ---------------------------
st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 1.2rem; padding-bottom: 3rem;}
#MainMenu, footer {visibility: hidden;}

.stApp {
  background:
    radial-gradient(900px 450px at 10% 10%, rgba(124,58,237,.22), transparent 60%),
    radial-gradient(800px 400px at 90% 20%, rgba(6,182,212,.16), transparent 55%),
    linear-gradient(135deg, #06070c, #070a14);
  color: #e9eef6;
}

.hero {
  border-radius: 22px;
  padding: 22px 22px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 18px 70px rgba(0,0,0,0.45);
}
.hero h1 {margin: 0; font-size: 2.05rem; letter-spacing: -0.5px;}
.hero p {margin: 8px 0 0 0; color: rgba(233,238,246,0.72); line-height: 1.4;}
.badges {margin-top: 12px; display:flex; flex-wrap:wrap; gap:8px;}
.badge {
  display:inline-flex; gap:8px; align-items:center;
  padding: 6px 10px; border-radius: 999px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  color: rgba(233,238,246,0.92);
  font-size: 0.85rem;
}

.card {
  border-radius: 18px;
  padding: 14px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 14px 50px rgba(0,0,0,0.40);
}
.cardTitle {font-weight: 850; letter-spacing: -0.2px; margin-bottom: 6px;}
.muted {color: rgba(233,238,246,0.70); font-size: 0.95rem;}

div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input,
div[data-testid="stFileUploader"] section {
  background: rgba(10,15,30,0.70) !important;
  color: #e9eef6 !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  border-radius: 14px !important;
}
textarea::placeholder, input::placeholder {color: rgba(233,238,246,0.45) !important;}

div[data-testid="stFileUploader"] * { color: rgba(233,238,246,0.92) !important; }
div[data-testid="stFileUploader"] button {
  background: rgba(255,255,255,0.10) !important;
  color: rgba(233,238,246,0.95) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  border-radius: 12px !important;
}

.stButton > button {
  border-radius: 14px !important;
  font-weight: 850 !important;
  background: linear-gradient(90deg, #7c3aed 0%, #2563eb 60%, #06b6d4 100%) !important;
  border: 0 !important;
  color: white !important;
  box-shadow: 0 0 26px rgba(124,58,237,0.18), 0 0 18px rgba(6,182,212,0.10);
}

div[data-testid="stExpander"] details {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header (hero)
# ---------------------------
st.markdown("""
<div class="hero">
  <h1>📄 Job Skill Gap Analyzer </h1>
  <p>Upload your resume and paste a job description. This tool provides <b>advisory</b> skill gap insights with supporting evidence.</p>
  <div class="badges">
    <span class="badge">🧠 Precised Results</span>
    <span class="badge">🔎 Evidence</span>
    <span class="badge">✍️ Rewrites</span>
    <span class="badge">📄 PDF report</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------------------
# PDF helper
# ---------------------------
def wrap_lines(text: str, max_chars=95):
    text = (text or "").replace("\n", " ").strip()
    if not text:
        return []
    words = text.split()
    lines, cur, cur_len = [], [], 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if cur_len + add > max_chars:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += add
    if cur:
        lines.append(" ".join(cur))
    return lines

def make_pdf_report(result: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    x = 0.8 * inch
    y = height - 0.8 * inch
    lh = 14

    def draw(text, bold=False):
        nonlocal y
        if y < 0.8 * inch:
            c.showPage()
            y = height - 0.8 * inch
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 11 if bold else 10)
        c.drawString(x, y, str(text)[:160])
        y -= lh

    draw("Career AI · Skill Gap Analyzer Report", bold=True)
    draw("")
    draw(f"Inferred role: {result.get('inferred_role','')}", bold=True)
    draw(f"Level: {result.get('inferred_level','')}", bold=True)
    draw("")

    summary = result.get("summary", "")
    if summary:
        draw("Summary", bold=True)
        for ln in wrap_lines(summary):
            draw(ln)
        draw("")

    draw("Skill Gaps", bold=True)
    for g in (result.get("skill_gaps", []) or [])[:30]:
        draw(f"- {g.get('skill','Unknown')} [{str(g.get('status','')).upper()}]", bold=True)
        for ln in wrap_lines(g.get("rationale", "")):
            draw(f"  {ln}")
    draw("")

    draw("Learning Plan", bold=True)
    for lp in (result.get("learning_plan", []) or [])[:20]:
        draw(f"- {lp.get('skill','Unknown')}", bold=True)
        for step in (lp.get("plan", []) or [])[:10]:
            for ln in wrap_lines(str(step)):
                draw(f"  • {ln}")
        draw("")

    c.save()
    return buf.getvalue()

# ---------------------------
# UI (same flow, nicer)
# ---------------------------
col1, col2 = st.columns(2, gap="large")

resume_text = ""  # keep outside so button logic works

with col1:
    st.markdown("<div class='card'><div class='cardTitle'>1) Upload Resume (PDF)</div><div class='muted'>PDF → text extraction via backend</div></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Resume PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        try:
            resp = requests.post(f"{API_URL}/extract_resume", files=files, timeout=120)
            resp.raise_for_status()
            resume_text = resp.json().get("resume_text", "")
            st.success("Resume extracted ✅")
            with st.expander("View extracted resume text"):
                st.text_area("Resume text", resume_text, height=250)
        except Exception as e:
            st.error("Resume extraction failed.")
            st.code(str(e))

with col2:
    st.markdown("<div class='card'><div class='cardTitle'>2) Paste Job Description</div><div class='muted'>Paste full JD for best results</div></div>", unsafe_allow_html=True)
    jd = st.text_area("Job description", height=250, label_visibility="collapsed", placeholder="Paste the full job description here…")

st.write("")
st.markdown("<div class='card'><div class='cardTitle'>Optional: Target role hint</div><div class='muted'>Example: Data Engineer, ML Engineer, SWE</div></div>", unsafe_allow_html=True)
target_role = st.text_input("Optional role", label_visibility="collapsed", placeholder="Data Engineer / ML Engineer / SWE")

st.divider()

# ---------------------------
# Analyze
# ---------------------------
if st.button("Analyze Skill Gaps 🚀", type="primary", use_container_width=True):
    if not resume_text.strip():
        st.error("Please upload a resume PDF first.")
        st.stop()
    if not jd.strip():
        st.error("Please paste a job description.")
        st.stop()

    payload = {
        "resume_text": resume_text,
        "job_description": jd,
        "target_role": target_role.strip() or None
    }

    with st.spinner("Analyzing..."):
        resp = requests.post(f"{API_URL}/analyze", json=payload, timeout=240)

        # Prevent Streamlit JSONDecodeError: show backend text if not JSON
        if resp.status_code != 200:
            st.error(f"Backend error ({resp.status_code})")
            st.code(resp.text[:4000])
            st.stop()

        try:
            result = resp.json()
        except Exception:
            st.error("Backend did not return JSON (got HTML/text instead).")
            st.code(resp.text[:4000])
            st.stop()

    st.session_state["result"] = result

# ---------------------------
# Results
# ---------------------------
result = st.session_state.get("result")
if result:
    tabs = st.tabs(["✅ Overview", "🧩 Skill Gaps", "✍️ Rewrites", "📚 Learning", "🔎 RAG", "📄 PDF"])

    with tabs[0]:
        st.markdown("<div class='card'><div class='cardTitle'>Summary</div></div>", unsafe_allow_html=True)
        st.write(result.get("summary", ""))

        st.info(
            f"Inferred role: **{result.get('inferred_role','')}** | "
            f"Level: **{result.get('inferred_level','')}**"
        )

    with tabs[1]:
        st.markdown("<div class='card'><div class='cardTitle'>Skill Gaps</div><div class='muted'>Evidence included when available</div></div>", unsafe_allow_html=True)

        for item in result.get("skill_gaps", []):
            status = str(item.get("status", "")).lower()
            emoji = {"strong": "🟢", "weak": "🟡", "missing": "🔴"}.get(status, "⚪")
            with st.expander(f"{emoji} {item.get('skill','Unknown')} — {status.upper()}"):
                st.write(item.get("rationale", ""))

                ev = item.get("evidence", [])
                if ev:
                    st.markdown("**Evidence**")
                    for e in ev[:8]:
                        st.markdown(f"- **{e.get('source','source')}**: {e.get('snippet','')}")

    with tabs[2]:
        st.markdown("<div class='card'><div class='cardTitle'>Resume Rewrites</div><div class='muted'>Copy-paste improved bullets</div></div>", unsafe_allow_html=True)

        for rr in result.get("resume_rewrites", []):
            with st.expander((rr.get("original", "")[:90] + "…") if rr.get("original") else "Rewrite"):
                st.markdown("**Original**")
                st.write(rr.get("original", ""))
                st.markdown("**Improved**")
                st.success(rr.get("improved", ""))
                if rr.get("why"):
                    st.caption(rr.get("why"))

    with tabs[3]:
        st.markdown("<div class='card'><div class='cardTitle'>Learning Plan</div><div class='muted'>Actionable steps per skill</div></div>", unsafe_allow_html=True)

        for lp in result.get("learning_plan", []):
            with st.expander(f"📘 {lp.get('skill','Unknown')}"):
                for step in lp.get("plan", []):
                    st.markdown(f"- {step}")

    with tabs[4]:
        st.markdown("<div class='card'><div class='cardTitle'>Retrieved Docs (RAG transparency)</div></div>", unsafe_allow_html=True)
        st.json(result.get("retrieved_docs", []))

        with st.expander("⚖️ Safety notes"):
            for s in result.get("safety_notes", []):
                st.markdown(f"- {s}")

    with tabs[5]:
        st.markdown("<div class='card'><div class='cardTitle'>Download Report</div><div class='muted'>PDF + JSON</div></div>", unsafe_allow_html=True)

        pdf_bytes = make_pdf_report(result)
        st.download_button(
            "⬇️ Download Career Report (PDF)",
            data=pdf_bytes,
            file_name="career_ai_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Raw JSON",
            data=json.dumps(result, indent=2).encode("utf-8"),
            file_name="career_ai_result.json",
            mime="application/json",
            use_container_width=True
        )
