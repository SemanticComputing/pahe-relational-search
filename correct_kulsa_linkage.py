from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

nbf = Namespace('http://ldf.fi/nbf/')

def remove_wrong(g):
    q = '''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX nbf:	<http://ldf.fi/nbf/>
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

        SELECT ?nbf ?kulsa ?prefLabel
        WHERE { 
          ?nbf nbf:kulsa ?kulsa . 
          ?nbf skosxl:prefLabel ?label .
          ?label skos:prefLabel ?prefLabel .
        }
        '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['nbf']['value']), nbf.kulsa, URIRef(row['kulsa']['value'])))

graph = Graph()

remove_wrong(graph)

graph.serialize('graphs/corrected_kulsa_links.ttl', format='turtle')
