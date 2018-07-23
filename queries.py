import requests


def execute_query(store, write_file, query):
    response = requests.post(store,
                             data={'query': query})
    write_file.write(response.text)


def raw_kirjasampo():
    query_file = open("queries/kirjasampo_novel_places.sparql", "r")
    w_file = open("constructed/raw/kirjasampo_novel_places_raw.ttl", "w")
    execute_query("http://ldf.fi/kirjasampo/sparql", w_file, query_file.read())


# Needs (on localhost server) place ontology, people from nbf, linkage file, raw relations file

# NOTE: 

def kirjasampo():
    query_file = open("queries/kirjasampo_n_places_construct.sparql", "r")
    w_file = open("constructed/kirjasampo_novel_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())
