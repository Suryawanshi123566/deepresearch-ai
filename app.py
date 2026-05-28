import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #d4dde8;
}

.stApp {
    background: #080d14;
    background-image:
        radial-gradient(ellipse 70% 45% at 15% 5%, rgba(0,190,255,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 85% 95%, rgba(100,60,255,0.06) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2300beff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3.5rem 5rem; max-width: 1280px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1520; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2rem;
    border-bottom: 1px solid rgba(0,190,255,0.1);
    margin-bottom: 3rem;
}
.topbar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.logo-icon {
    width: 36px;
    height: 36px;
    border: 1.5px solid rgba(0,190,255,0.5);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    background: rgba(0,190,255,0.06);
}
.logo-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #d4dde8;
}
.logo-text span { color: #00beff; }
.topbar-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00beff;
    border: 1px solid rgba(0,190,255,0.25);
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    background: rgba(0,190,255,0.05);
}

/* ── Hero ── */
.hero {
    padding: 0 0 3.5rem;
}
.hero-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #00beff;
    margin-bottom: 1.2rem;
    opacity: 0.8;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.02em;
    color: #eef2f7;
    margin: 0 0 1.5rem;
}
.hero h1 em {
    font-style: italic;
    color: #00beff;
    background: linear-gradient(135deg, #00beff, #6440ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: #7a94b0;
    max-width: 500px;
    line-height: 1.75;
    border-left: 2px solid rgba(0,190,255,0.25);
    padding-left: 1rem;
}

/* ── Horizontal rule ── */
.hr {
    height: 1px;
    background: linear-gradient(90deg, rgba(0,190,255,0.4), rgba(100,64,255,0.2), transparent);
    margin: 0 0 2.5rem;
}

/* ── Input card ── */
.input-wrap {
    background: rgba(13,24,40,0.8);
    border: 1px solid rgba(0,190,255,0.12);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.input-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,190,255,0.4), transparent);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(0,10,25,0.6) !important;
    border: 1px solid rgba(0,190,255,0.18) !important;
    border-radius: 10px !important;
    color: #eef2f7 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: #00beff !important;
}
.stTextInput > div > div > input::placeholder { color: #2d4a6a !important; }
.stTextInput > div > div > input:focus {
    border-color: rgba(0,190,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,190,255,0.08), 0 0 20px rgba(0,190,255,0.05) !important;
    outline: none !important;
}
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #00beff !important;
    font-weight: 400 !important;
    opacity: 0.8 !important;
}

/* ── Button ── */
.stButton > button {
    background: transparent !important;
    color: #00beff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(0,190,255,0.4) !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    position: relative !important;
    overflow: hidden !important;
    width: 100% !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, rgba(0,190,255,0.08), rgba(100,64,255,0.06)) !important;
    opacity: 0 !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    border-color: rgba(0,190,255,0.7) !important;
    box-shadow: 0 0 20px rgba(0,190,255,0.15), 0 0 40px rgba(0,190,255,0.05) !important;
    color: #80dfff !important;
}
.stButton > button:hover::before { opacity: 1 !important; }
.stButton > button:active { transform: scale(0.99) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(13,24,40,0.6);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(0,190,255,0.3);
    background: rgba(0,190,255,0.04);
}
.step-card.done {
    border-color: rgba(0,210,140,0.25);
    background: rgba(0,210,140,0.03);
}
.step-card::after {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 2px;
    background: rgba(255,255,255,0.04);
    transition: background 0.3s;
}
.step-card.active::after { background: linear-gradient(180deg, #00beff, #6440ff); }
.step-card.done::after   { background: #00d28c; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    font-weight: 400;
    letter-spacing: 0.12em;
    color: #2d4a6a;
}
.step-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #d4dde8;
}
.step-desc {
    font-size: 0.75rem;
    color: #3d5a7a;
    margin-top: 0.2rem;
    padding-left: 1.8rem;
}
.step-status {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.status-waiting  { color: #1e3a5f; }
.status-running  { color: #00beff; }
.status-done     { color: #00d28c; }

/* ── Section label ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #2d4a6a;
    margin-bottom: 1rem;
}

/* ── Results ── */
.result-block {
    background: rgba(8,16,28,0.7);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-block-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00beff;
    margin-bottom: 0.8rem;
    opacity: 0.7;
}
.result-block-content {
    font-size: 0.88rem;
    line-height: 1.8;
    color: #5a7a9a;
    white-space: pre-wrap;
}

/* ── Report & feedback ── */
.report-wrap {
    background: rgba(8,16,28,0.8);
    border: 1px solid rgba(0,190,255,0.15);
    border-radius: 16px;
    padding: 2.5rem 2.8rem;
    margin-top: 0.5rem;
    position: relative;
    overflow: hidden;
}
.report-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,190,255,0.5), rgba(100,64,255,0.3), transparent);
}
.feedback-wrap {
    background: rgba(8,16,28,0.8);
    border: 1px solid rgba(0,210,140,0.15);
    border-radius: 16px;
    padding: 2.5rem 2.8rem;
    margin-top: 0.5rem;
    position: relative;
    overflow: hidden;
}
.feedback-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,210,140,0.5), transparent);
}
.panel-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.panel-tag.cyan {
    color: #00beff;
    border-bottom: 1px solid rgba(0,190,255,0.12);
}
.panel-tag.green {
    color: #00d28c;
    border-bottom: 1px solid rgba(0,210,140,0.12);
}
.panel-tag::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.panel-tag.cyan::before  { background: #00beff; box-shadow: 0 0 6px #00beff; }
.panel-tag.green::before { background: #00d28c; box-shadow: 0 0 6px #00d28c; }

/* ── Global markdown text visibility fix ── */
.stMarkdown p,
.stMarkdown li,
.stMarkdown td,
.stMarkdown blockquote {
    color: #c8d8ea !important;
    line-height: 1.85 !important;
    font-size: 0.95rem !important;
}
.stMarkdown h1 {
    font-family: 'Playfair Display', serif !important;
    color: #eef2f7 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 1.5rem 0 0.8rem !important;
    letter-spacing: -0.01em !important;
}
.stMarkdown h2 {
    font-family: 'Playfair Display', serif !important;
    color: #ddeaf5 !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 2rem 0 0.6rem !important;
    padding-bottom: 0.4rem !important;
    border-bottom: 1px solid rgba(0,190,255,0.1) !important;
}
.stMarkdown h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #b0ccdf !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    margin: 1.4rem 0 0.4rem !important;
}
.stMarkdown strong {
    color: #eef2f7 !important;
    font-weight: 600 !important;
}
.stMarkdown em {
    color: #8ab4cc !important;
}
.stMarkdown a {
    color: #00beff !important;
    text-decoration: none !important;
    border-bottom: 1px solid rgba(0,190,255,0.3) !important;
}
.stMarkdown a:hover {
    border-bottom-color: #00beff !important;
}
.stMarkdown ul, .stMarkdown ol {
    padding-left: 1.4rem !important;
}
.stMarkdown li {
    margin-bottom: 0.4rem !important;
}
.stMarkdown code {
    background: rgba(0,190,255,0.08) !important;
    color: #00beff !important;
    border-radius: 4px !important;
    padding: 0.1rem 0.4rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stMarkdown blockquote {
    border-left: 3px solid rgba(0,190,255,0.3) !important;
    padding-left: 1rem !important;
    color: #7a94b0 !important;
    font-style: italic !important;
}
.stMarkdown hr {
    border: none !important;
    border-top: 1px solid rgba(0,190,255,0.1) !important;
    margin: 1.5rem 0 !important;
}

/* ── Example pills ── */
.pills-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.pill-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #1e3a5f;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.pill {
    background: rgba(0,10,25,0.4);
    border: 1px solid rgba(0,190,255,0.1);
    border-radius: 4px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    color: #3d6a9a;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Spinner ── */
.stSpinner > div { color: #00beff !important; }

/* ── Expander ── */
details { border: none !important; background: transparent !important; }
details summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #2d4a6a !important;
    letter-spacing: 0.12em !important;
    cursor: pointer;
    padding: 0.4rem 0 !important;
}
details summary:hover { color: #00beff !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #3d6a9a !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
    margin-top: 1rem !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(0,190,255,0.3) !important;
    color: #00beff !important;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #eef2f7;
    margin: 2.5rem 0 1.2rem;
    letter-spacing: -0.01em;
}

/* ── Warning ── */
.stAlert { border-radius: 10px !important; }

/* ── Footer ── */
.footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #0f2035;
    text-align: center;
    margin-top: 5rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("idle",     "status-waiting"),
        "running": ("● live",   "status-running"),
        "done":    ("✓ done",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">
        <div class="logo-icon">⚡</div>
        <span class="logo-text">Multi-Agent <span>Research AI</span></span>
    </div>
    <span class="topbar-badge">Multi-Agent Pipeline</span>
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">Autonomous AI Research Engine</div>
    <h1>Deep Research.<br><em>Instantly.</em></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping,
        writing, and critiquing — to deliver a polished research report
        on any Tech &amp; AI topic in minutes.
    </p>
</div>
<div class="hr"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_gap, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⟶  Execute Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="pills-row">
        <span class="pill-label">Try →</span>
        <span class="pill">LLM agents 2025</span>
        <span class="pill">CRISPR gene editing</span>
        <span class="pill">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("Search Agent scanning the web…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Reader Agent scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Writer drafting the research report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("Critic reviewing and scoring the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="hr" style="margin-top:2.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("Search Agent — raw output", expanded=False):
            st.markdown(
                f'<div class="result-block">'
                f'<div class="result-block-title">Search Agent Output</div>'
                f'<div class="result-block-content">{r["search"]}</div>'
                f'</div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("Reader Agent — raw output", expanded=False):
            st.markdown(
                f'<div class="result-block">'
                f'<div class="result-block-title">Reader Agent Output</div>'
                f'<div class="result-block-content">{r["reader"]}</div>'
                f'</div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="report-wrap">
            <div class="panel-tag cyan">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="↓  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-wrap">
            <div class="panel-tag green">Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Multi-Agent Research AI · LangChain multi-agent pipeline · Streamlit
</div>
""", unsafe_allow_html=True)
