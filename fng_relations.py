import csv
import utilities
import json
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

rel = Namespace('http://ldf.fi/relsearch/')


def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (high + low) // 2
        if values[mid].replace('"', '').strip() == target:
            return mid
        elif target < values[mid].replace('"','').strip():
            high = mid - 1
        else:
            low = mid + 1
    return -1

def find_index(name, list):
    index = binary_search(list, name)
    return index


def get_title(elem):
        for title in elem['title']:
            if 'fi' in title:
                return title['fi']
        return -1


def get_artist(elem, list):
    for row in elem['creator']:
        if 'value' in row:
            artist = row['value']
            index = utilities.find_index(artist, list[0])
            if index != -1:
                artist_uri = list[1][index]
                return artist, artist_uri
    return False

def get_subject(elem, list):
    for row in elem['subject']:
        if 'keyword' in row:
            subject = row['keyword']
            index = utilities.find_index(subject, list[0])
            if index != -1:
                subject_uri = list[1][index]
                print('     ' + subject_uri)  # For testing?


def get_date(elem):
    for row in elem['date']:
        if 'creation' in row:
            date = row['creation']
            return date
        else:
            return 'tuntematon'
    return 'tuntematon'


def get_uri(elem):
    for row in elem['identifier']:
        if 'uri' in row:
            return row['uri']
    return False


def add_place_relations(g, elem, places, artists, x):
    try:
        for row in elem['subject']:
            if 'keyword' in row:
                subject = row['keyword']
                index = find_index(subject, places[0])
                if index != -1 and subject != 'Johannes':   # There is a place called Johannes
                    place_uri = places[1][index]
                    add_painting_depicts_place(g, elem, artists, x, place_uri, subject)
                    x = x + 1
        return x
    except KeyError:
        return x


def add_painting_depicts_place(g, elem, artists, x, place_uri, place_name):
    resource_uri = rel['fng_painting_depicts_place_rel{}'.format(x)]
    if get_artist(elem, artists):
        artist = get_artist(elem, artists)
    else:
        return False
    if get_title(elem) != -1:
        title = get_title(elem)
    else:
        title = '?'
    g.add((resource_uri, namespace.RDF.type, rel.Relation))
    g.add((resource_uri, rel.sourceLink, URIRef(get_uri(elem))))
    g.add((resource_uri, rel.source, URIRef(get_uri(elem))))
    g.add((resource_uri, rel.personSubject, URIRef(artist[1])))
    g.add((resource_uri, rel.placeObject, URIRef(place_uri.replace('"','').strip())))
    g.add((resource_uri, rel.relationType, rel.paintingDepictsPlace))
    g.add((resource_uri, rel.sourceName, Literal("Taulun tiedot Kansallisgallerian tietokannassa", lang='fi')))
    if get_date(elem).isdigit():
        g.add((resource_uri, rel.date, Literal(get_date(elem), datatype=XSD.date)))
        g.add((resource_uri, namespace.SKOS.prefLabel, Literal(
            "Henkilö {0} on luonut vuonna {3} taideteoksen '"'{1}'"', joka kuvaa paikkaa {2}.".format(artist[0], title,
                                                                                           place_name, get_date(elem)))))
    else:
        g.add((resource_uri, namespace.SKOS.prefLabel, Literal(
            "Henkilö {0} on luonut taideteoksen '"'{1}'"', joka kuvaa paikkaa {2}.".format(artist[0], title,
                                                                                           place_name))))


def parse():

    csv_place = csv.reader(open('csv/rel_places.csv', 'r'))
    place_list = utilities.make_list(csv_place)

    csv_art = csv.reader(open('csv/nbf_artists.csv', 'r'))
    artist_list = utilities.make_list(csv_art)

    graph = Graph()

    art_json = open('graphs/fng-data-dc.json', 'r')
    parsed_json = json.load(art_json)
    x = 1000
    for element in parsed_json['descriptionSet']:
        for type in element['type']:
            if 'type' in type:
                if type['type'] == 'artwork':
                    x = add_place_relations(graph, element, place_list, artist_list, x)


    graph.serialize('constructed/fng_depicts_place.ttl', format='turtle')

parse()
