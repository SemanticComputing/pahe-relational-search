import csv
import utilities
import json


def jotain():
    csv_place = csv.reader(open('csv/rel_places.csv', 'r'))
    place_list = utilities.make_list(csv_place)

    print(place_list[1][utilities.find_index("aamu", place_list[0])])

    csv_art = csv.reader(open('csv/nbf_artists.csv', 'r'))
    artist_list = utilities.make_list(csv_art)

    print(utilities.find_index("aamu", place_list[0]))

def title(elem):
    try:
        for title in elem['title']:
            if 'fi' in title:
                print(title['fi'])
    except:
        pass

def get_artist(elem, list):
    for row in elem['creator']:
        if 'value' in row:
            artist = row['value']
            index = utilities.find_index(artist, list[0])
            if index != -1:
                artist_uri = list[1][index]
                print(' ' + artist_uri)

def get_subject(elem, list):
    for row in elem['subject']:
        if 'keyword' in row:
            subject = row['keyword']
            index = utilities.find_index(subject, list[0])
            if index != -1:
                subject_uri = list[1][index]
                print('     ' + subject_uri)

def get_place(subject, place_list):
    return 1

def parse():

    csv_place = csv.reader(open('csv/rel_places.csv', 'r'))
    place_list = utilities.make_list(csv_place)

    csv_art = csv.reader(open('csv/nbf_artists.csv', 'r'))
    artist_list = utilities.make_list(csv_art)


    art_json = open('graphs/fng-data-dc.json', 'r')
    parsed_json = json.load(art_json)
    for element in parsed_json['descriptionSet']:
        try:
            for type in element['type']:
                if 'type' in type:
                    if type['type'] == 'artwork':
                        title(element)
                        get_artist(element, artist_list)
                        get_subject(element, place_list)
        except:
            pass


parse()

#jotain()