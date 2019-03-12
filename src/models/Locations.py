import googlemaps


def get_lng_lat(postalcode, huisnummer, city, key):
    try:
        address = str(postalcode) + ', ' + str(huisnummer) + ', ' + str(city)
    except:
        address = "onbekend"
    gmaps = googlemaps.Client(key=key)

    try:
        geocode_result = gmaps.geocode(address + ', Netherlands')
        result = geocode_result[0]['geometry']['location']
        print("getting", address)
        return result['lat'], result['lng']
    except:
        print("trouble with", address)
        return 'NA', 'NA'


def add_lng_lat_data(data, key):
    lat_lng = list(map(lambda x, y, z: get_lng_lat(x, y, z, key), data['Postcode'], data['Huisnummer'], data['Plaats']))
    lat = []
    lng = []
    for i in lat_lng:
        lng.append(i[1])
        lat.append(i[0])
    data['lng'] = lng
    data['lat'] = lat
    data_clean = data[data['lat'] != 'NA']
    return data_clean
