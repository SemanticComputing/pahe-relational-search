import requests

store = 'http://localhost:3030/ds/query'

def death_places():
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX schema: <http://schema.org/>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX gvp: <http://vocab.getty.edu/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rel: <http://ldf.fi/relsearch/>

    CONSTRUCT {
        [ a rel:Relation ;
            rel:relationType rel:deathPlace ;
            rel:personSubject ?person ;
            rel:placeObject ?place ;
            rel:date ?deathtime ] .
    }

    WHERE {
        VALUES ?place_class { schema:Place nbf:Place rel:Place }
        VALUES ?person_class { gvp:PersonConcept foaf:Person }
        ?person a|(a/rdfs:subClassOf+) ?person_class .
        ?death crm:P100_was_death_of/^foaf:focus ?person .
        ?death ?any ?place . # nbf:place!
        ?place a|(a/rdfs:subClassOf+) ?place_class . 
        OPTIONAL {
  	        ?death nbf:time ?dtime . # Not general!
  	        ?dtime gvp:estStart ?deathtime .
        }
        OPTIONAL {
            ?death gvp:estStart ?deathtime .
        }
    }'''

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/raw/nbf_deaths.ttl", "w")

    write_file.write(response.text)

def event_places():
    q ='''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX schema: <http://schema.org/>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX gvp: <http://vocab.getty.edu/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rel: <http://ldf.fi/relsearch/>
    PREFIX bioc: <http://ldf.fi/schema/bioc/> 
    BASE <http://ldf.fi/relsearch/>
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

    CONSTRUCT {
        ?uri a rel:Relation ;
        rel:personSubject ?person ;
        rel:placeObject ?rel_place ;
        rel:date ?date ;
        rel:relationType rel:eventPlace ;
        rel:relationTypeComment ?eClassName ;
        rel:source ?event ;
        skos:prefLabel ?description . 
    }

    WHERE {
  	    VALUES ?place_class { schema:Place nbf:Place rel:Place } 
	    ?event_class rdfs:subClassOf+ schema:Event .
  	    ?event a ?event_class .
  	    ?event bioc:inheres_in ?actor .
  	    ?person foaf:focus ?actor .
  	    ?event skos:prefLabel ?eventLabel .
  	    FILTER (lang(?eventLabel) = 'fi') .
  	    ?event_class skos:prefLabel ?eClassLabel .
        BIND( str(?eClassLabel) as ?eClassName) .
 	    FILTER (lang(?eClassLabel) = 'fi') .
  	    ?place a|(a/rdfs:subClassOf) ?place_class .
  	    ?event ?any ?place .
  	
  	    ?rel_place a rel:Place .
  	    ?rel_place skos:exactMatch ?place .
  	    ?rel_place skos:prefLabel ?placeLabel .
  
	    OPTIONAL {
    	    ?event gvp:estStart ?date .
  	    }
  	    OPTIONAL {
    	    ?event ?hasTime ?time .
    	    ?time gvp:estStart ?date .
        }
  
  
        ?person skosxl:prefLabel ?personLabel .
        ?personLabel skos:prefLabel ?personName .
        ?personLabel schema:familyName ?familyName .
        ?personLabel schema:givenName ?givenName .
  
        BIND(uri(encode_for_uri(concat(str(?personName), str(?placeLabel), str(?eClassLabel), str(?event)))) as ?uri) .
  
        BIND(concat("Henkilön ", str(?givenName), " ", str(?familyName), " elämään liittyy paikassa ", str(?placeLabel), " ", lcase(?eClassName), "-tyyppinen tapahtuma: ", str(?eventLabel)) as ?description)
    }
    '''

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/nbf_events.ttl", "w")

    write_file.write(response.text)

#death_places()

event_places()
