import requests

def construct(store, write_file, query):
    response = requests.post(store,
                             data={'query': query})
    write_file.write(response.text)


# Needs place ontology, people from nbf, linkage file, raw relations file
def kirjasampo():
    query_file = open("queries/kirjasampo_n_places_construct.sparql", "r")
    w_file = open("constructed/kirjasampo_novel_places.ttl", "w")
    construct("http://localhost:3030/ds/query", w_file, query_file.read())

kirjasampo()