import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gdpr_permissions.services.pupils_service import PupilsService


class SheetsImport:
    @staticmethod
    def import_from_sheets():
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/darrenjones/PycharmProjects/dj/damers/gdpr_permissions/gdpr_permissions/services/oauth2test-c0ddcb504254.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Pupil Import Test Sheet').sheet1

        current_row = 2
        # get data list and clean values to True and False
        while wks.cell(current_row,1).value:
            data_list = wks.row_values(current_row)
            data_cleaned = [True if x=='TRUE' else False for x in data_list[3:]]

            #check if row already imported
            imported_cell_column = 4 + len(PupilsService.capabilities())
            if wks.cell(current_row,imported_cell_column).value != "DONE":

                # build pupil dict to send to db
                new_pupil_dict = {}
                for idx, attribute in enumerate(PupilsService.attributes()[1:4]):
                    new_pupil_dict[attribute]=data_list[idx]
                for idx, capability in enumerate(PupilsService.capabilities()):
                    new_pupil_dict[capability]=data_cleaned[idx]

                # send dict to db
                _ = PupilsService.create_new_pupil(new_pupil_dict)

                # update row to show imported
                wks.update_cell(current_row,imported_cell_column,'DONE')

            print(f"{current_row} - done.")
            current_row +=1

        print('all imported.')
        return
