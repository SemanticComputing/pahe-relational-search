from rdflib import Graph

g = Graph()
g.parse('constructed/person_ontology.ttl', format='turtle')
g.parse('constructed/history_event_places.ttl', format='turtle')
g.parse('constructed/fennica_work_places.ttl', format='turtle')
g.parse('constructed/kirjasampo_novel_places.ttl', format='turtle')
g.parse('constructed/snellman_letter_places.ttl', format='turtle')
g.parse('constructed/snellman_received_places.ttl', format='turtle')
g.parse('constructed/schema.ttl', format='turtle')
g.parse('constructed/fng_depicts_place.ttl', format='turtle')
g.parse('graphs/place_ontology.ttl', format='turtle')

g.serialize('graphs/demo_relations.ttl', format='turtle')