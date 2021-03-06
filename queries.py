import requests


def execute_query(store, write_file, query):
    print("executing query")
    print(query)
    response = requests.post(store,
                             data={'query': query})
    write_file.write(response.text)


# kirjasampo Novels depict places

def raw_kirjasampo():
    query_file = open("queries/kirjasampo_novel_places.sparql", "r")
    w_file = open("constructed/raw/kirjasampo_novel_places_raw.ttl", "w")
    execute_query("http://ldf.fi/kirjasampo/sparql", w_file, query_file.read())


# Needs (on localhost server) place ontology, people from nbf, linkage file, raw relations file

def kirjasampo():
    query_file = open("queries/kirjasampo_n_places_construct.sparql", "r")
    w_file = open("constructed/kirjasampo_novel_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())


# Fennica places

def raw_fennica_subject_places():
    query_file = open("queries/fennica_work_depicts_place.sparql", "r")
    w_file = open("constructed/raw/fennica_work_places_raw.ttl", "w")
    execute_query("http://data.nationallibrary.fi/bib/sparql", w_file, query_file.read())

# needs people; fennica_links; place_ontology; raw_fennica
def fennica_works():
    print("fennica")
    query_file = open("queries/fennica_works.sparql", "r")
    w_file = open("constructed/fennica_work_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

# Historia

def history_event_places_raw():
    query_file = open("queries/histo_events_places.sparql", "r")
    w_file = open("constructed/raw/histo_places_raw.ttl", "w")
    execute_query("http://ldf.fi/history/sparql", w_file, query_file.read())

def histo_linking():
    query_file = open("queries/linking/histo_place_linking.sparql", "r")
    w_file = open("graphs/histo_place_links_1.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def histo_linking2():
    query_file = open("queries/linking/histo_place_linking2.sparql", "r")
    w_file = open("graphs/histo_place_links_2.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def construct_history_event_places():
    query_file = open("queries/histo_even_places_construct.sparql", "r")
    w_file = open("constructed/history_event_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

# Snellman

def snellman_letters_raw():
    query_file = open("queries/snellman_letters_raw.sparql", "r")
    w_file = open("constructed/raw/snellman_letters_raw.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def snellman_received_raw():
    query_file = open("queries/snellman_received_raw.sparql", "r")
    w_file = open("constructed/raw/snellman_received_raw.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def snellman_letters_construct():
    query_file = open("queries/snellman_letters_construct.sparql", "r")
    w_file = open("constructed/snellman_letter_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def snellman_received_construct():
    query_file = open("queries/snellman_received_construct.sparql", "r")
    w_file = open("constructed/snellman_received_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

# nbf-events

def nbf_event_places_construct():
    query_file = open("queries/nbf_events_construct.sparql", "r")
    w_file = open("constructed/nbf_event_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def create_person_ontology():
    query_file = open("queries/linking/new_person_ontology.sparql", "r")
    w_file = open("constructed/person_ontology.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def same_birth_place():
    query_file = open("queries/same_birth_place.sparql", "r")
    w_file = open("constructed/hehe/same_birth_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def place_linking_to_nbf():
    query_file = open("queries/linking/place_rel_to_nbf.sparql", "r")
    w_file = open("graphs/bad_places.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

# fng

def fng_construct():
    query_file = open("queries/fng_construct.sparql", "r")
    w_file = open("constructed/fng_depicts_place.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())


# filtering relations to only dead people

def only_dead_people():
    query_file = open("queries/linking/only_dead_people.sparql", "r")
    w_file = open("constructed/person_ontology.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())

def filter_relations():
    query_file = open("queries/filter_relations.sparql", "r")
    w_file = open("constructed/relations.ttl", "w")
    execute_query("http://localhost:3030/ds/query", w_file, query_file.read())