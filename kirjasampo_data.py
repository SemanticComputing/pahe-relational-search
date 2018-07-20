import requests



def construct(store, write_file, query):
    response = requests.post(store,
                             data={'query': query})
    write_file.write(response.text)


def raw_kirjasampo():
    query_file = open("queries/kirjasampo_novel_places.sparql", "r")
    w_file = open("constructed/raw/kirjasampo_novel_places_raw.ttl", "w")
    construct("http://ldf.fi/kirjasampo/sparql", w_file, query_file.read())

raw_kirjasampo()