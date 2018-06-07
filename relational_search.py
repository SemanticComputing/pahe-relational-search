from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

rel = Namespace('http://ldf.fi/relsearch/')

def schema(g):
    g.add((rel.relation, namespace.RDF.type, namespace.RDFS.Class))
    g.add((rel.relation, namespace.SKOS.prefLabel, Literal('Yhteys kahden asian välillä', lang='fi')))

    g.add((rel.personSubject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.personSubject, namespace.SKOS.prefLabel, Literal('Yhdistettävä henkilö', lang='fi')))

    g.add((rel.placeObject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.placeObject, namespace.SKOS.prefLabel, Literal('Yhdistettävä paikka', lang='fi')))

    g.add((rel.relationType, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.relationType, namespace.SKOS.prefLabel, Literal('Yhteyden tyyppi', lang='fi')))

    g.add((rel.date, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.date, namespace.SKOS.prefLabel, Literal('Yhteyden aikaisin päivämäärä', lang='fi')))

    g.add((rel.source, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.source, namespace.SKOS.prefLabel, Literal('Kuvaus tiedon haku paikasta', lang='fi')))

    g.add((rel.sourceLink, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.sourceLink, namespace.SKOS.prefLabel, Literal('Linkki yhteyteen liittyvään resurssiin', lang='fi')))


    # death and birth

    g.add((rel.lifeEvent, namespace.RDF.type, rel.RelationType))
    g.add((rel.lifeEvent, namespace.SKOS.prefLabel, Literal('Syntymä ja kuolema', lang='fi')))

    g.add((rel.birthPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.birthPlace, namespace.SKOS.broader, rel.lifeEvent))
    g.add((rel.birthPlace, namespace.SKOS.prefLabel, Literal('A on syntynyt paikassa B', lang='fi')))

    g.add((rel.deathPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.deathPlace, namespace.SKOS.broader, rel.lifeEvent))
    g.add((rel.deathPlace, namespace.SKOS.prefLabel, Literal('A on kuollut paikassa B', lang='fi')))


    # letters

    g.add((rel.letters, namespace.RDF.type, rel.RelationType))
    g.add((rel.letters, namespace.SKOS.prefLabel, Literal('Kirjeisiin liittyvät yhteydet', lang='fi')))

    g.add((rel.letterSentFrom, namespace.RDF.type, rel.RelationType))
    g.add((rel.letterSentFrom, namespace.SKOS.broader, rel.letters))
    g.add((rel.letterSentFrom, namespace.SKOS.prefLabel, Literal('A on lähettänyt kirjeen paikasta B', lang='fi')))

    g.add((rel.letterReceivedFrom, namespace.RDF.type, rel.RelationType))
    g.add((rel.letterReceivedFrom, namespace.SKOS.broader, rel.letters))
    g.add((rel.letterReceivedFrom, namespace.SKOS.prefLabel, Literal('A on vastaanottanut kirjeen paikasta B', lang='fi')))


    # created work relates to place

    g.add((rel.creationEvent, namespace.RDF.type, rel.RelationType))
    g.add((rel.creationEvent, namespace.SKOS.prefLabel,
           Literal('A on luonut teoksen joka liittyy paikkaan B', lang='fi')))

    g.add((rel.workDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.workDepictsPlace, namespace.SKOS.broader, rel.creationEvent))
    g.add((rel.workDepictsPlace, namespace.SKOS.prefLabel,
           Literal('A on luonut teoksen joka kuvaa paikkaa B', lang='fi')))

    g.add((rel.paintingDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.paintingDepictsPlace, namespace.SKOS.broader, rel.workDepictsPlace))
    g.add((rel.paintingDepictsPlace, namespace.SKOS.prefLabel,
           Literal('A on maalannut teoksen joka kuvaa paikkaa B', lang='fi')))

    g.add((rel.novelDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.novelDepictsPlace, namespace.SKOS.broader, rel.workDepictsPlace))
    g.add((rel.novelDepictsPlace, namespace.SKOS.prefLabel,
                     Literal('A on kirjoittanut romaanin joka kuvaa paikkaa B', lang='fi')))


    # career and honours

    g.add(((rel.careerRelation, namespace.RDF.type, rel.RelationType)))
    g.add((rel.careerRelation, namespace.SKOS.prefLabel, Literal('Ura, opiskelu ja kunnianosoitukset')))

    g.add((rel.careerAtPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.careerAtPlace, namespace.SKOS.broader, rel.careerRelation))
    g.add((rel.careerAtPlace, namespace.SKOS.prefLabel, Literal('A:n ura tai opiskelu liittyy paikkaan B', lang='fi')))

    g.add((rel.honourAtPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.honourAtPlace, namespace.SKOS.broader, rel.careerRelation))
    g.add((rel.honourAtPlace, namespace.SKOS.prefLabel,
                 Literal('A on vastaanottanut kunnianosoituksen paikassa B', lang='fi')))



    g.serialize('relations/schema.ttl', format='turtle')

graph = Graph()

graph.bind('', rel)
graph.bind('skos', namespace.SKOS)

schema(graph)

graph.parse('relations/careers_to_places.ttl', format='turtle')
graph.parse('relations/kulttuurisampo_paintings.ttl', format='turtle')
graph.parse('relations/nbf_life_relations.ttl', format='turtle')
graph.parse('relations/snellman_relations.ttl', format='turtle')
graph.parse('relations/kirjasampo_books_depict_place.ttl', format='turtle')

graph.serialize('relations/pahe_relations.ttl', format='turtle')
