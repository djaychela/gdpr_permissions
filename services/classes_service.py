from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.classes import Classes
from gdpr_permissions.services.logging_service import LoggingService
from gdpr_permissions.config import config


class ClassesService():
    @staticmethod
    def attributes():
        attributes_list = config.class_attributes_list[:]
        return attributes_list

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

    @staticmethod
    def get_all_class_info() -> list:
        attributes = ClassesService.attributes()
        session = DbSessionFactory.create_session()
        class_info_return = []
        for classes in session.query(Classes).order_by(Classes.id).all():
            current_class_dict = {}
            for attribute in attributes:
                current_class_dict[attribute]=eval('classes.'+attribute)
            class_info_return.append(current_class_dict)
        return class_info_return

    @staticmethod
    def get_single_class_info(id) -> dict:
        attributes = ClassesService.attributes()
        session = DbSessionFactory.create_session()
        class_info_return = {}
        class_info = session.query(Classes).get(id)
        for attribute in attributes:
            class_info_return[attribute] = eval('class_info.'+attribute)
        return class_info

    @staticmethod
    def store_single_class_info(class_info):
        attributes = ClassesService.attributes()
        session = DbSessionFactory.create_session()
        class_to_store = session.query(Classes).get(class_info['id'])
        for attribute in attributes[1:]:
            exec("class_to_store." + attribute + "='" + class_info[attribute] + "'")
        session.commit()
        LoggingService.add_entry(class_info, 'class','edit')
        return

    @staticmethod
    def create_new_class(class_info):
        session = DbSessionFactory.create_session()
        class_to_store = Classes()
        for key in class_info.keys():
            exec("class_to_store." + key + "='" + class_info[key] + "'")
        session.add(class_to_store)
        session.commit()
        LoggingService.add_entry(class_info, 'class', 'create')
        return

    @staticmethod
    def delete_class(class_id):
        session = DbSessionFactory.create_session()
        session.query(Classes).filter(Classes.id == class_id).delete()
        deleted_class = {'id': class_id}
        LoggingService.add_entry(deleted_class, 'class', 'delete')
        session.commit()
        return
