import os
import json
import datetime

log_file = 'pupil_data_logfile.json'


class LoggingService:
    @staticmethod
    def start_logging():
        log_file_entry = {'message': '*** SYSTEM STARTUP ***'}
        LoggingService.add_entry(log_file_entry, mode='system', action='startup')
        return

    @staticmethod
    def read_logfile():
        log_file_contents = []
        with open(log_file, 'r') as file:
            for line in file:
                log_file_contents.append(json.loads(line))
        return log_file_contents

    @staticmethod
    def read_logfile_by_id(id):
        log_file_contents = []
        with open(log_file, 'r') as file:
            for line in file:
                current_dict = json.loads(line)
                if 'id' in current_dict.keys() and int(current_dict['id']) == id:
                    log_file_contents.append(current_dict)
        return log_file_contents

    @staticmethod
    def add_entry(log_entry, mode, action):
        output = {'date': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 'entrytype': mode, 'action': action}
        output_dict = dict(output, **log_entry)
        with open(log_file, 'a') as file:
            file.write(json.dumps(output_dict))
            file.write('\n')
        return

    @staticmethod
    def delete_user_entries(pupil_id):
        new_log_entries=[]
        with open(log_file, 'r') as file:
            for line in file:
                current_dict = json.loads(line)
                if 'id' in current_dict.keys() and current_dict['id'] == pupil_id:
                    pass
                else:
                    new_log_entries.append(current_dict)
        with open(log_file, 'w') as file:
            for line in new_log_entries:
                file.write(json.dumps(line))
                file.write('\n')
        return
