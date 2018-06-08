from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relsearch/')


def remove_dublicates(g):
    q = '''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?place1 place2
        WHERE { 
        ?place1 skos:prefLabel ?label .
  		?place2 skos:prefLabel ?label .
        FILTER(?place1 != ?place2) .
        }'''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:
        g.remove((URIRef(row[1], None, None)))


graph = Graph()
graph.parse('relations/paikat.ttl', format='turtle')

remove_dublicates(graph)

graph.serialize('relations/corrected_paikat.ttl', format='turtle')