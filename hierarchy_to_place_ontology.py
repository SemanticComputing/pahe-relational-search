from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relse/')

def first_level_broader(g):
    q = '''
        PREFIX yso: <http://www.yso.fi/onto/yso/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rel: <http://ldf.fi/relse/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?relPlace ?broaderPlace
        WHERE { 
	    ?place1 a skos:Concept .
  	    ?place1 skos:inScheme yso:places .
  	    ?relPlace a rel:Place .
  	    ?place1 skos:broader ?place2 .
  	    ?relPlace skos:exactMatch ?place1 .
  	    ?broaderPlace skos:exactMatch ?place2 .	    
        }'''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['relPlace']['value']), namespace.SKOS.broader, URIRef(row['broaderPlace']['value'])))


def areas_given_to_ussr(g):
    q = '''
            PREFIX yso: <http://www.yso.fi/onto/yso/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT ?relPlace ?note
            WHERE {
            ?place1 a skos:Concept .
            ?place1 skos:inScheme yso:places .
            ?place1 skos:note ?note .
            ?relPlace skos:exactMatch ?place1 .
            FILTER(lang(?note) = 'fi') .
            }'''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    g.add((rel.p_luovutetut_alueet, namespace.RDF.type, rel.Place))
    g.add((rel.p_luovutetut_alueet, namespace.SKOS.prefLabel, Literal("Neuvostoliitolle luovutetut alueet")))

    for row in response.json()['results']['bindings']:
        if  "Neuvostoliitolle luovutetun alueen" in row['note']['value'] or \
                "luovutetulle alueelle" in row['note']['value']:
            g.add((URIRef(row['relPlace']['value']), namespace.SKOS.broader, rel.p_luovutetut_alueet))

def linkage(g):
    q = '''
        PREFIX yso: <http://www.yso.fi/onto/yso/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX nbf:	<http://ldf.fi/nbf/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        SELECT DISTINCT ?relPlace ?match ?nbf_place
        WHERE { 
	    ?place1 a skos:Concept .
  	    ?place1 skos:inScheme yso:places .
  		?relPlace skos:exactMatch ?place1 .
  		?place1 skos:closeMatch ?match .
  		?place1 skos:prefLabel ?label .
  		?nbf_place a nbf:Place .
  	    ?nbf_place skos:prefLabel ?label .
        }'''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:
        try:
            g.add((URIRef(row['relPlace']['value']), namespace.SKOS.closeMatch, URIRef(row['match']['value'])))
        except:
            pass
        try:
            g.add((URIRef(row['relPlace']['value']), namespace.SKOS.closeMatch, URIRef(row['nbf_place']['value'])))
        except:
            pass


graph = Graph()

graph.parse('graphs/no_hierarchy_place_ontology.ttl', format='turtle')

first_level_broader(graph)

areas_given_to_ussr(graph)

linkage(graph)

graph.serialize('graphs/place_ontology.ttl', format='turtle')
