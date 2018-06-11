from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relsearch/')

def generate_places(r_g, w_g):
    q = r_g.query('''
        PREFIX yso: <http://www.yso.fi/onto/yso/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?place1 ?label1
        WHERE { 
	    ?place1 a skos:Concept .
  	    ?place1 skos:inScheme yso:places .
  	    ?place1 skos:prefLabel ?label1 .
  	    FILTER(lang(?label1) = 'fi') .
        }''')

    x=1000
    for row in q:
        place_uri = rel['p{}'.format(x)]
        w_g.add((place_uri, namespace.RDF.type, rel.Place))
        w_g.add((place_uri, namespace.SKOS.prefLabel, row[1]))
        w_g.add((place_uri, namespace.SKOS.exactMatch, row[0]))

        x=x+1


r_graph = Graph()
w_graph = Graph()

r_graph.parse('graphs/yso-paikat-skos.ttl', format='turtle')

generate_places(r_graph, w_graph)

w_graph.serialize('graphs/no_hierarchy_place_ontology.ttl', format='turtle')

#graph1 = Graph()

#first_level_broader(graph1)

#graph1.serialize('graphs/place_ontology1.ttl', format='turtle')

#remove_yso(graph)


