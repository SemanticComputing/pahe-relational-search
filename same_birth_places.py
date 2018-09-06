import requests

endpoint = "http://localhost:3030/ds/query"

def get_query(dateMin, dateMax):
    query = '''
        PREFIX schema: <http://schema.org/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX nbf:	<http://ldf.fi/nbf/>
        PREFIX relse: <http://ldf.fi/relsearch/>
        BASE <http://ldf.fi/relse/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
        PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        CONSTRUCT {
          ?uri a relse:Relation ;
            relse:personSubject ?person1 ;
            relse:personObject ?person2 ;
            relse:date ?earlierDate ;
            skos:prefLabel ?description ;
            relse:source ?source1 ;
            relse:source ?source2 ;
            relse:sourceName "Tapahtuma Semanttisessa Kansallisbiografiassa"@fi ;
            
            rdfs:seeAlso ?placeMatch .
        }
            
        WHERE {
        
          ?relation1 a relse:Relation .
          ?relation1 relse:date ?date1 .
          FILTER(?date1 < "''' + dateMax + '''"^^xsd:date) .
          FILTER(?date1 > "''' + dateMin + '''"^^xsd:date) .
        
          ?relation2 a relse:Relation .
            
          ?relation1 relse:placeObject ?place .
          ?relation2 relse:placeObject ?place .
          
          ?relation1 relse:personSubject ?person1 .
          ?relation2 relse:personSubject ?person2 .
          
          FILTER (?person1 != ?person2) .
            
          ?relation2 relse:date ?date2 .
          
          ?relation1 relse:source ?source1 .
          ?relation2 relse:source ?source2 .
          
          ?person1 skosxl:prefLabel ?label1 .
          ?label1 schema:familyName ?familyName1 .
          ?label1 schema:givenName ?givenName1 .
          
          ?person2 skosxl:prefLabel ?label2 .
          ?label2 schema:familyName ?familyName2 .
          ?label2 schema:givenName ?givenName2 .
          
          ?place skos:prefLabel ?placeLabel .
          ?place skos:exactMatch ?placeMatch .
          
          BIND (if(?date1 < ?date2, ?date1, ?date2) as ?earlierDate) .
          
          BIND (concat(str(?givenName1), " ", str(?familyName1), " ja ", str(?givenName2), " ", str(?familyName2), " ovat molemmat syntyneet paikassa ", str(?placeLabel), ".") as ?description ) 
          
          BIND (uri(encode_for_uri(concat("AAb", str(?person1), str(?person2), "_same_b_place"))) as ?uri)
        }
        '''

    return query

def execute_query(write_file, query):
    print("executing query")
    print(query)
    response = requests.post(endpoint,
                             data={'query': query})
    write_file.write(response.text)

def same_b_places():

    w_file = open("constructed/births/births1700.ttl", "w")
    query = get_query("0100-12-31", "1700-01-01")
    execute_query(w_file, query)

    w_file = open("constructed/births/births1800.ttl", "w")
    query = get_query("1699-12-31", "1800-01-01")
    execute_query(w_file, query)

    w_file = open("constructed/births/births1850.ttl", "w")
    query = get_query("1799-12-31", "1850-01-01")
    execute_query(w_file, query)

    w_file = open("constructed/births/births1900.ttl", "w")
    query = get_query("1850-01-01", "1899-12-31")
    execute_query(w_file, query)

    w_file = open("constructed/births/births1950.ttl", "w")
    query = get_query("1900-01-01", "1949-12-31")
    execute_query(w_file, query)

    w_file = open("constructed/births/births2020.ttl", "w")
    query = get_query("1950-01-01", "2020-12-31")
    execute_query(w_file, query)


same_b_places()