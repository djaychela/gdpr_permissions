from pyramid.config import Configurator
import os
from gdpr_permissions.data.dbsession import DbSessionFactory
import gdpr_permissions


def init_db(config):
    top_folder = os.path.dirname(gdpr_permissions.__file__)
    rel_folder = os.path.join('db','gdpr_permissions_db.db')
    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('list', '/list')
    config.add_route('users', '/users')
    config.add_route('edit', '/edit')
    config.add_route('list_2','/list_2')
    config.add_route('classes_list','/classes_list')
    config.add_route('class_list_capabilities','/class_list_capabilities')
    config.add_route('update_overview','/update_overview')
    config.add_route('import_from_sheets','/import_from_sheets')
    config.scan()
    init_db(config)
    return config.make_wsgi_app()
