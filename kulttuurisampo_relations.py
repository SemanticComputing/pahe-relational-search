import requests
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv

rel = Namespace('http://ldf.fi/relsearch/')

def decode(uri):
    uri = uri.replace('%2C', ',')
    uri = uri.replace('%C3%84', 'Ä')
    uri = uri.replace('%C3%A4', 'ä')
    uri = uri.replace('%C3%85', 'Å')
    uri = uri.replace('%C3%A5', 'å')
    uri = uri.replace('%C3%B6', 'ö')
    uri = uri.replace('%C3%96', 'Ö')
    return uri


def painters(g, person):
    person_uri = URIRef(person)
    q = g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX nbf: <http://ldf.fi/nbf/> 
            SELECT ?s
            WHERE { ?s nbf:kulsa ?person . }
            """, initBindings={'person': person_uri})
    if len(list(q)) > 0:
        for row in q:
            return(row[0])
    else:
        return "false"

def places(g, place):
    q = g.query("""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX nbf: <http://ldf.fi/nbf/> 
            
        SELECT DISTINCT ?place ?label
        WHERE {
            ?place a nbf:Place .
            ?place skos:prefLabel ?label .
        }""", initBindings={'label': Literal(place, lang='fi')})
    if len(list(q)) > 0:
        for row in q:
            return(row[0])
    else:
        return "false"


def painting_depicts_relations(read_graph, write_graph):

    subjects = open("csv/subjects_ku_sa.csv", "r")
    lukija = csv.reader(subjects)

    x = 1000
    for row in lukija:
        resource_uri = rel['painting_depicts_place_rel{}'.format(x)]
        painter = painters(read_graph, decode(row[2]))
        if painter != "false":
            place = places(read_graph, row[3])
            if place != "false":
                write_graph.add((resource_uri, namespace.RDF.type, rel.Relation))
                write_graph.add((resource_uri, rel.personSubject, URIRef(painter)))
                write_graph.add((resource_uri, rel.placeObject, URIRef(place)))
                write_graph.add((resource_uri, rel.relationType, rel.paintingDepictsPlace))
                write_graph.add((resource_uri, namespace.RDFS.comment, Literal(
                    "Henkilö {0} on maalannut teoksen '"'{1}'"', joka kuvaa paikkaa {2}.".format(row[5], row[1], row[3]))))
                write_graph.add((resource_uri, rel.source, Literal("Kulttuurisampo", lang='fi')))
                write_graph.add((resource_uri, rel.date, Literal(row[4], datatype=XSD.date)))
                x = x + 1



graph = Graph()
graph.parse('graphs/corrected_kulsa_links.ttl', format='turtle')
graph.parse('NBF/places.ttl', format='turtle')

w_graph = Graph()

painting_depicts_relations(graph, w_graph)

w_graph.serialize('relations/kulttuurisampo_paintings.ttl', format='turtle')