from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relsearch/')

# need nbf-places and yso-places

def create_places_from_nbf(g):
    q = '''
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
            PREFIX yso: <http://www.yso.fi/onto/yso> 
            PREFIX nbf:	<http://ldf.fi/nbf/>
            
            SELECT DISTINCT ?label ?ysoPlace ?nbfplace 
            WHERE {
            ?nbfplace a nbf:Place .
            ?nbfplace skos:prefLabel ?label .
            ?ysoPlace a skos:Concept .
            ?ysoPlace skos:prefLabel ?label .
            }
            '''
    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x=1000

    for row in response.json()['results']['bindings']:
        place_uri = rel['place{}'.format(x)]
        g.add((place_uri, namespace.RDF.type, rel.Place))
        g.add((place_uri, namespace.SKOS.prefLabel, Literal(row['label']['value'], lang='fi')))
        g.add((place_uri, namespace.OWL.sameAs, URIRef(row['ysoPlace']['value'])))
        g.add((place_uri, namespace.SKOS.exactMatch, URIRef(row['nbfplace']['value'])))

        x=x+1

def remove_dublicates(g):
    q = g.query('''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        SELECT DISTINCT ?place1 ?place2
        WHERE { 
        ?place1 skos:prefLabel ?label .
  		?place2 skos:prefLabel ?label .
        FILTER(?place1 != ?place2) .
        }''')

    for row in q:
        g.remove((URIRef(row[1]), None, None))


graph = Graph()

create_places_from_nbf(graph)
remove_dublicates(graph)

graph.serialize('relations/paikat.ttl', format='turtle')

