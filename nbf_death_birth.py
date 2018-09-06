import requests

store = 'http://localhost:3030/ds/query'

def death_places():
    query_file = open("queries/nbf_deaths.sparql", "r")
    q = query_file.read()

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/nbf_deaths.ttl", "w")

    write_file.write(response.text)

def birth_places():
    query_file = open("queries/nbf_births.sparql", "r")
    q = query_file.read()

    response = requests.post(store,
                             data={'query': q})

    write_file = open("constructed/nbf_births.ttl", "w")

    write_file.write(response.text)

death_places()
birth_places()
