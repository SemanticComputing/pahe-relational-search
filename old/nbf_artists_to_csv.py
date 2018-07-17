from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests
import re

rel = Namespace('http://ldf.fi/relsearch/')

# needs nbf people.ttl on local server

def arstist_to_csv():
    q = '''
    PREFIX bioc: <http://ldf.fi/schema/bioc/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX occupations: <http://ldf.fi/nbf/occupations/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    
    SELECT DISTINCT ?name ?personConcept
    WHERE {
        ?personConcept foaf:focus ?person .
        ?person a nbf:Person .
        ?person skos:prefLabel ?name .
        ?person bioc:has_profession occupations:taidemaalari .
    }
    ORDER BY ?name
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    artist_file = open('csv/nbf_artists.csv', 'w')

    for row in response.json()['results']['bindings']:
        name = re.sub("[\(].*?[\)]", "", row['name']['value']).strip()
        artist_file.write('"' + name + '","' + row['personConcept']['value'] + '"\n')

    artist_file.close()


# needs relation places on local server

def places_to_csv():
    q = '''
    PREFIX rel: <http://ldf.fi/relsearch/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT DISTINCT ?name ?place
    WHERE {
        ?place a rel:Place .
        ?place skos:prefLabel ?name .
    }
    ORDER BY ?name
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    place_file = open('csv/rel_places.csv', 'w')

    for row in response.json()['results']['bindings']:
        place_file.write('"' + row['name']['value'] + '","' + row['place']['value'] + '"\n')

    place_file.close()

arstist_to_csv()

places_to_csv()
