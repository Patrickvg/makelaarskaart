from apiclient import discovery
from google.oauth2 import service_account
from config import Config
import pandas as pd


def get_sheet_data():
    try:
        scopes = ['https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/drive.file',
                  'https://www.googleapis.com/auth/spreadsheets']
        secret_file = Config.google_secret_location

        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)

        spreadsheet_id = '1lamfclV9II4j7shxTaxUVuKbBIaKM7JYj7HNkTFQ-Fo'

        range_name = 'Actief'

        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name)
        response = request.execute()

        headers = response['values'].pop(0)
        df = pd.DataFrame(response['values'], columns=headers)

        df = df[(df['Casco ID'].notnull()) & (df['Casco ID'] != '')].reset_index()
        return df

    except OSError as e:
        print(e)


def clean(dataset):
    dataset.rename(index=str, columns={'Huisnr.': 'Huisnummer'}, inplace=True)
    dataset_ka_online = dataset[(dataset['KA gekoppeld'] == '✓ Directe XML (niet via KA)') | (dataset['KA gekoppeld'] == '✓')]
    dataset_ka_online.drop(['Provincie', 'Contactpersoon', 'Emailadres', 'KA',
                            'Datum akkoord', 'Maand akkoord', 'Zelf aangemeld?', 'Bron',
                            'Accountmanager Auto-fill', 'Gekoppeld door', 'KA gekoppeld',
                            'Aanbod online', 'Huislijn uitgesloten', 'Uitbehandeld RB',
                            'Agent Pages status', 'Akkoord AV', 'RB contactmoment',
                            'Linkje gevraagd?', 'Linkjes actief', 'Datum link online',
                            'Link vermelding', 'Link bestemming', 'OPMERKINGEN'], inplace=True, axis=1)
    return dataset_ka_online
