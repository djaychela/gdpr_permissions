import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.capabilities_service import CapabilitiesService
from gdpr_permissions.services.preferences_service import Preferences
import os


class SheetsImport:
    @staticmethod
    def access_sheets():
        scope = ['https://spreadsheets.google.com/feeds']
        oauth_file = Preferences.get_preference('sheets_import_json_file')
        oauth_file_location = os.path.abspath('gdpr_permissions/config/' + oauth_file)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_file_location, scope)
        gc = gspread.authorize(credentials)
        return gc.open('Pupil Import Test Sheet').sheet1


    @staticmethod
    def import_from_sheets():
        wks = SheetsImport.access_sheets()

        current_row = 2
        # get data list and clean values to True and False
        while wks.cell(current_row, 1).value:
            data_list = wks.row_values(current_row)
            data_cleaned = [True if x == 'TRUE' else False for x in data_list[3:]]
            pupil_attribute_columns = list(PupilsService.attributes().keys())[1:4]
            pupil_capability_columns = list(CapabilitiesService.get_capabilities().keys())
            print(pupil_attribute_columns, pupil_capability_columns)

            # check if row already imported
            imported_cell_column = 4 + len(CapabilitiesService.get_capabilities())
            if wks.cell(current_row, imported_cell_column).value != "DONE":

                # build pupil dict to send to db
                new_pupil_dict = {}
                for idx, attribute in enumerate(pupil_attribute_columns):
                    new_pupil_dict[attribute] = data_list[idx]
                for idx, capability in enumerate(pupil_capability_columns)  :
                    new_pupil_dict[capability] = data_cleaned[idx]

                # send dict to db
                _ = PupilsService.create_new_pupil(new_pupil_dict)

                # update row to show imported
                wks.update_cell(current_row, imported_cell_column, 'DONE')

            current_row += 1

        return

    @staticmethod
    def get_file_path():
        print(os.path.abspath('../config/oauth2test-6162ffd5ef8b.json'))

    @staticmethod
    def export_column_names_to_sheet():
        wks = SheetsImport.access_sheets()
        capabilities = CapabilitiesService.get_capabilities(mode='nice')
        cell_offset = 3
        for key in capabilities.keys():
            cell_position = int(key[1:])
            wks.update_cell(1,cell_offset+cell_position, capabilities[key])
        return

