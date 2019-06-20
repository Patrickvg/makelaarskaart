from models.Connection_sheet import get_sheet_data, clean
from mapbox import Datasets
from config import Config
from models.Reorganize import get_data_set_from_mapbox, delete_feature, add_feature
from models.Locations import add_lng_lat_data


def dataset_choice(branche):
    if branche == 'NVM':
        return Config.dataset_NVM
    elif branche == 'VBO':
        return Config.dataset_VBO
    elif branche == 'VastgoedPRo':
        return Config.dataset_VastgoedPRo
    elif branche == 'Onafhankelijk':
        return Config.dataset_Onafhankelijk


def update_mapbox(dataset_realtor, mapbox_data):
    # get realtors already online in mapbox
    cleaned_realtor_data = dataset_realtor
    cleaned_realtor_data['in_list'] = list(map(lambda x: x in list(mapbox_data['properties.Makelaarsnaam']),
                                               cleaned_realtor_data['Makelaarsnaam']))
    realtor_for_location = cleaned_realtor_data[cleaned_realtor_data['in_list'] != True]
    # remove realtors if neccesary
    set_to_add = add_lng_lat_data(realtor_for_location, Config.google_token)
    # get lat_lon for new realtors
    set_to_add.drop(['Plaats', 'Postcode', 'Huisnummer', 'index'], inplace=True, axis=1)
    set_to_add.rename(index=str, columns={'Casco ID': 'Casco_id'}, inplace=True)
    # clean dataframe to comply to mapbox standard
    added = list(map(lambda index,name,branche, row_id, lat, lng:
                     add_feature(dataset_id=dataset_choice(branche=branche),
                                 index=index,
                                 name=name,
                                 row_id=str(row_id),
                                 branche=branche,
                                 lat=lat,
                                 lng=lng,
                                 mapbox_dataset=dataset_constructor_mapbox),
                     set_to_add.index.values,
                     set_to_add['Makelaarsnaam'],
                     set_to_add['Branche'],
                     set_to_add['Casco_id'],
                     set_to_add['lat'],
                     set_to_add['lng']))
    return added
    '''return print("adding to {}: \n"
                 "{} \n"
                 "{} \n".format(branches, set_to_add, added))'''
# add new features to dataset of mapbox


def remove_mapbox(dataset_realtor, mapbox_data):
    data_mapbox = mapbox_data
    data_mapbox['in_list'] = list(
        map(lambda x: x in list(dataset_realtor['Makelaarsnaam']), data_mapbox['properties.Makelaarsnaam']))
    set_to_remove = data_mapbox[data_mapbox['in_list'] != True].reset_index()
    removed = list(map(lambda mapbox_row_id:
                       delete_feature(dataset_id=dataset_choice(branche=branches),
                                      row_id=mapbox_row_id,
                                      mapbox_dataset=dataset_constructor_mapbox),
                       set_to_remove['id']))
    return print("removing from {}: \n"
                 "{} \n"
                 "{} \n".format(branches, set_to_remove, removed))


if __name__ == "__main__":
    dataset_constructor_mapbox = Datasets(access_token=Config.mapbox_token)
    active_realtor_data = get_sheet_data()
    clean_realtor_data = clean(active_realtor_data)

    for branches in list(set(active_realtor_data.Branche))[0:]:
        realtor_data = clean_realtor_data[clean_realtor_data['Branche'] == branches]
        mapbox_dataset = get_data_set_from_mapbox(dataset_choice(branche=branches), dataset_constructor_mapbox)
        update_mapbox(realtor_data, mapbox_dataset)
        remove_mapbox(realtor_data, mapbox_dataset)
