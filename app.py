import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.web_scraper import scrape_url
from scraper.pdf_loader import load_pdf
from extractor.entity_extractor import extract_entities
from extractor.relation_extractor import extract_relations
from graph.graph_rag import build_graph, query_graph, get_graph_for_visualization, get_contradictions, get_quiz_questions
from graph.neo4j_client import Neo4jClient
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(page_title="GraphMind", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #F8FAFC; }
    .main .block-container { padding-top: 2rem; max-width: 1100px; }

    .topbar {
        background: white;
        border-bottom: 1px solid #E2E8F0;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #0F172A;
        text-align: center;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }
    .hero-accent { color: #2563EB; }
    .hero-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    .feature-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.3rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s, border-color 0.2s;
    }
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(37,99,235,0.08);
        border-color: #BFDBFE;
    }
    .feature-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .feature-title { color: #1E293B; font-weight: 600; font-size: 0.88rem; margin-bottom: 0.2rem; }
    .feature-desc { color: #94A3B8; font-size: 0.78rem; line-height: 1.5; }

    .step-card {
        background: #F1F5F9;
        border-left: 3px solid #2563EB;
        border-radius: 6px;
        padding: 0.65rem 1rem;
        margin: 0.3rem 0;
        color: #475569;
        font-size: 0.84rem;
    }
    .step-number { color: #2563EB; font-weight: 600; }

    .success-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #166534;
        font-size: 0.88rem;
    }
    .warning-box {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #92400E;
        font-size: 0.88rem;
    }
    .error-box {
        background: #FFF1F2;
        border: 1px solid #FECDD3;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #9F1239;
        font-size: 0.88rem;
        margin: 0.4rem 0;
    }
    .answer-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        color: #334155;
        line-height: 1.8;
        font-size: 0.92rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-number { font-size: 2rem; font-weight: 700; color: #2563EB; }
    .metric-label { color: #94A3B8; font-size: 0.75rem; margin-top: 0.2rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

    .stButton>button {
        background: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.55rem 1.3rem;
        font-weight: 500;
        font-size: 0.88rem;
        transition: background 0.2s, box-shadow 0.2s;
        width: 100%;
        box-shadow: 0 1px 2px rgba(37,99,235,0.2);
    }
    .stButton>button:hover {
        background: #1D4ED8;
        box-shadow: 0 4px 12px rgba(37,99,235,0.25);
    }

    .stTextInput>div>div>input {
        background: white;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        color: #0F172A;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stTextInput>div>div>input:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
    .stTextInput>div>div>input::placeholder { color: #94A3B8; }

    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 4px;
        gap: 2px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748B;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.45rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: white !important;
    }

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    div[data-testid="stExpander"] summary { color: #64748B; font-size: 0.84rem; }

    .stRadio label { color: #334155; font-size: 0.88rem; }

    .tag {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.74rem;
        font-weight: 500;
        margin: 2px;
    }
    .tag-green {
        background: #F0FDF4;
        color: #166534;
        border-color: #BBF7D0;
    }
    .tag-purple {
        background: #FAF5FF;
        color: #6B21A8;
        border-color: #E9D5FF;
    }

    .section-label {
        color: #475569;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown('<div class="hero-title">🧠 <span class="hero-accent">Graph</span>Mind</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Transform any knowledge source into an interactive, queryable graph · Powered by Neo4j · LLaMA 3.3 · Groq</div>', unsafe_allow_html=True)

# Feature cards
c1, c2, c3, c4 = st.columns(4)
features = [
    ("🌐", "Web Scraping", "Ingest any URL and extract structured knowledge automatically"),
    ("🕸️", "Knowledge Graph", "Entities and relationships stored in Neo4j AuraDB"),
    ("💬", "Graph RAG", "Multi-hop traversal for deeply connected answers"),
    ("⚡", "LLaMA 3.3 70B", "Powered by Groq for ultra-fast inference"),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Ingest", "💬 Query", "🕸️ Visualize", "⚠️ Contradictions", "🎓 Study Mode"
])

# TAB 1
with tab1:
    st.markdown('<div class="section-label">Knowledge Source</div>', unsafe_allow_html=True)
    with st.expander("How to use", expanded=False):
        st.markdown("""
        <div class="step-card"><span class="step-number">01 &nbsp;</span> Choose URL or PDF input</div>
        <div class="step-card"><span class="step-number">02 &nbsp;</span> Paste a URL or upload a PDF document</div>
        <div class="step-card"><span class="step-number">03 &nbsp;</span> Click Ingest — entities and relationships are extracted automatically</div>
        <div class="step-card"><span class="step-number">04 &nbsp;</span> Switch to Query or Visualize to explore your graph</div>
        """, unsafe_allow_html=True)

    source_type = st.radio("Input type:", ["🌐 URL", "📄 PDF"], horizontal=True)

    if source_type == "🌐 URL":
        url = st.text_input("", placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence", label_visibility="collapsed")
        if st.button("🚀 Ingest URL"):
            if url:
                with st.spinner("Scraping and building knowledge graph..."):
                    text = scrape_url(url)
                    if "Error" in text:
                        st.markdown(f'<div class="error-box">❌ {text}</div>', unsafe_allow_html=True)
                    else:
                        entities = extract_entities(text, url)
                        relations = extract_relations(text, entities)
                        n_e, n_r = build_graph(text, url, entities, relations)
                        st.markdown(f'<div class="success-box">✅ Extracted <b>{n_e} entities</b> and <b>{n_r} relationships</b></div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('<div class="section-label">Entities Found</div>', unsafe_allow_html=True)
                            for e in entities[:6]:
                                t = "tag-green" if e.get("type") == "Person" else "tag-purple" if e.get("type") == "Technology" else "tag"
                                st.markdown(f'<span class="{t}">{e["name"]}</span>', unsafe_allow_html=True)
                        with col2:
                            st.markdown('<div class="section-label">Relationships</div>', unsafe_allow_html=True)
                            for r in relations[:6]:
                                st.markdown(f'<span class="tag">{r["from"]}</span> → <span class="tag-green">{r["relation"]}</span> → <span class="tag">{r["to"]}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ Please enter a URL</div>', unsafe_allow_html=True)
    else:
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        if st.button("🚀 Ingest PDF"):
            if uploaded_file:
                with st.spinner("Reading PDF..."):
                    text = load_pdf(uploaded_file)
                    entities = extract_entities(text, uploaded_file.name)
                    relations = extract_relations(text, entities)
                    n_e, n_r = build_graph(text, uploaded_file.name, entities, relations)
                    st.markdown(f'<div class="success-box">✅ Extracted <b>{n_e} entities</b> and <b>{n_r} relationships</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ Please upload a PDF</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🗑️ Clear Graph"):
            client = Neo4jClient()
            client.clear_graph()
            client.close()
            st.success("Graph cleared!")

# TAB 2
with tab2:
    st.markdown('<div class="section-label">Query Your Knowledge Graph</div>', unsafe_allow_html=True)
    with st.expander("How to use", expanded=False):
        st.markdown("""
        <div class="step-card"><span class="step-number">01 &nbsp;</span> Ingest at least one source first</div>
        <div class="step-card"><span class="step-number">02 &nbsp;</span> Type a natural language question</div>
        <div class="step-card"><span class="step-number">03 &nbsp;</span> GraphMind traverses the graph and returns cited answers</div>
        <div class="step-card"><span class="step-number">Tip &nbsp;</span> Ask "What connects X to Y?" for multi-hop answers</div>
        """, unsafe_allow_html=True)

    question = st.text_input("", placeholder="What connects Albert Einstein to modern physics?", label_visibility="collapsed")
    if st.button("🔍 Ask GraphMind"):
        if question:
            with st.spinner("Traversing knowledge graph..."):
                answer = query_graph(question)
                st.markdown('<div class="section-label">Answer</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ Please enter a question</div>', unsafe_allow_html=True)

# TAB 3
with tab3:
    st.markdown('<div class="section-label">Interactive Graph</div>', unsafe_allow_html=True)
    with st.expander("How to use", expanded=False):
        st.markdown("""
        <div class="step-card"><span class="step-number">Interact &nbsp;</span> Drag nodes, zoom, hover edges for relationship labels</div>
        <div class="step-card"><span class="step-number">Colors &nbsp;</span> Blue = primary entities &nbsp;|&nbsp; Green = connected &nbsp;|&nbsp; Purple = concepts</div>
        <div class="step-card"><span class="step-number">Tip &nbsp;</span> Ingest multiple sources to see cross-source connections</div>
        """, unsafe_allow_html=True)

    if st.button("🕸️ Load Graph"):
        with st.spinner("Loading..."):
            data = get_graph_for_visualization()
            if not data:
                st.markdown('<div class="warning-box">⚠️ No graph data. Ingest a source first.</div>', unsafe_allow_html=True)
            else:
                net = Network(height="680px", width="100%", bgcolor="#FFFFFF", font_color="#1E293B")
                net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=180)

                added_nodes = set()
                for record in data:
                    src, tgt, rel = record["source"], record["target"], record["relation"]
                    if src not in added_nodes:
                        net.add_node(src, label=src, color="#2563EB", size=22, font={"size": 13, "color": "#FFFFFF"}, borderWidth=2)
                        added_nodes.add(src)
                    if tgt not in added_nodes:
                        net.add_node(tgt, label=tgt, color="#059669", size=16, font={"size": 11, "color": "#FFFFFF"}, borderWidth=1)
                        added_nodes.add(tgt)
                    net.add_edge(src, tgt, title=rel, label=rel, color="#CBD5E1", width=1.5, font={"size": 9, "color": "#64748B"})

                net.set_options("""{"physics":{"enabled":true,"stabilization":{"iterations":80}},"interaction":{"hover":true,"navigationButtons":true,"keyboard":true}}""")
                net.save_graph("graph_viz.html")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<div class="metric-card"><div class="metric-number">{len(added_nodes)}</div><div class="metric-label">Entities</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-card"><div class="metric-number">{len(data)}</div><div class="metric-label">Relationships</div></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="metric-card"><div class="metric-number">{len(set(r["source"] for r in data))}</div><div class="metric-label">Source Nodes</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                with open("graph_viz.html", "r") as f:
                    html = f.read()
                components.html(html, height=680, scrolling=False)

# TAB 4
with tab4:
    st.markdown('<div class="section-label">Contradiction Detector</div>', unsafe_allow_html=True)
    with st.expander("How this works", expanded=False):
        st.markdown("""
        <div class="step-card"><span class="step-number">What it does &nbsp;</span> Finds where two sources describe the same entities differently</div>
        <div class="step-card"><span class="step-number">How to use &nbsp;</span> Ingest 2+ sources on the same topic, then scan</div>
        <div class="step-card"><span class="step-number">Example &nbsp;</span> Source A: "Einstein invented X" vs Source B: "Einstein discovered X"</div>
        """, unsafe_allow_html=True)

    if st.button("🔍 Scan for Contradictions"):
        with st.spinner("Scanning..."):
            contradictions = get_contradictions()
            if not contradictions:
                st.markdown('<div class="success-box">✅ No contradictions found across your sources.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"Found **{len(contradictions)}** contradiction(s):")
                for c in contradictions:
                    st.markdown(f'<div class="error-box">⚡ <b>{c["entity1"]}</b> ↔ <b>{c["entity2"]}</b><br>Source 1: <code>{c["relation1"]}</code> ({c["source1"]})<br>Source 2: <code>{c["relation2"]}</code> ({c["source2"]})</div>', unsafe_allow_html=True)

# TAB 5
with tab5:
    st.markdown('<div class="section-label">Study Mode</div>', unsafe_allow_html=True)
    with st.expander("How this works", expanded=False):
        st.markdown("""
        <div class="step-card"><span class="step-number">What it does &nbsp;</span> Generates quiz questions from your knowledge graph</div>
        <div class="step-card"><span class="step-number">How to use &nbsp;</span> Ingest a source, then generate questions</div>
        <div class="step-card"><span class="step-number">Tip &nbsp;</span> Try to answer before expanding to reveal the answer</div>
        """, unsafe_allow_html=True)

    if st.button("🎯 Generate Quiz"):
        with st.spinner("Generating..."):
            questions = get_quiz_questions()
            if not questions:
                st.markdown('<div class="warning-box">⚠️ No data. Ingest a source first.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"**{len(questions)} questions generated:**")
                for i, q in enumerate(questions):
                    with st.expander(f"Q{i+1} — What connects **{q['from_entity']}** to **{q['to_entity']}**?"):
                        st.markdown(f'<div class="success-box">✅ <b>{q["from_entity"]}</b> <span style="color:#94A3B8">──[</span><b style="color:#2563EB">{q["relation"]}</b><span style="color:#94A3B8">]──▶</span> <b>{q["to_entity"]}</b></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#CBD5E1;font-size:0.75rem;">GraphMind · Neo4j AuraDB · LLaMA 3.3 70B · Groq · Streamlit</div>', unsafe_allow_html=True)