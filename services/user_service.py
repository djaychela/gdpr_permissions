from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.user import Users
from gdpr_permissions.services.accounts_service import AccountsService
from gdpr_permissions.services.logging_service import LoggingService


class UsersService:
    @staticmethod
    def get_users():
        session = DbSessionFactory.create_session()
        user_return = []
        for user in session.query(Users).all():
            user_return.append(user)
        return user_return

    @classmethod
    def by_name(cls, name):
        session = DbSessionFactory.create_session()
        return session.query(Users).filter(Users.username == name).first()

    @staticmethod
    def users_to_list(user_list):
        user_output_list = []
        for user in user_list:
            current_user_dict = {}
            current_user_dict['id'] = user.id
            current_user_dict['username'] = user.username
            current_user_dict['pwdhash'] = user.pwdhash
            current_user_dict['cap_view'] = user.cap_view
            current_user_dict['cap_edit'] = user.cap_edit
            user_output_list.append(current_user_dict)
        return user_output_list

    @staticmethod
    def users_to_list_2(user_list):
        user_attributes = ['id', 'username', 'pwdhash', 'cap_view', 'cap_edit']
        user_output_list = []
        for user in user_list:
            current_user_dict = {}
            for attribute in user_attributes:
                current_user_dict[attribute] = eval('user.' + attribute)
            user_output_list.append(current_user_dict)
        return user_output_list

    @staticmethod
    def get_users_list():
        session = DbSessionFactory.create_session()
        user_attributes = ['id', 'username', 'password_hash', 'cap_view', 'cap_edit']
        user_output_list = []
        for user in session.query(Users).all():
            current_user_dict = {}
            for attribute in user_attributes:
                current_user_dict[attribute] = eval('user.' + attribute)
            user_output_list.append(current_user_dict)
        return user_output_list

    @staticmethod
    def get_current_user_info(user_id):
        session = DbSessionFactory.create_session()
        user_attributes = ['id', 'username', 'password_hash', 'cap_view', 'cap_edit']
        user_output_dict = {}
        user = session.query(Users).get(user_id)
        for attribute in user_attributes:
            user_output_dict[attribute] = eval('user.' + attribute)
        return user_output_dict

    @staticmethod
    def change_user_password(user_id, password):
        session = DbSessionFactory.create_session()
        user = session.query(Users).get(user_id)
        user.password_hash = AccountsService.create_password_hash(password)
        session.commit()
        user_log={'user_id':user_id, 'username': user.username}
        LoggingService.add_entry(user_log, 'user','password_change')
        return

    @staticmethod
    def create_new_user(username, password):
        session = DbSessionFactory.create_session()
        user_to_store = Users()
        user_to_store.username = username
        user_to_store.password_hash = AccountsService.create_password_hash(password)
        session.add(user_to_store)
        session.commit()
        user_log = {'user_id': user_to_store.id, 'username': user_to_store.username}
        LoggingService.add_entry(user_log, 'user', 'created')
        return

    @staticmethod
    def delete_user(user_id):
        session = DbSessionFactory.create_session()
        user_to_log = session.query(Users).get(user_id)
        session.query(Users).filter(Users.id == user_id).delete()
        session.commit()
        user_log = {'user_id': user_to_log.id, 'username': user_to_log.username}
        LoggingService.add_entry(user_log, 'user', 'deleted')
        return
