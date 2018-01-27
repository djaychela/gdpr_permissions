from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.pupil import Pupils
from gdpr_permissions.data.classes import Classes


class PupilsService:
    @staticmethod
    def get_pupils():
        session = DbSessionFactory.create_session()
        pupil_return = []
        for pupil in session.query(Pupils).all():
            pupil_return.append(pupil)
        return pupil_return

    @staticmethod
    def get_pupils_list(sort_order, filter, class_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        if filter:
            filter_string = 'Pupils.' + filter + '== True'
            for pupil in session.query(Pupils).filter(eval(filter_string)) \
                    .filter(Pupils.class_id == class_filter) \
                    .order_by(eval('Pupils.' + sort_order)):
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
    def capabilities():
        return ['damers_web', 'damers_blog', 'damers_twitter',
                'damers_class_photo', 'damers_prod_dvd', 'damers_newsletter', \
                'wistia_video', 'dasp_web', 'dasp_music_web', 'dor_echo', 'cel_pound_mag', 'cel_pound_web']

    @staticmethod
    def capabilities_nice_name():
        return ['Web', 'Blog', 'Twitter', 'Photos', 'DVD', 'News', 'Wistia', 'DASP-W', 'DASPMW', 'D-Echo', 'PoundM',
                'PoundW']

    @staticmethod
    def capabilities_dict():
        capabilities_dict = {}
        capabilities_tag = PupilsService.capabilities()
        capabilities_long = PupilsService.capabilities_nice_name()
        for i in range(len(capabilities_tag)):
            capabilities_dict[capabilities_tag[i]] = capabilities_long[i]
        return capabilities_dict

    @staticmethod
    def attributes():
        return ['id', 'first_name', 'last_name', 'class_id', 'class_info.class_strand', 'class_info.class_year']

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
        print(data_to_store)
        for key, value in data_to_store.items():
            if key in PupilsService.attributes():
                exec("pupil_to_edit." + key + "='" + str(value) + "'")
            else:
                exec("pupil_to_edit." + key + "=" + str(value) + "")
        session.commit()

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
