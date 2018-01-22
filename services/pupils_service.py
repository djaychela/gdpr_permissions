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


