import requests
import csv
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef


def painting_subject_places():

    q = '''
	    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX kaunokki: <http://www.yso.fi/onto/kaunokki#>
        PREFIX saha: <http://seco.tkk.fi/saha3/>
        PREFIX btj: <http://www.btj.fi/>

        SELECT DISTINCT ?writer ?work ?workName ?writername ?placeName ?year
        WHERE {
        ?work a <http://www.yso.fi/onto/kaunokki#romaani> .
        ?work <http://www.yso.fi/onto/kaunokki#worldPlace> ?place .
        ?work <http://www.yso.fi/onto/kaunokki#tekija> ?writer .
  		?work skos:prefLabel ?workName .
        ?work <http://www.yso.fi/onto/kaunokki#manifests_in> ?version .
        ?version <http://www.yso.fi/onto/kaunokki#onEnsimmainenVersio> <http://www.yso.fi/onto/kaunokki#true> .
        ?version <http://www.yso.fi/onto/kaunokki#ilmestymisvuosi> ?date .
        ?date skos:prefLabel ?dateLabel .
        BIND(str(?dateLabel) AS ?year) .
        ?writer skos:prefLabel ?writername .
        ?place skos:prefLabel ?placeName .
        FILTER(lang(?placeName) = 'fi') .
  	    FILTER(lang(?workName) = 'fi') .
        }'''

    response = requests.post('http://ldf.fi/kulttuurisampo/sparql',
                             data={'query': q})

    books_csv = open("csv/kirjasampo_book_places.csv", "w")

    for row in response.json()['results']['bindings']:
        books_csv.write('"' + row['writer']['value'] + '","' + row['work']['value'] + '","' \
                           + row['workName']['value'] + '","'+  row['writername']['value'] + '","' + row['placeName']['value'] + '","' + \
                           row['year']['value'] + '"\n')

    books_csv.close()

painting_subject_places()