from gdpr_permissions.data.dbsession import DbSessionFactory
from gdpr_permissions.data.user import Users


class UsersService:
    @staticmethod
    def get_users():
        session = DbSessionFactory.create_session()
        user_return = []
        for user in session.query(Users).all():
            user_return.append(user)

        return user_return

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
        user_attributes = ['id', 'username', 'pwdhash', 'cap_view', 'cap_edit']
        user_output_list = []
        for user in session.query(Users).all():
            current_user_dict = {}
            for attribute in user_attributes:
                current_user_dict[attribute] = eval('user.' + attribute)
            user_output_list.append(current_user_dict)
        return user_output_list
