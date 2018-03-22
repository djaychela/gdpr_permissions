from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.pupil import Pupils
from gdpr_permissions.services.capabilities_service import CapabilitiesService
from gdpr_permissions.services.logging_service import LoggingService
from gdpr_permissions.config import config
from gdpr_permissions.services.preferences_service import Preferences


class PupilsService:
    @staticmethod
    def attributes():
        pupils_attributes_dict = config.pupils_attributes_dict.copy()
        return pupils_attributes_dict

    @staticmethod
    def all_attributes():
        attributes_dict = PupilsService.attributes()
        attributes_dict.update(CapabilitiesService.get_capabilities())
        return attributes_dict

    @staticmethod
    def get_pupils():
        session = DbSessionFactory.create_session()
        pupil_return = []
        for pupil in session.query(Pupils).all():
            pupil_return.append(pupil)
        return pupil_return

    @staticmethod
    def get_pupils_list(class_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        if class_filter is None or class_filter == "None":
            for pupil in session.query(Pupils) \
                    .order_by(Pupils.last_name.asc()).all():
                current_pupil_dict = {}
                for attribute in pupil_attributes:
                    current_pupil_dict[attribute] = eval('pupil.' + attribute)
                pupil_output_list.append(current_pupil_dict)
        else:
            for pupil in session.query(Pupils).filter(Pupils.class_id == class_filter) \
                    .all():
                current_pupil_dict = {}
                for attribute in pupil_attributes.keys():
                    current_pupil_dict[attribute] = eval('pupil.' + str(attribute))
                pupil_output_list.append(current_pupil_dict)
        return pupil_output_list

    @staticmethod
    def get_year_group_list(year_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        if year_filter is None or year_filter == "None":
            for pupil in session.query(Pupils) \
                    .order_by(Pupils.last_name.asc()).all():
                current_pupil_dict = {}
                for attribute in pupil_attributes:
                    current_pupil_dict[attribute] = eval('pupil.' + attribute)
                pupil_output_list.append(current_pupil_dict)
        else:
            for pupil in session.query(Pupils).join(Pupils.class_info)\
                    .filter(Pupils.class_info.property.mapper.class_.class_year == year_filter).all():
                current_pupil_dict = {}
                for attribute in pupil_attributes.keys():
                    current_pupil_dict[attribute] = eval('pupil.' + str(attribute))
                pupil_output_list.append(current_pupil_dict)
        return pupil_output_list

    @staticmethod
    def get_single_pupil(id):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_attributes['groups'] = 'groups'
        pupil = session.query(Pupils).get(id)
        current_pupil_dict = {}
        for attribute in pupil_attributes:
            current_pupil_dict[attribute] = eval('pupil.' + attribute)
        return current_pupil_dict

    @staticmethod
    def current_capabilities(id):
        session = DbSessionFactory.create_session()
        pupil_capabilities = CapabilitiesService.get_capabilities()
        for pupil in session.query(Pupils).filter(Pupils.id == id):
            current_capability_dict = {}
            for capability in pupil_capabilities:
                current_capability_dict[capability] = eval('pupil.' + capability)
        return current_capability_dict

    @staticmethod
    def capabilities_dict():
        capabilities_dict = {}
        capabilities_tag = list(CapabilitiesService.get_capabilities().values())
        capabilities_long = list(CapabilitiesService.get_capabilities(mode='nice').values())
        for i in range(len(capabilities_tag)):
            capabilities_dict[capabilities_tag[i]] = capabilities_long[i]
        return capabilities_dict



    @staticmethod
    def store_pupil_data(data_to_store):
        LoggingService.add_entry(data_to_store, 'pupil', 'edit')
        session = DbSessionFactory.create_session()
        pupil_to_edit = session.query(Pupils).get(data_to_store['id'])
        keys_to_store_as_text=PupilsService.attributes()
        keys_to_store_as_text['groups']='groups'
        for key, value in data_to_store.items():
            if key in keys_to_store_as_text:
                exec("pupil_to_edit." + key + "='" + str(value) + "'")
            else:
                exec("pupil_to_edit." + key + "=" + str(value))
        session.commit()
        PupilsService.create_pupil_overview(pupil_to_edit.id)
        return

    @staticmethod
    def create_pupil_overview(id):
        session = DbSessionFactory.create_session()
        pupil_capabilities = CapabilitiesService.get_capabilities()
        pupil = session.query(Pupils).get(id)
        total_permissions = 0
        for capability in pupil_capabilities:
            if eval('pupil.' + capability):
                total_permissions += 1
        if total_permissions == 0:
            pupil.overview = 'none'
        elif total_permissions == len(pupil_capabilities):
            pupil.overview = 'ok'
        else:
            pupil.overview = 'check'
        session.commit()
        return

    @staticmethod
    def get_pupils_overview(class_filter):
        session = DbSessionFactory.create_session()
        pupil_overview_dict = {}
        overview_info = ['ok', 'check', 'none']
        if class_filter == "None":
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils).filter(Pupils.overview == overview) \
                        .order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        else:
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils).filter(Pupils.class_id == class_filter) \
                        .filter(Pupils.overview == overview) \
                        .order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        return pupil_overview_dict

    @staticmethod
    def get_pupils_year_overview(year_filter):
        session = DbSessionFactory.create_session()
        pupil_overview_dict = {}
        overview_info = ['ok', 'check', 'none']
        if year_filter == "None":
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils).filter(Pupils.overview == overview) \
                        .order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        else:
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils).join(Pupils.class_info).filter(
                        Pupils.class_info.property.mapper.class_.class_year == year_filter, Pupils.overview == overview) \
                        .order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        return pupil_overview_dict

    @staticmethod
    def create_new_pupil(pupil_info_dict):
        session = DbSessionFactory.create_session()
        pupil_to_store = Pupils()
        for key in pupil_info_dict.keys():
            if key == 'class_id':
                exec("pupil_to_store." + key + "=" + str(pupil_info_dict[key]))
            elif type(pupil_info_dict[key]) is str:
                exec("pupil_to_store." + key + "='" + pupil_info_dict[key] + "'")
            elif type(pupil_info_dict[key]) is bool:
                exec("pupil_to_store." + key + "=" + str(pupil_info_dict[key]))
        session.add(pupil_to_store)
        session.commit()
        PupilsService.create_pupil_overview(pupil_to_store.id)
        pupil_info_dict['id'] = pupil_to_store.id
        LoggingService.add_entry(pupil_info_dict, 'pupil', 'create')
        return

    @staticmethod
    def pupil_year_update():
        number_of_year_groups = int(Preferences.get_preference('number_of_year_groups'))
        session = DbSessionFactory.create_session()
        for pupil in session.query(Pupils).all():
            current_pupil_class = pupil.class_id
            if current_pupil_class % number_of_year_groups == 0:
                session.query(Pupils).filter(Pupils.id == pupil.id).delete()
                LoggingService.delete_user_entries(pupil.id)
            else:
                pupil.class_id += 1
                session.add(pupil)
        session.commit()
        return

    @staticmethod
    def delete_single_pupil(pupil_id):
        session = DbSessionFactory.create_session()
        session.query(Pupils).filter(Pupils.id == pupil_id).delete()
        deleted_pupil = {'id': pupil_id}
        LoggingService.add_entry(deleted_pupil, 'pupil', 'delete')
        session.commit()
        return

    @staticmethod
    def update_pupil_classes(old_class, new_class):
        session = DbSessionFactory.create_session()
        for pupil in session.query(Pupils).filter(Pupils.class_id == old_class):
            pupil.class_id = new_class
            pupil_log = {'id': pupil.id, 'class_id': new_class}
            for attribute in PupilsService.attributes():
                pupil_log[attribute] = eval('pupil.' + attribute)
            for capability in CapabilitiesService.get_capabilities():
                pupil_log[capability] = eval('pupil.' + capability)
            LoggingService.add_entry(pupil_log, 'pupil', 'move')
        session.commit()
        return

    @staticmethod
    def get_pupils_with_groups(group_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_attributes['groups'] = 'groups'
        pupil_output_list = []
        if group_filter == "None":
            for pupil in session.query(Pupils).filter(Pupils.groups != ''):
                current_pupil_dict = {}
                for attribute in pupil_attributes.keys():
                    current_pupil_dict[attribute] = eval('pupil.' + str(attribute))
                pupil_output_list.append(current_pupil_dict)
        else:
            for pupil in session.query(Pupils).filter(Pupils.groups != ''):
                current_pupil_dict = {}
                for attribute in pupil_attributes.keys():
                    current_pupil_dict[attribute] = eval('pupil.' + str(attribute))
                if str(group_filter) in pupil.groups:
                    pupil_output_list.append(current_pupil_dict)
        return pupil_output_list

    @staticmethod
    def get_pupils_with_groups_overview(group_filter):
        session = DbSessionFactory.create_session()
        pupil_overview_dict = {}
        overview_info = ['ok', 'check', 'none']
        if group_filter == "None":
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils).filter(Pupils.overview == overview) \
                        .filter(Pupils.groups != '').order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        else:
            for overview in overview_info:
                current_pupils_list = []
                for pupil in session.query(Pupils) \
                        .filter(Pupils.overview == overview).filter(Pupils.groups != '') \
                        .order_by(Pupils.last_name):
                    groups = pupil.groups
                    group_list = groups.split(' ')
                    if str(group_filter) in group_list:
                        current_pupils_list.append(pupil.first_name + " " + pupil.last_name.upper())
                pupil_overview_dict[overview] = current_pupils_list
        return pupil_overview_dict
