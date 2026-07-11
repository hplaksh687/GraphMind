from groq import Groq
from graph.neo4j_client import Neo4jClient
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def build_graph(text: str, source: str, entities: list, relations: list):
    db = Neo4jClient()
    for entity in entities:
        db.create_entity(
            name=entity["name"],
            entity_type=entity.get("type", "Unknown"),
            source=source
        )
    for rel in relations:
        db.create_relationship(
            from_entity=rel["from"],
            to_entity=rel["to"],
            relation=rel["relation"],
            source=source
        )
    db.close()
    return len(entities), len(relations)

def query_graph(question: str) -> str:
    db = Neo4jClient()
    graph_data = db.get_all_graph_data()
    db.close()
    if not graph_data:
        return "No knowledge graph found. Please ingest a source first."
    context_lines = []
    for record in graph_data[:80]:
        context_lines.append(
            f"{record['source']} --[{record['relation']}]--> {record['target']}"
        )
    context = "\n".join(context_lines)
    prompt = f"""You are GraphMind, an AI that answers questions using a knowledge graph.
Here is the knowledge graph context:
{context}
Answer this question using the knowledge graph above.
Cite which connections you used.
Question: {question}"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def get_graph_for_visualization():
    db = Neo4jClient()
    data = db.get_all_graph_data()
    db.close()
    return data

def get_contradictions():
    db = Neo4jClient()
    data = db.find_contradictions()
    db.close()
    return data

def get_quiz_questions():
    db = Neo4jClient()
    data = db.generate_quiz()
    db.close()
    return data