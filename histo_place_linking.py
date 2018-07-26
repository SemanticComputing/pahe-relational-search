import csv

# query used to find places
'''
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX schema: <http://schema.org/>
PREFIX relse: <http://ldf.fi/relsearch/>
    
SELECT DISTINCT ?event ?eLabel
WHERE {
  ?event a crm:E5_Event .
  ?event crm:P7_took_place_at ?place .
  ?place rdfs:label ?eLabel
}'''


def places():
    places = csv.reader(open('csv/histo_places.csv', 'r'))
