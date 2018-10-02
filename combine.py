from rdflib import Graph

def combine_demo(g):
    g.parse('constructed/schema.ttl', format='turtle')
    g.parse('constructed/fennica_work_places.ttl', format='turtle')
    g.parse('constructed/fng_depicts_place.ttl', format='turtle')
    g.parse('constructed/history_event_places.ttl', format='turtle')
    g.parse('constructed/kirjasampo_novel_places.ttl', format='turtle')
    #g.parse('constructed/snellman_letter_places.ttl', format='turtle')
    #g.parse('constructed/snellman_received_places.ttl', format='turtle')


def combine_nbf(g):
    g.parse('constructed/nbf_births.ttl', format='turtle')
    g.parse('constructed/nbf_deaths.ttl', format='turtle')
    g.parse('constructed/nbf_event_places.ttl', format='turtle')

def combine_snellman(g):
    g.parse('constructed/snellman_letter_places.ttl', format='turtle')
    g.parse('constructed/snellman_received_places.ttl', format='turtle')

graph_demo= Graph()
combine_demo(graph_demo)
graph_demo.serialize('constructed/demo_relations.ttl', format='turtle')

#graph_nbf= Graph()
#combine_nbf(graph_nbf)
#graph_nbf.serialize('constructed/demo_nbf_relations.ttl', format='turtle')

#graph_snellman= Graph()
#combine_snellman(graph_snellman)
#graph_snellman.serialize('constructed/demo_snellman_relations.ttl', format='turtle')


