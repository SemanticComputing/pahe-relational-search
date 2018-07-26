import csv
import utilities
import requests
from rdflib import Graph,namespace, Namespace, URIRef



def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (high + low) // 2
        #print(values[mid] + " " + target)
        if values[mid] == target:
            return mid
        else:
            if target < values[mid]:
                high = mid - 1
            else:
                low = mid + 1
    return -1

# spesific for these csv-files
def make_list(csv_file, index):
    list = []
    for row in csv_file:
        list.append(row[index].replace('"','').strip())
    return list


def nbf_to_histo_from_csv(g):

    csv_histo = csv.reader(open('csv/histo_names.csv', 'r'))

    csv_nbf = csv.reader(open('csv/nbf_names.csv', 'r'))
    nbf_comparison_list = make_list(csv_nbf, 1)

    csv_nbf = csv.reader(open('csv/nbf_names.csv', 'r'))
    nbf_uri_list = make_list(csv_nbf, 0)

    for row in csv_histo:
        try:
            index = binary_search(nbf_comparison_list, row[1].replace('"','').strip())
            if index >= 0:
                print(index)
                g.add((URIRef(nbf_uri_list[index]), namespace.SKOS.exactMatch, URIRef(row[0].replace('"','').strip())))
        except:
            pass


#graph = Graph()
#nbf_to_fennica_from_csv(graph)
#graph.serialize('graphs/fennica_linkin.ttl', format='turtle')

graph = Graph()
nbf_to_histo_from_csv(graph)
graph.serialize('graphs/histo_links.ttl', format='turtle')