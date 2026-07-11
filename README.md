
 GraphMind

Don't search through knowledge. Traverse it.

A Knowledge Graph RAG system that turns raw documents into a living, queryable web of facts — with citations, contradiction detection, and multi-hop reasoning built in.

 Built for HACKHAZARDS '26 · Neo4j Partner Track

Live Demo · Demo Video · Report Bug

</div>

The Problem

Ask a standard RAG chatbot a question that spans two ideas, and watch it fall apart. Feed it two sources that disagree, and it'll confidently hand you whichever chunk scored highest on similarity — with zero warning that a contradiction even exists.

That's because vector-only RAG treats every chunk of text as an island. It has no concept of how facts connect to each other — only how similar they sound.

GraphMind fixes this by making the connections themselves the thing you query.

The Idea

Instead of embedding chunks and hoping similarity search finds the right ones, GraphMind reads your documents, extracts the actual entities and relationships inside them using LLaMA 3.3 70B on Groq, and writes them into a live Neo4j knowledge graph. From there, every question becomes a graph traversal — not a guess.

"How does X relate to Z?"
        ↓
   Standard RAG: searches for chunks that *sound* like the answer
   GraphMind:    finds X → traverses the graph → discovers the path to Z


Features

Multi-source IngestionLoad knowledge straight from URLs or PDFs Entity & Relationship ExtractionLLaMA 3.3 70B (via Groq) turns raw text into structured graph triples in near real-time🗄️ Living Knowledge GraphEvery fact persists in Neo4j AuraDB — queryable, growable, permanent Graph RAG QueryingAsk in plain English, get answers grounded in traversal — not similarity guessesSource CitationsEvery fact in every answer traces back to exactly where it came from Contradiction DetectorTwo sources disagree? GraphMind catches it and tells you Interactive Graph VisualizationExplore the entire knowledge structure visually via PyVis Study ModeAuto-generates quizzes straight from the graph for active recall


Tech Stack

<div align="center">
LayerTechnologyWhyUIStreamlitFast, clean, ships in hours not weeksGraph DatabaseNeo4j AuraDBNative traversal — the graph is the retrieval layerLLM / ExtractionGroq API · LLaMA 3.3 70BFast enough for real-time extraction on ingestionWeb ScrapingBeautifulSoupClean text extraction from arbitrary URLsPDF ParsingPyPDF2Turns documents into ingestible raw textGraph VisualizationPyVisInteractive, in-browser graph exploration

</div>

🏗️ Architecture

                    📄 Input (URL / PDF)
                            │
                            ▼
              ┌──────────────────────────┐
              │        INGESTION          │   web_scraper.py · pdf_loader.py
              └─────────────┬─────────────┘
                            ▼
              ┌──────────────────────────┐
              │  ENTITY + RELATION        │   entity_extractor.py
              │  EXTRACTION (Groq/LLaMA)  │   relation_extractor.py
              └─────────────┬─────────────┘
                            ▼
              ┌──────────────────────────┐
              │   KNOWLEDGE GRAPH          │   neo4j_client.py
              │   (Neo4j AuraDB)           │
              └─────────────┬─────────────┘
                            ▼
              ┌──────────────────────────┐
              │   GRAPH RAG QUERY ENGINE   │   graph_rag.py
              │   (traversal + synthesis)  │
              └─────────────┬─────────────┘
                            ▼
             ✅ Cited Answer + 🕸️ Live Visualization
                      (app.py · Streamlit)


📁 Project Structure

GraphMinds/
├── app.py                       # Streamlit entrypoint
├── config.py                    # Configuration & secrets loading
├── scraper/
│   ├── web_scraper.py           # URL → raw text
│   └── pdf_loader.py            # PDF → raw text
├── extractor/
│   ├── entity_extractor.py      # Text → entities (Groq/LLaMA)
│   └── relation_extractor.py    # Text → relationships (Groq/LLaMA)
└── graph/
    ├── neo4j_client.py          # Neo4j AuraDB connection & queries
    └── graph_rag.py             # Graph traversal + RAG answer generation


🚀 Running Locally

Prerequisites: Python 3.10+, a Neo4j AuraDB instance, a Groq API key

bashgit clone https://github.com/hplaksh687/GraphMind.git
cd GraphMind
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Create a .env file in the project root:

NEO4J_URI=your-neo4j-aura-uri
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password
GROQ_API_KEY=your-groq-key

Run it:

bashstreamlit run app.py


See It In Action

🔗 Live App: (add Streamlit Cloud link)
🎥 Demo Video: (add video link)
📝 Technical Deep-Dive: (add blog link)


What's Next


Entity resolution — normalize surface-form variants ("Neo4j" vs "Neo4j AuraDB") before they fragment the graph
Hybrid retrieval — combine graph traversal with vector similarity for queries where exact entity matching isn't enough
Multi-document reasoning — surface not just contradictions but corroboration across sources



<div align="center">
👤 Team

Laksh H P
B.Tech CSE (AI & ML) · SRM Institute of Science and Technology

GitHub · LinkedIn


Built for HACKHAZARDS '26

Domain: Learning & Knowledge Systems · Partner Track: Neo4j
