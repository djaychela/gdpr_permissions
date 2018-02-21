import os
import json

log_file='pupil_data_logfile.json'


class LoggingService:
    def create_logfile(self):
        with open(log_file,'a+') as file:
            file.write()
        return

    def read_logfile(self):
        with open(log_file, 'r') as file:
            log_file_contents=file.read()
        return log_file_contents

    def append_logfile(self, log_entry):
        with open(log_file, 'r+') as file:
            file.write(log_entry)

        return



