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
    def get_pupils_list(sort_order, class_filter):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        if class_filter is None or class_filter=="None":
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

    @staticmethod
    def create_pupil_overview(id):
        session = DbSessionFactory.create_session()
        pupil_capabilities = PupilsService.capabilities()
        pupil = session.query(Pupils).get(id)
        total_permissions = 0
        for capability in pupil_capabilities:
            if eval('pupil.' + capability):
                total_permissions +=1
        print(total_permissions)
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
        overview_info=['ok','check','none']
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
                for pupil in session.query(Pupils).filter(Pupils.class_id == class_filter)\
                        .filter(Pupils.overview == overview)\
                        .order_by(Pupils.last_name):
                    current_pupils_list.append(pupil.first_name+ " "+pupil.last_name.upper())
                pupil_overview_dict[overview]=current_pupils_list
        return pupil_overview_dict