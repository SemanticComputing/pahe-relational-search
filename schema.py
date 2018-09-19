from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

rel = Namespace('http://ldf.fi/relse/')

def schema(g):

    g.add((rel.place, namespace.RDF.type, namespace.RDFS.Class))
    g.add((rel.place, namespace.SKOS.prefLabel, Literal('Paikka', lang='fi')))

    g.add((rel.relation, namespace.RDF.type, namespace.RDFS.Class))
    g.add((rel.relation, namespace.SKOS.prefLabel, Literal('Yhteys kahden asian välillä', lang='fi')))

    g.add((rel.relationEndPoint, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.relationEndPoint, namespace.SKOS.prefLabel, Literal('Semanttisen yhteyden alku- tai päätepiste', lang='fi')))

    g.add((rel.relationSubject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.relationSubject, namespace.RDFS.subPropertyOf, rel.relationEndPoint))
    g.add((rel.relationSubject, namespace.SKOS.prefLabel,
           Literal('Semanttisen yhteyden alkupiste', lang='fi')))

    g.add((rel.relationObject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.relationObject, namespace.RDFS.subPropertyOf, rel.relationEndPoint))
    g.add((rel.relationObject, namespace.SKOS.prefLabel,
           Literal('Semanttisen yhteyden päätepiste', lang='fi')))

    g.add((rel.personSubject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.personSubject, namespace.SKOS.prefLabel, Literal('Yhteyden henkilösubjekti', lang='fi')))
    g.add((rel.personSubject, namespace.RDFS.subPropertyOf, rel.relationSubject))

    g.add((rel.placeObject, namespace.RDF.type, namespace.RDF.Property))
    g.add((rel.placeObject, namespace.SKOS.prefLabel, Literal('Yhteyden paikkaobjekti', lang='fi')))
    g.add((rel.placeObject, namespace.RDFS.subPropertyOf, rel.relationObject))

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
    g.add((rel.lifeEvent, namespace.SKOS.broader, rel.eventRelation))

    g.add((rel.birthPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.birthPlace, namespace.SKOS.broader, rel.lifeEvent))
    g.add((rel.birthPlace, namespace.SKOS.prefLabel, Literal('Syntynyt paikassa', lang='fi')))

    g.add((rel.deathPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.deathPlace, namespace.SKOS.broader, rel.lifeEvent))
    g.add((rel.deathPlace, namespace.SKOS.prefLabel, Literal('Kuollut paikassa', lang='fi')))


    # letters

    g.add((rel.letters, namespace.RDF.type, rel.RelationType))
    g.add((rel.letters, namespace.SKOS.prefLabel, Literal('Kirjeisiin liittyvät yhteydet', lang='fi')))

    g.add((rel.letterSentFrom, namespace.RDF.type, rel.RelationType))
    g.add((rel.letterSentFrom, namespace.SKOS.broader, rel.letters))
    g.add((rel.letterSentFrom, namespace.SKOS.prefLabel, Literal('Lähettetty kirje paikasta', lang='fi')))

    g.add((rel.letterReceivedFrom, namespace.RDF.type, rel.RelationType))
    g.add((rel.letterReceivedFrom, namespace.SKOS.broader, rel.letters))
    g.add((rel.letterReceivedFrom, namespace.SKOS.prefLabel, Literal('Vastaanotettu kirje paikasta', lang='fi')))


    # created work relates to place

    g.add((rel.creationEvent, namespace.RDF.type, rel.RelationType))
    g.add((rel.creationEvent, namespace.SKOS.prefLabel,
           Literal('Teos liittyy paikkaan', lang='fi')))

    g.add((rel.workDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.workDepictsPlace, namespace.SKOS.broader, rel.creationEvent))
    g.add((rel.workDepictsPlace, namespace.SKOS.prefLabel,
           Literal('Teos kuvaa paikkaa', lang='fi')))

    g.add((rel.paintingDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.paintingDepictsPlace, namespace.SKOS.broader, rel.workDepictsPlace))
    g.add((rel.paintingDepictsPlace, namespace.SKOS.prefLabel,
           Literal('Maalaus kuvaa paikkaa', lang='fi')))

    g.add((rel.novelDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.novelDepictsPlace, namespace.SKOS.broader, rel.literaryWorkDepictsPlace))
    g.add((rel.novelDepictsPlace, namespace.SKOS.prefLabel,
                     Literal('Romaani kuvaa paikkaa', lang='fi')))

    g.add((rel.literaryWorkDepictsPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.literaryWorkDepictsPlace, namespace.SKOS.broader, rel.workDepictsPlace))
    g.add((rel.literaryWorkDepictsPlace, namespace.SKOS.prefLabel, Literal('Kirjoitus kuvaa paikkaa', lang='fi')))

    # events

    g.add((rel.eventRelation, namespace.RDF.type, rel.RelationType))
    g.add((rel.eventRelation, namespace.SKOS.prefLabel, Literal('Tapahtumiin liittyvat yhteydet', lang='fi')))

    g.add((rel.eventTookPlaceAt, namespace.RDF.type, rel.RelationType))
    g.add((rel.eventTookPlaceAt, namespace.SKOS.prefLabel, Literal('Historiallinen tapahtuma paikassa', lang='fi')))
    g.add((rel.eventTookPlaceAt, namespace.SKOS.broader, rel.eventRelation))

    #g.add((rel.minorEvent, namespace.RDF.type, rel.RelationType))
    #g.add((rel.minorEvent, namespace.SKOS.prefLabel, Literal('Henkilökohtaiset tapahtumat')))
    #g.add((rel.minorEvent, namespace.SKOS.broader, rel.eventRelation))

    g.add((rel.careerAtPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.careerAtPlace, namespace.SKOS.broader, rel.eventRelation))
    g.add((rel.careerAtPlace, namespace.SKOS.prefLabel, Literal('Ura tai opiskelu liittyy paikkaan', lang='fi')))

    g.add((rel.honourAtPlace, namespace.RDF.type, rel.RelationType))
    g.add((rel.honourAtPlace, namespace.SKOS.broader, rel.eventRelation))
    g.add((rel.honourAtPlace, namespace.SKOS.prefLabel,
                 Literal('Kunnianosoitus liittyy paikkaan', lang='fi')))



    g.serialize('constructed/schema.ttl', format='turtle')

graph = Graph()
schema(graph)
