import pandas as pd


def get_data_set_from_mapbox(dataset_id, mapbox_dataset):
    data = mapbox_dataset.list_features(dataset_id)
    df = pd.io.json.json_normalize(data.json()['features'])
    lat = []
    lng = []
    for i in df['geometry.coordinates']:
        lng.append(i[0])
        lat.append(i[1])
    df['lat'] = lat
    df['lng'] = lng
    return df


def add_feature(dataset_id, row_id, name, branche, lat, lng, mapbox_dataset):
    feature = {
        'type': 'Feature', 'id': row_id, 'properties': {'Makelaarsnaam': name, 'Branche': branche,
                                                        'coordinates': [lng, lat]},
        'geometry': {'type': 'Point', 'coordinates': [lng, lat]}}
    resp = mapbox_dataset.update_feature(dataset_id, id, feature)
    return resp.status_code


def delete_feature(dataset_id, row_id, mapbox_dataset):
    resp = mapbox_dataset.delete_feature(dataset_id, row_id)
    return resp.status_code
