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
    	BASE <http://ldf.fi/relsearch/>
    	PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

        CONSTRUCT {
            ?uri a rel:Relation ;
                rel:relationType rel:deathPlace ;
                rel:personSubject ?person ;
                rel:placeObject ?rel_place ;
        		rel:source ?death ;
                rel:date ?deathtime ;
      			skos:prefLabel ?description .
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

      		?rel_place a rel:Place .
      		?rel_place skos:closeMatch ?place .
      		?rel_place skos:prefLabel ?placeName .

      		?person skosxl:prefLabel ?personLabel .
            ?personLabel skos:prefLabel ?personName .
            ?personLabel schema:familyName ?familyName .
            ?personLabel schema:givenName ?givenName .

      		BIND(uri(encode_for_uri(concat(str(?person), str(?rel_place), "death_place", str(?death)))) as ?uri) .

            BIND(concat(str(?givenName), " ", str(?familyName), " on kuollut paikkassa ", str(?placeName), ".") as ?description) .

        }'''

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/nbf_deaths.ttl", "w")

    write_file.write(response.text)

def birth_places():
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
	    BASE <http://ldf.fi/relsearch/>
	    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

        CONSTRUCT {
        ?uri a rel:Relation ;
            rel:relationType rel:birthPlace ;
            rel:personSubject ?person ;
            rel:placeObject ?rel_place ;
    		rel:source ?birth ;
            rel:date ?birthTime ;
  			skos:prefLabel ?description .
        }

        WHERE {
            VALUES ?place_class { schema:Place nbf:Place rel:Place }
            VALUES ?person_class { gvp:PersonConcept foaf:Person }
            ?person a|(a/rdfs:subClassOf+) ?person_class .
            ?birth crm:P98_brought_into_life/^foaf:focus ?person .
            ?birth ?any ?place . # nbf:place!
            ?place a|(a/rdfs:subClassOf+) ?place_class . 
            OPTIONAL {
  	            ?birth nbf:time ?time . # Not general!
  	            ?time gvp:estStart ?birthTime .
            }
            OPTIONAL {
                ?birth gvp:estStart ?birthTime .
            }
  		
  		    ?rel_place a rel:Place .
  		    ?rel_place skos:closeMatch ?place .
  		    ?rel_place skos:prefLabel ?placeName .
  
  		    ?person skosxl:prefLabel ?personLabel .
            ?personLabel skos:prefLabel ?personName .
            ?personLabel schema:familyName ?familyName .
            ?personLabel schema:givenName ?givenName .
  		
  		    BIND(uri(encode_for_uri(concat(str(?person), str(?rel_place), "birth_place", str(?birth)))) as ?uri) .
  		
            BIND(concat(str(?givenName), " ", str(?familyName), " on syntynyt paikkassa ", str(?placeName), ".") as ?description) .
  		
        }'''

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/nbf_births.ttl", "w")

    write_file.write(response.text)

death_places()
birth_places()
