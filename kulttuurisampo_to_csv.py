import requests
import csv
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef


def painting_subject_places():

    q = '''
	PREFIX kirjasampo: <http://www.yso.fi/onto/kaunokki#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX cido: <http://www8.informatik.uni-erlangen.de/IMMD8/Services/cidoc-crm/erlangen-crm_090330_5_0_1_TQ.owl#>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?painting ?name_of_painting ?painter ?place ?label ?date ?painter_name
    WHERE { 		
    ?painting a <http://www.muusa.fi/rdf/class_p%C3%A4%C3%A4luokka_maalaus> .
    ?painting cido:property_production_property_taiteilija ?painter .
    ?painter skos:prefLabel ?painter_name .
    ?painting cido:P129.is_about ?subject .
    ?painting skos:prefLabel ?name_of_painting .
    ?subject rdfs:label ?label .
    ?place a cido:E53.Place .
    ?place rdfs:label ?label .
    ?painting cido:property_production_P4.has_time-span ?time .
    ?time <http://www.yso.fi/onto/time-schema#earliestStart> ?date .
    FILTER(lang(?name_of_painting) = 'fi')
    }'''

    response = requests.post('http://ldf.fi/kulttuurisampo/sparql',
                             data={'query': q})

    subjects_csv = open("csv/subjects_ku_sa.csv", "w")

    for row in response.json()['results']['bindings']:
        subjects_csv.write('"' + row['painting']['value'] + '","' + row['name_of_painting']['value'] + '","' \
                           + row['painter']['value'] + '","'+  row['label']['value'] + '","' + row['date']['value'] + '","' + \
                           row['painter_name']['value'] + '"\n')

    subjects_csv.close()

#subjects = open("csv/subjects_ku_sa.csv", "r")
#lukija = csv.reader(subjects)

#for row in lukija:
#    print(row[4].split('-')[0])

def nbf_places(g):
    q = g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX nbf: <http://ldf.fi/nbf/> 
            SELECT ?place ?place_name
            WHERE { 
                ?place a nbf:Place .
                ?place skos:prefLabel ?label .
                FILTER(lang(?label) = 'fi') .
                BIND(str(?label) AS ?place_name) .
                }
            """)
    if len(list(q)) > 0:
        with open('csv/nbf_places.csv','w') as places:
            for row in q:
                places.write('"' + row[0] + '","' + row[1] + '"\n')

graph = Graph()
graph.parse('NBF/places.ttl', format='turtle')

painting_subject_places()
nbf_places(graph)