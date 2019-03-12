from dotenv import load_dotenv
from os.path import join, dirname
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(object):
    mapbox_token = os.environ.get('MAPBOX_ACCESS_TOKEN')
    google_secret_location = os.environ.get('GOOGLE_SECRET_LOCATION')
    dataset_Onafhankelijk = os.environ.get('MAPBOX_DATASET_ID_ONAFHANKELIJK')
    dataset_VastgoedPRo = os.environ.get('MAPBOX_DATASET_ID_VASTGOEDPRO')
    dataset_NVM = os.environ.get('MAPBOX_DATASET_ID_NVM')
    dataset_VBO = os.environ.get('MAPBOX_DATASET_ID_VBO')
    google_token = os.environ.get("GOOGLE_TOKEN")
