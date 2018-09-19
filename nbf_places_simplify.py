from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv

rel = Namespace('http://ldf.fi/relse/')

def places(g):
    csv_place = csv.reader(open('csv/single_nbf_places.csv', 'r'))
    for row in csv_place:
        g.add((URIRef(row[0].replace('"', '').strip()), namespace.SKOS.prefLabel, Literal(row[1].replace('"', '').strip(), lang = 'fi')))
        g.add((URIRef(row[0].replace('"', '').strip()), namespace.RDF.type, rel.Place))
graph = Graph()
places(graph)
graph.serialize('graphs/simple_placeswith.ttl', format='turtle')

