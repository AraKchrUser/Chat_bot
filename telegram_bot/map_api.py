import requests
from pprint import pprint


def get_static_api():
    # longlat — долгота, широта;
    geocoder_req = ("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode"
                    "=Благовещенск,+ул.+50+лет+Октября,+8/2&format=json")
    response = requests.get(geocoder_req)
    if response:
        response = response.json()
        toponym = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        address = toponym['metaDataProperty']['GeocoderMetaData']['text']
        coord = toponym['Point']['pos']
        # print(f'address: {address}\t\t coord: {coord}')
        req = ('https://static-maps.yandex.ru/1.x/?display-text'
               f'=%D0%9C%D0%A4%D0%A6&ll={coord.split()[0]},{coord.split()[1]}&spn=0.0001457,0.00119&l=map,trf&size=650,450')
        return req
    else:
        return 'Error'
