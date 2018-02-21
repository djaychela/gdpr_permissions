from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.pupil import Pupils
from gdpr_permissions.data.classes import Classes
import gdpr_permissions.settings


class PupilsService:
    @staticmethod
    def attributes():
        return ['id', 'first_name', 'last_name', 'class_id']

    @staticmethod
    def capabilities():
        return ['damers_web', 'damers_blog', 'damers_twitter',
                'damers_class_photo', 'damers_prod_dvd', 'damers_newsletter', \
                'wistia_video', 'dasp_web', 'dasp_music_web', 'dor_echo', 'cel_pound_mag', 'cel_pound_web']

    @staticmethod
    def capabilities_nice_name():
        return ['Web', 'Blog', 'Twitter', 'Photos', 'DVD', 'News', 'Wistia', 'DASP-W', 'DASPMW', 'D-Echo', 'PoundM',
                'PoundW']

    @staticmethod
    def get_pupils():
        session = DbSessionFactory.create_session()
        pupil_return = []
        for pupil in session.query(Pupils).all():
            pupil_return.append(pupil)
        return pupil_return

    @staticmethod
    def get_pupils_list(sort_order, class_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        if class_filter is None or class_filter == "None":
            for pupil in session.query(Pupils) \
                    .order_by(eval('Pupils.' + sort_order)).all():
                current_pupil_dict = {}
                for attribute in pupil_attributes:
                    current_pupil_dict[attribute] = eval('pupil.' + attribute)
                pupil_output_list.append(current_pupil_dict)
        else:
            for pupil in session.query(Pupils).filter(Pupils.class_id == class_filter) \
                    .order_by(eval('Pupils.' + sort_order)).all():
                current_pupil_dict = {}
                for attribute in pupil_attributes:
                    current_pupil_dict[attribute] = eval('pupil.' + attribute)
                pupil_output_list.append(current_pupil_dict)
        return pupil_output_list

    @staticmethod
    def get_single_pupil(id):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil = session.query(Pupils).get(id)
        current_pupil_dict = {}
        for attribute in pupil_attributes:
            current_pupil_dict[attribute] = eval('pupil.' + attribute)
        return current_pupil_dict

    @staticmethod
    def current_capabilities(id):
        session = DbSessionFactory.create_session()
        pupil_capabilities = PupilsService.capabilities()
        for pupil in session.query(Pupils).filter(Pupils.id == id):
            current_capability_dict = {}
            for capability in pupil_capabilities:
                current_capability_dict[capability] = eval('pupil.' + capability)
        return current_capability_dict

    @staticmethod
    def capabilities_dict():
        capabilities_dict = {}
        capabilities_tag = PupilsService.capabilities()
        capabilities_long = PupilsService.capabilities_nice_name()
        for i in range(len(capabilities_tag)):
            capabilities_dict[capabilities_tag[i]] = capabilities_long[i]
        return capabilities_dict

    @staticmethod
    def all_attributes():
        attributes_list = PupilsService.attributes()
        for attribute in PupilsService.capabilities():
            attributes_list.append(attribute)
        return attributes_list

    @staticmethod
    def store_pupil_data(data_to_store):
        session = DbSessionFactory.create_session()
        pupil_to_edit = session.query(Pupils).get(data_to_store['id'])
        for key, value in data_to_store.items():
            if key in PupilsService.attributes():
                exec("pupil_to_edit." + key + "='" + str(value) + "'")
            else:
                exec("pupil_to_edit." + key + "=" + str(value) + "")
        session.commit()
        PupilsService.create_pupil_overview(pupil_to_edit.id)
        return

    @staticmethod
    def pupil_join_query():
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        print(pupil_attributes)
        for pupil in session.query(Pupils).join(Classes, Classes.id == Pupils.class_id).filter(Pupils.id == 1):
            current_pupil_dict = {}
            print(pupil)
            for attribute in pupil_attributes:
                print(attribute)
                print(pupil.classes.class_strand)
                current_pupil_dict[attribute] = eval('pupil.' + attribute)
            pupil_attributes.append(current_pupil_dict)
        return pupil_attributes

    @staticmethod
    def create_pupil_overview(id):
        session = DbSessionFactory.create_session()
        pupil_capabilities = PupilsService.capabilities()
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
    def get_number_of_pupils():
        session = DbSessionFactory.create_session()
        number_of_rows = session.query(Pupils).count()
        return number_of_rows

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

        return

    @staticmethod
    def pupil_year_update():
        session = DbSessionFactory.create_session()
        for pupil in session.query(Pupils).all():
            current_pupil_class = pupil.class_id
            if current_pupil_class % 5 == 0:
                session.query(Pupils).filter(Pupils.id == pupil.id).delete()
            else:
                pupil.class_id += 1
                session.add(pupil)
        session.commit()
        return

    @staticmethod
    def delete_single_pupil(id):
        session = DbSessionFactory.create_session()
        session.query(Pupils).filter(Pupils.id == id).delete()
        session.commit()
        return
