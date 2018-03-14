from gdpr_permissions.data.groups import Groups
from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.services.logging_service import LoggingService


class GroupsService():
    @staticmethod
    def list_all_attributes() -> list:
        return ['id', 'group_name', 'group_desc']

    @staticmethod
    def get_all_groups():
        session = DbSessionFactory.create_session()
        groups_output_list = []
        for group in session.query(Groups).all():
            current_group_dict={}
            for attribute in GroupsService.list_all_attributes():
                current_group_dict[attribute] = eval('group.' + attribute)
            groups_output_list.append(current_group_dict)
        return groups_output_list

    @staticmethod
    def get_group_names():
        session = DbSessionFactory.create_session()
        groups_output_dict={}
        for group in session.query(Groups).all():
            groups_output_dict[group.id] = group.group_name
        return groups_output_dict

    @staticmethod
    def get_single_group_info(group_id) -> dict:
        session = DbSessionFactory.create_session()
        attributes = GroupsService.list_all_attributes()
        group_info_return = {}
        group_info = session.query(Groups).get(group_id)
        for attribute in attributes:
            group_info_return[attribute] = eval('group_info.' + attribute)
        return group_info_return

    @staticmethod
    def store_group_info(group_to_store):
        attributes = GroupsService.list_all_attributes()
        session = DbSessionFactory.create_session()
        group_to_be_stored = session.query(Groups).get(group_to_store['id'])
        for attribute in attributes:
            exec("group_to_be_stored." + attribute + "='" + group_to_store[attribute] + "'")
        session.commit()
        LoggingService.add_entry(group_to_store, 'group', 'store')
        return

    @staticmethod
    def delete_group(group_id):
        session = DbSessionFactory.create_session()
        session.query(Groups).filter(Groups.id == group_id).delete()
        session.commit()
        deleted_group = {'id': group_id}
        LoggingService.add_entry(deleted_group, 'group', 'delete')
        return

    @staticmethod
    def create_new_group(group_info):
        session = DbSessionFactory.create_session()
        group_to_store = Groups()
        for key in group_info.keys():
            exec("group_to_store." + key + "='" + group_info[key] + "'")
        session.add(group_to_store)
        session.commit()
        LoggingService.add_entry(group_info, 'group', 'create')
        return

