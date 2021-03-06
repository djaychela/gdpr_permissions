from pyramid.config import Configurator
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import os
from gdpr_permissions.data.dbsession import DbSessionFactory
import gdpr_permissions
from gdpr_permissions.services.logging_service import LoggingService
from gdpr_permissions.services.preferences_service import Preferences



def init_db(config):
    top_folder = os.path.dirname(gdpr_permissions.__file__)
    rel_folder = os.path.join('db', 'gdpr_permissions_db.db')
    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


class Root(object):
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, 'admin', ALL_PERMISSIONS), ]

    def __init__(self, request):
        self.request = request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authentication_policy = AuthTktAuthenticationPolicy('gdpr_permissions')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.include('pyramid_jinja2')
    config.set_root_factory(Root)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # user pages
    config.add_route('class_view_detail', '/class_view_detail')
    config.add_route('class_view_summary', '/class_view_summary')
    config.add_route('year_view_summary', '/year_view_summary')
    config.add_route('year_view_detail', '/year_view_detail')
    config.add_route('groups_view_summary', '/groups_view_summary')
    config.add_route('groups_view_detail', '/groups_view_detail')

    # admin pages
    config.add_route('users', '/admin/users')
    config.add_route('create_user', '/admin/create_user')
    config.add_route('delete_user', '/admin/delete_user')
    config.add_route('set_password', '/admin/set_password')
    config.add_route('create_pupil', '/admin/create_pupil')
    config.add_route('edit', '/admin/edit', factory='gdpr_permissions.services.accounts_service.DatabaseRecordFactory')
    config.add_route('import_from_sheets', 'admin/import_from_sheets')
    config.add_route('year_group_update_1', '/admin/year_group_update_1')
    config.add_route('year_group_update_2', '/admin/year_group_update_2')
    config.add_route('delete_pupil', '/admin/delete_pupil')
    config.add_route('logfile_read', '/admin/logfile_read')
    config.add_route('logfile_pupil_history', '/admin/logfile_pupil_history')
    config.add_route('classes_list', '/admin/classes_list')
    config.add_route('class_edit', '/admin/class_edit')
    config.add_route('class_create', '/admin/class_create')
    config.add_route('class_delete', '/admin/class_delete')
    config.add_route('capabilities_list', '/admin/capabilities_list')
    config.add_route('capability_edit', '/admin/capability_edit')
    config.add_route('groups_list', '/admin/groups_list')
    config.add_route('group_edit', '/admin/group_edit')
    config.add_route('group_delete', '/admin/group_delete')
    config.add_route('group_create', '/admin/group_create')

    # sign in pages
    config.add_route('auth', '/sign/{action}')
    config.add_route('signin', '/signin')

    # logging setup
    LoggingService.start_logging()

    config.scan()
    init_db(config)
    app = config.make_wsgi_app()
    return app