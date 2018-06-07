from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

rel = Namespace('http://ldf.fi/relsearch/')


def death_place_relations(g):
    q = '''
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX dbo: <http://dbpedia.org/ontology/>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX snell: <http://ldf.fi/snellman/>
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	PREFIX place: <http://purl.org/ontology/places/>
	PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
	PREFIX nbf:	<http://ldf.fi/nbf/>
	PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
	PREFIX schema: <http://schema.org/>
	PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
	PREFIX gvp:	<http://vocab.getty.edu/ontology#>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    	SELECT DISTINCT ?nbfperson ?familyName ?firstName ?deathtime ?place ?placeName ?death
    	WHERE { 
        ?nbfperson a nbf:PersonConcept .
        ?nbfperson skosxl:prefLabel ?label .
        ?label schema:familyName ?familyName .
        ?label schema:givenName ?firstName .        
        ?nbfperson foaf:focus ?actor .
        ?death crm:P100_was_death_of ?actor .
        ?death nbf:time ?dtime .
	    ?death nbf:place ?place .
        ?dtime gvp:estStart ?deathtime .
	    ?place skos:prefLabel ?placeName .
  	    FILTER (!isLiteral(?place)) .
  	    FILTER (lang(?placeName) = 'fi')
        }
        '''


    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 1000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['dprel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.personSubject, URIRef(row['nbfperson']['value'])))
        g.add((resource_uri, rel.placeObject, URIRef(row['place']['value'])))
        g.add((resource_uri, rel.relationType, rel.deathPlace))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "Henkilö {0}, {1} on kuollut paikassa {2} päivämääränä {3}.".format(row['familyName']['value'], row['firstName']['value'],
                                                                                      row['placeName']['value'],
                                                                                      row['deathtime']['value']))))
        g.add((resource_uri, rel.source, URIRef(row['death']['value'])))
        g.add((resource_uri, rel.date, Literal(row['deathtime']['value'], datatype=XSD.date)))
        x = x + 1

def birth_place_relations(g):
    q = '''
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX dbo: <http://dbpedia.org/ontology/>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX snell: <http://ldf.fi/snellman/>
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	PREFIX place: <http://purl.org/ontology/places/>
	PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
	PREFIX nbf:	<http://ldf.fi/nbf/>
	PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
	PREFIX schema: <http://schema.org/>
	PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
	PREFIX gvp:	<http://vocab.getty.edu/ontology#>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    	SELECT DISTINCT ?nbfperson ?familyName ?firstName ?birthtime ?place ?placeName ?birth
    	WHERE { 
        ?nbfperson a nbf:PersonConcept .
        ?nbfperson skosxl:prefLabel ?label .
        ?label schema:familyName ?familyName .
        ?label schema:givenName ?firstName .        
        ?nbfperson foaf:focus ?actor .
        ?birth crm:P98_brought_into_life ?actor .
        ?birth nbf:time ?btime .
	    ?birth nbf:place ?place .
        ?btime gvp:estStart ?birthtime .
	    ?place skos:prefLabel ?placeName .
  	    FILTER (!isLiteral(?place)) .
  	    FILTER (lang(?placeName) = 'fi')
        }
        '''


    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 1000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['bprel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.relationType, rel.birthPlace))
        g.add((resource_uri, rel.personSubject, URIRef(row['nbfperson']['value'])))
        g.add((resource_uri, rel.placeObject, URIRef(row['place']['value'])))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "Henkilö {0}, {1} on syntynyt paikassa {2} päivämääränä {3}.".format(row['familyName']['value'], row['firstName']['value'],
                                                                                      row['placeName']['value'],
                                                                                      row['birthtime']['value']))))
        g.add((resource_uri, rel.source, URIRef(row['birth']['value'])))
        g.add((resource_uri, rel.date, Literal(row['birthtime']['value'], datatype=XSD.date)))
        x = x + 1



graph = Graph()

birth_place_relations(graph)
death_place_relations(graph)


graph.serialize('relations/nbf_life_relations.ttl', format='turtle')
