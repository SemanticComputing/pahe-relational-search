from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

# btj is missing, around hundred instances
nbf = Namespace('http://ldf.fi/nbf/')

def convert_to_csv(graph):
    q = graph.query('''
        prefix nbf:<http://ldf.fi/nbf/>
        
        SELECT DISTINCT ?nbf ?kirjasampo
        WHERE {
	        ?nbf nbf:kirjasampo ?kirjasampo .  
        } ''')

    csv_file = open('csv/corrected_kirjasampo.csv', 'w')

    g = Graph()

    for row in q:
        string = row[1]
        string = string.replace('http://www.kirjasampo.fi/fi/kulsa/kauno%253A', 'http://www.yso.fi/onto/kaunokki#')
        string = string.replace('http://www.kirjasampo.fi/fi/kulsa/saha3%253A', 'ttp://seco.tkk.fi/saha3/')

        if 'www.btj.fi%252' not in string:
            csv_file.write('"' + row[0] + '","' + string + '"\n')
            g.add((URIRef(row[0]), nbf.kirjasampo, URIRef(string)))

    g.serialize('graphs/corrected_kirjasampo_linkage.ttl', format='turtle')

    csv_file.close()

graph = Graph()
graph.parse('NBF/Kirjasampo.ttl', format='turtle')

convert_to_csv(graph)



