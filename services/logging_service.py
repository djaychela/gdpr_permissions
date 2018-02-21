import os
import json
import datetime

log_file='pupil_data_logfile.json'


class LoggingService:
    @staticmethod
    def create_logfile():
        log_file_entry={'message': '*** SYSTEM STARTUP ***'}
        LoggingService.add_entry(log_file_entry, mode='system', action='startup')
        return

    @staticmethod
    def read_logfile():
        with open(log_file, 'r') as file:
            log_file_contents=file.read()
        return log_file_contents

    @staticmethod
    def add_entry(log_entry, mode, action):
        output = {'date': str(datetime.datetime.now()), 'entrytype': mode, 'action': action}
        output_dict = dict(output, **log_entry)
        with open(log_file, 'a') as file:
            file.write(json.dumps(output_dict))
            file.write('\n')
        return




