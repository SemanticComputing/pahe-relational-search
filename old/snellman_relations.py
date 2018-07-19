from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests


#Currently not implementing people to people relations

rel = Namespace('http://ldf.fi/relsearch/')


def letter_place_relations(g):
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX snell: <http://ldf.fi/snellman/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rel: <http://ldf.fi/relsearch/>


    SELECT DISTINCT ?letter ?docname ?person ?name ?place ?placename ?source ?date ?nbfPerson ?nbfPlace ?relPlace
    WHERE {
    ?person a foaf:Person .
    ?person snell:nbf ?nbfPerson .
    ?person skos:prefLabel ?name .
    ?kirjeenvaihto a snell:Correspondence .
    ?letter dc:relation ?kirjeenvaihto .
    ?letter dc:creator ?person .
    ?letter snell:writtenIn ?place .
    ?place snell:nbf ?nbfPlace .
    ?letter skos:prefLabel ?docname .
    ?place skos:prefLabel ?placename .
    ?relPlace a rel:Place .
    ?relPlace skos:prefLabel ?placename .
    ?letter dc:source ?source .
    ?letter dc:date ?date .
    }
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 15000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['letter_written_rel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.relationType, rel.letterSentFrom))
        g.add((resource_uri, rel.personSubject, URIRef(row['nbfPerson']['value'])))
        g.add((resource_uri, rel.placeObject, URIRef(row['relPlace']['value'])))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "Henkilö {0} on lähettänyt kirjeen paikasta {1} päivämääränä {2}.".format(row['name']['value'],
                                                                                      row['placename']['value'],
                                                                                      row['date']['value']))))
        g.add((resource_uri, rel.sourceLink, URIRef(row['source']['value'])))
        g.add((resource_uri, rel.source, Literal('J. V. Snellmanin kootut teokset', lang='fi')))
        g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
        x = x + 1


def received_letter_place(g):
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX snell: <http://ldf.fi/snellman/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rel: <http://ldf.fi/relsearch/>

    SELECT DISTINCT ?letter ?docname ?person ?name ?place ?placename ?source ?date ?nbfPerson ?nbfPlace ?relPlace
    WHERE {
    ?person a foaf:Person .
    ?person snell:nbf ?nbfPerson .
    ?person skos:prefLabel ?name .
    ?kirjeenvaihto a snell:Correspondence .
    ?letter dc:relation ?kirjeenvaihto .
    ?kirjeenvaihto snell:correspondent ?person .
    ?letter dc:creator ?creator .
    ?letter snell:writtenIn ?place .
    ?place snell:nbf ?nbfPlace .
    ?letter skos:prefLabel ?docname .
    ?place skos:prefLabel ?placename .
    ?relPlace a rel:Place .
    ?relPlace skos:prefLabel ?placename .
    ?letter dc:source ?source .
    ?letter dc:date ?date .
    FILTER(?creator = <http://ldf.fi/snellman/1>) 
    }
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 1000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['received_letter_rel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.relationType, rel.letterReceivedFrom))
        g.add((resource_uri, rel.personSubject, URIRef(row['nbfPerson']['value'])))
        g.add((resource_uri, rel.placeObject, URIRef(row['relPlace']['value'])))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "Henkilö {0} on vastaanottanut päivämääränä {2} kirjoitetun kirjeen J. V. Snellmanilta paikasta {1}.".format(
                row['name']['value'],
                row['placename']['value'],
                row['date']['value']))))
        g.add((resource_uri, rel.sourceLink, URIRef(row['source']['value'])))
        g.add((resource_uri, rel.source, Literal('J. V. Snellmanin kootut teokset', lang='fi')))
        g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
        x = x + 1

def snellman_received_from(g):
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX snell: <http://ldf.fi/snellman/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rel: <http://ldf.fi/relsearch/>

    SELECT DISTINCT ?letter ?docname ?person ?name ?place ?placename ?source ?date ?nbfPerson ?nbfPlace ?relPlace
    WHERE {
    ?person a foaf:Person .
    ?person snell:nbf ?nbfPerson .
    ?person skos:prefLabel ?name .
    ?kirjeenvaihto a snell:Correspondence .
    ?letter dc:relation ?kirjeenvaihto .
    ?kirjeenvaihto snell:correspondent ?person .
    ?letter dc:creator ?creator .
    ?letter snell:writtenIn ?place .
    ?place snell:nbf ?nbfPlace .
    ?letter skos:prefLabel ?docname .
    ?place skos:prefLabel ?placename .
    ?relPlace a rel:Place .
    ?relPlace skos:prefLabel ?placename .
    ?letter dc:source ?source .
    ?letter dc:date ?date .
    FILTER(?creator != <http://ldf.fi/snellman/1>)
    }
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 1000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['received_letter_snell_rel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.relationType, rel.letterReceivedFrom))
        g.add((resource_uri, rel.personSubject, URIRef('http://ldf.fi/nbf/p996')))
        g.add((resource_uri, rel.placeObject, URIRef(row['relPlace']['value'])))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "J. V. Snellman on vastaanottanut päivämääränä {1} kirjoitetun kirjeen paikasta {0}.".format(
                row['placename']['value'],
                row['date']['value']))))
        g.add((resource_uri, rel.source, URIRef(row['source']['value'])))
        g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
        x = x + 1


# not moved to new place ontology!!!!

def people_in_letter_relations(g):
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX snell: <http://ldf.fi/snellman/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?sender ?senderLabel ?person ?name ?source ?date ?nbfSender ?nbfPerson
    WHERE {
    ?person a foaf:Person .
    ?person snell:nbf ?nbfPerson .
    ?person skos:prefLabel ?name .
    ?kirjeenvaihto a snell:Correspondence .
    ?letter dc:relation ?kirjeenvaihto .
    ?letter dc:creator ?sender .
    ?sender snell:nbf ?nbfSender .
    ?letter dc:relation ?person .
    ?letter skos:prefLabel ?docname .
    ?letter dc:source ?source .
    ?letter dc:date ?date .
    ?sender skos:prefLabel ?senderLabel .
    FILTER(?sender != ?person) .
    }
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    x = 1000
    for row in response.json()['results']['bindings']:
        resource_uri = rel['person_mentioned_rel{}'.format(x)]
        g.add((resource_uri, namespace.RDF.type, rel.Relation))
        g.add((resource_uri, rel.relationType, rel.mentionedInLetter))
        g.add((resource_uri, rel.personSubject, URIRef(row['nbfSender']['value'])))
        g.add((resource_uri, rel.personObject, URIRef(row['nbfPerson']['value'])))
        g.add((resource_uri, namespace.RDFS.comment, Literal(
            "Henkilö {0} on maininnut kirjeessään henkilön {1} päivämääränä {2}.".format(row['senderLabel']['value'],
                                                                                         row['name']['value'],
                                                                                         row['date']['value']))))
        g.add((resource_uri, rel.source, URIRef(row['source']['value'])))
        g.add((resource_uri, rel.date, Literal(row['date']['value'], datatype=XSD.date)))
        x = x + 1




graph = Graph()

letter_place_relations(graph)
snellman_received_from(graph)
received_letter_place(graph)

graph.serialize('relations/snellman_relations.ttl', format='turtle')
