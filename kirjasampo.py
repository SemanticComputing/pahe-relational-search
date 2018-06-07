import csv
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

rel = Namespace('http://ldf.fi/relsearch/')


def writers(g, person):
    person_uri = URIRef(person)
    q = g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX nbf: <http://ldf.fi/nbf/> 
            SELECT ?s
            WHERE { ?s nbf:kirjasampo ?person . }
            """, initBindings={'person': person_uri})
    if len(list(q)) > 0:
        for row in q:
            return row[0]
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
            return row[0]
    else:
        return "false"

def check_dublicates(g, person, place, book):
    book_uri = URIRef(book)
    q = g.query("""
        PREFIX rel: <http://ldf.fi/relsearch/>

        SELECT DISTINCT ?relation
        WHERE {
            ?relation a rel:Relation .
            ?relation rel:placeObject ?place .
            ?relation rel:personSubject ?person .
            ?relation rel:sourceLink ?book .
        }""", initBindings={'person': person, 'place': place, 'book': book_uri})
    if len(list(q)) > 0:
        return True
    else:
        return False


def book_depicts_place(read_graph, write_graph):

    #links = open("csv/corrected_kirjasampo.csv", "r")
    books = open("csv/kirjasampo_book_places.csv", "r")
    #link_reader = csv.reader(links)
    book_reader = csv.reader(books)



    x = 1000
    for row in book_reader:
        resource_uri = rel['novel_depicts_place_rel{}'.format(x)]
        writer = writers(read_graph, row[0])
        if writer != "false":
            place = places(read_graph, row[4])
            if place != "false" and not check_dublicates(write_graph, writer, place, row[1]):
                split_name = row[3].split(',')
                writer_name = split_name[1].strip() + ' ' + split_name[0].strip()
                write_graph.add((resource_uri, namespace.RDF.type, rel.Relation))
                write_graph.add((resource_uri, rel.personSubject, URIRef(writer)))
                write_graph.add((resource_uri, rel.placeObject, URIRef(place)))
                write_graph.add((resource_uri, rel.relationType, rel.novelDepictsPlace))
                write_graph.add((resource_uri, namespace.RDFS.comment, Literal(
                    "{0} on kirjoittanut romaanin '"'{1}'"', joka kuvaa paikkaa {2}.".format(writer_name, row[2],
                                                                                                 row[4]))))
                write_graph.add((resource_uri, rel.source, Literal("Kirjasampo", lang='fi')))
                write_graph.add((resource_uri, rel.sourceLink, URIRef(row[1])))
                write_graph.add((resource_uri, rel.date, Literal(row[5], datatype=XSD.date)))
                x = x + 1

graph = Graph()
graph.parse('graphs/corrected_kirjasampo_linkage.ttl', format='turtle')
graph.parse('NBF/places.ttl', format='turtle')

write_graph = Graph()

book_depicts_place(graph, write_graph)

write_graph.serialize('kirjasampo_books_depict_place.ttl', format='turtle')