from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
rel = Namespace('http://ldf.fi/relsearch/')
import requests

def career_places(g):
    q = """
            PREFIX nbf:	<http://ldf.fi/nbf/>
            PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
            PREFIX bioc: <http://ldf.fi/schema/bioc/>
            PREFIX schema: <http://schema.org/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX gvp:	<http://vocab.getty.edu/ontology#>

            SELECT DISTINCT ?person ?place ?placeName ?eventLabel ?familyName ?firstName ?place ?date ?event
            WHERE {
                ?person a nbf:PersonConcept .
                ?person skosxl:prefLabel ?label .
                ?label schema:familyName ?familyName .
                ?label schema:givenName ?firstName . 
                ?person foaf:focus ?actor .
                ?event bioc:inheres_in ?actor .
                ?event skos:prefLabel ?eventLabel .
                ?event nbf:place ?place .
                ?place skos:prefLabel ?placeName .
                ?event a nbf:Career .
                ?event nbf:time ?time .
                ?time gvp:estStart ?date .
                FILTER(lang(?placeName) = 'fi') .
            }
            """
    x=1000
    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:

        if not row['placeName']['value'] == 'Suomen leijona':

            resource_uri = rel['career_place_rel{}'.format(x)]
            g.add((resource_uri, namespace.RDF.type, rel.Relation))
            g.add((resource_uri, rel.personSubject, URIRef(row['person']['value'])))
            g.add((resource_uri, rel.placeObject, URIRef(row['place']['value'])))
            g.add((resource_uri, rel.relationType, rel.careerAtPlace))
            g.add((resource_uri, namespace.RDFS.comment, Literal(
                "Henkilön {0}, {1} uraan tai opiskeluun liittyi paikassa {3} tapahtuma: {2}.".format(row['familyName']['value'],
                                                                        row['firstName']['value'],
                                                                        row['eventLabel']['value'],
                                                                        row['placeName']['value']))))
            g.add((resource_uri, rel.source, URIRef(row['event']['value'])))
            g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
            x = x + 1

def honours(g):
    q = """
            PREFIX nbf:	<http://ldf.fi/nbf/>
            PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
            PREFIX bioc: <http://ldf.fi/schema/bioc/>
            PREFIX schema: <http://schema.org/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX gvp:	<http://vocab.getty.edu/ontology#>

            SELECT DISTINCT ?person ?place ?placeName ?eventLabel ?familyName ?firstName ?place ?date ?event
            WHERE {
                ?person a nbf:PersonConcept .
                ?person skosxl:prefLabel ?label .
                ?label schema:familyName ?familyName .
                ?label schema:givenName ?firstName . 
                ?person foaf:focus ?actor .
                ?event bioc:inheres_in ?actor .
                ?event skos:prefLabel ?eventLabel .
                ?event nbf:place ?place .
                ?place skos:prefLabel ?placeName .
                ?event a nbf:Honour .
                ?event nbf:time ?time .
                ?time gvp:estStart ?date .
                FILTER(lang(?placeName) = 'fi') .
            }
            """
    x=1000
    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    for row in response.json()['results']['bindings']:
        if not row['placeName']['value'] == 'Suomen leijona':

            resource_uri = rel['honour_place_rel{}'.format(x)]
            g.add((resource_uri, namespace.RDF.type, rel.Relation))
            g.add((resource_uri, rel.personSubject, URIRef(row['person']['value'])))
            g.add((resource_uri, rel.placeObject, URIRef(row['place']['value'])))
            g.add((resource_uri, rel.relationType, rel.honourAtPlace))
            g.add((resource_uri, namespace.RDFS.comment, Literal(
                "Henkilö {0}, {1} on vastaanottanut kunnianosoituksen: {2}.".format(row['familyName']['value'],
                                                                        row['firstName']['value'],
                                                                        row['eventLabel']['value']))))
            g.add((resource_uri, rel.source, URIRef(row['event']['value'])))
            g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
            x = x + 1


graph = Graph()

career_places(graph)
honours(graph)

graph.serialize('relations/careers_to_places.ttl', format='turtle')