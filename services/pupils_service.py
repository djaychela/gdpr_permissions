from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.pupil import Pupils


class PupilsService:
    @staticmethod
    def get_pupils():
        session = DbSessionFactory.create_session()
        pupil_return = []
        for pupil in session.query(Pupils).all():
            pupil_return.append(pupil)

        return pupil_return

    @staticmethod
    def get_pupils_list():
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        pupil_output_list = []
        for pupil in session.query(Pupils).order_by(Pupils.last_name).all():
            current_pupil_dict = {}
            for attribute in pupil_attributes:
                current_pupil_dict[attribute] = eval('pupil.' + attribute)
            pupil_output_list.append(current_pupil_dict)
        return pupil_output_list

    @staticmethod
    def get_single_pupil(id):
        session = DbSessionFactory.create_session()
        pupil_attributes = PupilsService.all_attributes()
        for pupil in session.query(Pupils).order_by(Pupils.last_name).filter(Pupils.id == id):
            current_pupil_dict = {}
            for attribute in pupil_attributes:
                current_pupil_dict[attribute] = eval('pupil.' + attribute)
        return current_pupil_dict

    @staticmethod
    def capabilities():
        return ['damers_web', 'damers_blog', 'damers_twitter',
                            'damers_class_photo', 'damers_prod_dvd', 'damers_newsletter', \
                            'wistia_video', 'dasp_web', 'dasp_music_web', 'dor_echo', 'cel_pound_mag', 'cel_pound_web']

    @staticmethod
    def all_attributes():
        attributes_list = ['id', 'first_name', 'last_name']
        for attribute in PupilsService.capabilities():
            attributes_list.append(attribute)
        return attributes_list