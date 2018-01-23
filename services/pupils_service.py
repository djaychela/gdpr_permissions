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
        pupil_attributes =['id','first_name','last_name','damers_web','damers_blog','damers_twitter','damers_class_photo','damers_prod_dvd','damers_newsletter', \
                'wistia_video','dasp_web','dasp_music_web','dor_echo','cel_pound_mag','cel_pound_web']
        pupil_output_list =[]
        for pupil in session.query(Pupils).all():
            current_pupil_dict={}
            for attribute in pupil_attributes:
                current_pupil_dict[attribute] = eval('pupil.' + attribute)
            pupil_output_list.append(current_pupil_dict)
        return pupil_output_list


