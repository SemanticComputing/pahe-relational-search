from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relsearch/')

def first_level_broader(g):
    q = '''
        PREFIX yso: <http://www.yso.fi/onto/yso/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rel: <http://ldf.fi/relsearch/>

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


def ares_given_to_ussr(g):
    q = '''
            PREFIX yso: <http://www.yso.fi/onto/yso/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

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


def move_old_towns(g):
    q = '''
            PREFIX yso: <http://www.yso.fi/onto/yso/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

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

    for row in response.json()['results']['bindings']:
        if row['note']['value'] == "Neuvostoliitolle luovutetun alueen kunta" or \
                row['note']['value'] == "Neuvostoliitolle luovutetun alueen kaupunki":
            g.add((URIRef(row['relPlace']['value']), namespace.SKOS.broader, rel.p_luovutetut_alueet))


graph = Graph()

graph.parse('graphs/no_hierarchy_place_ontology.ttl', format='turtle')

first_level_broader(graph)

ares_given_to_ussr(graph)

graph.serialize('graphs/place_ontology3.ttl', format='turtle')