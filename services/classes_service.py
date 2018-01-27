from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.classes import Classes


class ClassesService():
    @staticmethod
    def get_all_classes():
        session = DbSessionFactory.create_session()
        class_return = {}
        for classes in session.query(Classes).order_by(Classes.class_strand).all():
            class_name = classes.class_strand + ' ' + classes.class_year
            class_return[classes.id]=class_name
        return class_return

