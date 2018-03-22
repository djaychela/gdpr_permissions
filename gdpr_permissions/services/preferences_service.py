import json, os
import gdpr_permissions
top_folder = os.path.dirname(gdpr_permissions.__file__)
rel_folder = os.path.join('config', 'gdpr_preferences.json')
prefs_file = os.path.join(top_folder, rel_folder)


class Preferences:
    @staticmethod
    def get_preference(pref_name):
        prefs = Preferences.read_preferences()
        if pref_name in prefs.keys():
            return prefs[pref_name]
        else:
            return "Error: Pref '{}' not found".format(pref_name)

    @staticmethod
    def store_preference(pref_name, pref_value):
        current_prefs = Preferences.read_preferences()
        current_prefs[pref_name] = pref_value
        Preferences.write_preferences(current_prefs)

    @staticmethod
    def read_preferences() -> dict:
        prefs_file_output = {}
        with open(prefs_file, 'r') as prefs_file_contents:
            for line in prefs_file_contents:
                current_pref = json.loads(line.strip())
                prefs_file_output.update(current_pref)
        return prefs_file_output

    @staticmethod
    def write_preferences(prefs_dict):
        with open(prefs_file, 'w') as prefs_file_on_disk:
            prefs_file_on_disk.write(json.dumps(prefs_dict))
        return
