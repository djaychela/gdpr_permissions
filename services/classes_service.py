from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.classes import Classes


class ClassesService():
    @staticmethod
    def get_all_classes() -> dict:
        session = DbSessionFactory.create_session()
        class_return = {}
        for classes in session.query(Classes).order_by(Classes.class_strand).all():
            class_name = classes.class_strand + ' ' + classes.class_year
            class_return[classes.id]=class_name
        return class_return

    @staticmethod
    def get_all_year_groups() -> list:
        session = DbSessionFactory.create_session()
        year_return = []
        for classes in session.query(Classes).order_by(Classes.class_year).all():
            year_return.append(classes.class_year)
        return year_return

