import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from self_improving_agent.memory.database import get_connection
import graphqlite

conn = get_connection()
db = graphqlite.wrap(conn)

print("Testing MERGE with SET...")
db.cypher("MERGE (n {id: 42}) SET n:SetNode, n.name = 'test'")
res = list(db.cypher("MATCH (n:SetNode) RETURN n"))
print("MERGE SET result:", res)
print("Result for 3092:", res)

print("\nListing all edges:")
res_all = list(db.cypher("MATCH (a)-[r:PRODUCES_LESSON]->(b) RETURN a, b LIMIT 3"))
print("Edges:", res_all)

# Look for any nodes
res_nodes = list(db.cypher("MATCH (l:Lesson) RETURN l LIMIT 3"))
print("Lesson nodes:", res_nodes)

print("\nAll nodes:")
res_all_nodes = list(db.cypher("MATCH (n) RETURN n LIMIT 3"))
print("All nodes:", res_all_nodes)
