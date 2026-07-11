from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv(override=True)

NEO4J_URI = os.environ.get("NEO4J_URI", "").strip()
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "").strip()
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "").strip()

class Neo4jClient:
    def __init__(self):
        uri = str(NEO4J_URI).strip()
        username = str(NEO4J_USERNAME).strip()
        password = str(NEO4J_PASSWORD).strip()
        self.driver = GraphDatabase.driver(
            uri, auth=(username, password)
        )

    def close(self):
        self.driver.close()

    def create_entity(self, name: str, entity_type: str, source: str):
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entity {name: $name})
                SET e.type = $type, e.source = $source
            """, name=name, type=entity_type, source=source)

    def create_relationship(self, from_entity: str, to_entity: str, relation: str, source: str):
        with self.driver.session() as session:
            session.run("""
                MERGE (a:Entity {name: $from_entity})
                MERGE (b:Entity {name: $to_entity})
                MERGE (a)-[r:RELATES_TO {type: $relation, source: $source}]->(b)
            """, from_entity=from_entity, to_entity=to_entity,
                relation=relation, source=source)

    def get_all_graph_data(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
                RETURN a.name AS source, r.type AS relation, b.name AS target
            """)
            return [dict(record) for record in result]

    def find_contradictions(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Entity)-[r1:RELATES_TO]->(b:Entity)
                MATCH (a)-[r2:RELATES_TO]->(b)
                WHERE r1.source <> r2.source AND r1.type <> r2.type
                RETURN a.name AS entity1, b.name AS entity2,
                       r1.type AS relation1, r1.source AS source1,
                       r2.type AS relation2, r2.source AS source2
            """)
            return [dict(record) for record in result]

    def generate_quiz(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
                RETURN a.name AS from_entity, r.type AS relation, b.name AS to_entity
                LIMIT 5
            """)
            return [dict(record) for record in result]

    def clear_graph(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")