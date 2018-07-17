import requests

def link_people():
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX schema: <http://schema.org/>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX gvp: <http://vocab.getty.edu/ontology#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX snellman: <http://ldf.fi/snellman/> 

    CONSTRUCT {
        ?person skos:exactMatch ?snell_person .
        }
    WHERE {
  	    ?snell_person a foaf:Person .
  	    ?snell_person snellman:birthYear ?snell_b_year .
  	    ?snell_person foaf:givenName ?snell_given_name .
  	    ?snell_person foaf:familyName ?snell_family_name .
  	    ?person a nbf:PersonConcept .
  	    ?person schema:relatedLink ?link .
  	    ?person skos:prefLabel ?prefLabel .
  	    ?person skosxl:prefLabel ?label .
  	    ?label schema:familyName ?familyName .
  	    ?label schema:givenName ?givenName .
  	    ?person foaf:focus ?actor .
  	    ?birth crm:P98_brought_into_life ?actor .
  	    ?birth nbf:time ?time .
  	    ?time gvp:estStart ?bdate .
  	    BIND(year(?bdate) as ?byear ) .
  	    FILTER (?snell_given_name = ?givenName) .
  	    FILTER (?snell_family_name = ?familyName) .
  	    FILTER (?snell_b_year = ?byear) .
        }
    '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    linkage_file = open("graphs/snellman_nbf_people.ttl", "w")

    linkage_file.write(response.text)

link_people()