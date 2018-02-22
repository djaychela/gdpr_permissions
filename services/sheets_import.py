import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gdpr_permissions.services.pupils_service import PupilsService
import os


class SheetsImport:
    @staticmethod
    def import_from_sheets():
        scope = ['https://spreadsheets.google.com/feeds']
        oath_file = 'oauth2test-c0ddcb504254.json'
        oath_file_location = os.path.abspath('gdpr_permissions/config/'+oath_file)
        print(oath_file_location)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oath_file_location, scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Pupil Import Test Sheet').sheet1

        current_row = 2
        # get data list and clean values to True and False
        while wks.cell(current_row, 1).value:
            data_list = wks.row_values(current_row)
            data_cleaned = [True if x == 'TRUE' else False for x in data_list[3:]]

            # check if row already imported
            imported_cell_column = 4 + len(PupilsService.capabilities())
            if wks.cell(current_row, imported_cell_column).value != "DONE":

                # build pupil dict to send to db
                new_pupil_dict = {}
                for idx, attribute in enumerate(PupilsService.attributes()[1:4]):
                    new_pupil_dict[attribute] = data_list[idx]
                for idx, capability in enumerate(PupilsService.capabilities()):
                    new_pupil_dict[capability] = data_cleaned[idx]

                # send dict to db
                _ = PupilsService.create_new_pupil(new_pupil_dict)

                # update row to show imported
                wks.update_cell(current_row, imported_cell_column, 'DONE')

            current_row += 1

        return

    @staticmethod
    def get_file_path():
        print(os.path.abspath('../config/oauth2test-c0ddcb504254.json'))