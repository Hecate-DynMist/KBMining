from py2neo import Graph
graph=Graph('http://localhost:7474')

result = graph.run("MATCH (n:ApplyFormat) RETURN n LIMIT 25")
print(result)
